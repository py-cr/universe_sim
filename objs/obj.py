# -*- coding:utf-8 -*-
# title           :对象基类
# description     :对象基类（所有星体都继承了该类）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from abc import ABCMeta, abstractmethod
import json
import numpy as np
import math
from common.consts import AU
import copy
import os


class Obj(metaclass=ABCMeta):
    """
    对象基类
    """

    def __init__(self, name, mass, init_position, init_velocity,
                 density=5e3, color=(125 / 255, 125 / 255, 125 / 255),
                 texture=None, size_scale=1.0, distance_scale=1.0,
                 parent=None, ignore_mass=False,
                 trail_color=None, show_name=False,
                 gravity_only_for=[], model=None):
        """
        对象类
        @param name: 对象名称
        @param mass: 对象质量 (kg)
        @param init_position: 初始位置 (km)
        @param init_velocity: 初始速度 (km/s)
        @param density: 平均密度 (kg/m³)
        @param color: 对象颜色（纹理图片优先）
        @param texture: 纹理图片
        @param size_scale: 尺寸缩放
        @param distance_scale: 距离缩放
        @param parent: 对象的父对象
        @param ignore_mass: 是否忽略质量（如果为True，则不计算引力）
                            TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在对象物理学中是不严谨）
        @param trail_color: 对象拖尾颜色（默认对象颜色）
        @param show_name: 是否显示对象名称
        """
        self.__his_pos = []
        self.__his_vel = []
        self.__his_acc = []
        self.__his_reserved_num = 200
        self.gravity_only_for = gravity_only_for
        self.model = self.find_model(model)

        if name is None:
            name = getattr(self.__class__, '__name__')

        self.name = name
        self.__mass = mass

        # 是否忽略质量（如果为True，则不计算引力）
        # TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在对象物理学中是不严谨）
        if self.__mass <= 0:  # 质量小于等于0就忽略
            self.ignore_mass = True
        else:
            self.ignore_mass = ignore_mass

        self.__init_position = None
        self.__init_velocity = None

        self.init_position = np.array(init_position, dtype='float32')
        self.init_velocity = np.array(init_velocity, dtype='float32')

        self.__density = density

        self.color = color
        self.trail_color = color if trail_color is None else trail_color
        self.texture = texture

        self.size_scale = size_scale
        self.distance_scale = distance_scale

        # 初始化后，加速度为0，只有多个对象的引力才会影响到加速度
        # km/s²
        self.__acceleration = np.array([0, 0, 0], dtype='float32')
        self.__record_history()

        # 是否显示
        self.appeared = True
        self.parent = parent

        self.show_name = show_name

        self.resolution = None
        self.light_disable = False

        self.__has_rings = False

    def find_model(self, model: str):
        if not model.endswith(".obj"):
            return model
        if os.path.exists(model):
            return model
        paths = [os.path.join('.', 'objs/models'),
                 os.path.join('..', 'objs/models'),
                 os.path.join('..', '..', 'objs/models')]
        for path in paths:
            p = os.path.join(path, model)
            if os.path.exists(p):
                return p

        return ""

    def set_ignore_gravity(self, value=True):
        """
        设置忽略质量，True为引力失效
        @param value:
        @return:
        """
        # TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在对象物理学中是不严谨）
        if self.__mass <= 0:  # 质量小于等于0就忽略
            self.ignore_mass = True
        else:
            self.ignore_mass = value
        return self

    def set_light_disable(self, value=True):
        """
        设置灯光为无效
        @param value:
        @return:
        """
        self.light_disable = value
        return self

    def set_resolution(self, value):
        """
        设置对象的分辨率
        @param value:
        @return:
        """
        self.resolution = value
        return self

    @property
    def init_position(self):
        """
        获取对象的初始位置（单位：km）
        @return:
        """
        return self.__init_position

    @init_position.setter
    def init_position(self, value):
        """
        设置对象的初始位置（单位：km）
        @param value:
        @return:
        """
        self.__init_position = np.array(value, dtype='float32')
        self.__position = copy.deepcopy(self.__init_position)

    @property
    def init_velocity(self):
        """
        获取对象的初始速度 (km/s)
        @return:
        """
        return self.__init_velocity

    @init_velocity.setter
    def init_velocity(self, value):
        """
        设置对象的初始速度 (km/s)
        @param value:
        @return:
        """
        self.__init_velocity = np.array(value, dtype='float32')
        self.__velocity = copy.deepcopy(self.__init_velocity)

    @property
    def position(self):
        """
        获取对象的位置（单位：km）
        @return:
        """
        return self.__position

    @position.setter
    def position(self, value):
        """
        设置对象的位置（单位：km）
        @param value:
        @return:
        """
        self.__position = value
        self.__record_history()

    @property
    def acceleration(self):
        """
        获取对象的加速度（单位：km/s²）
        @return:
        """
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, value):
        """
        设置对象的加速度（单位：km/s²）
        @param value:
        @return:
        """
        self.__acceleration = np.array(value, dtype=float)
        self.__record_history()

    def stop(self):
        """
        停止运动，将加速度和速度置零
        @return:
        """
        self.velocity = [0.0, 0.0, 0.0]
        self.acceleration = [0.0, 0.0, 0.0]

    def stop_and_ignore_gravity(self):
        """
        停止运动，并忽略质量（不受引力影响）
        TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在对象物理学中是不严谨）
        @return:
        """
        self.set_ignore_gravity()
        self.stop()

    @property
    def velocity(self):
        """
        获取对象的速度（单位：km/s）
        @return:
        """
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        """
        设置对象的速度（单位：km/s）
        @param value:
        @return:
        """
        self.__velocity = value
        self.__record_history()

    def __append_history(self, his_list, data):
        """
        追加每个位置时刻的历史数据
        @param his_list:
        @param data:
        @return:
        """
        # 如果历史记录为0 或者 新增数据和最后的历史数据不相同，则添加
        if len(his_list) == 0 or \
                np.sum(data == his_list[-1]) < len(data):
            his_list.append(data.copy())

    def __record_history(self):
        """
        记录每个位置时刻的历史数据
        @return:
        """
        # 如果历史记录数超过了保留数量，则截断，只保留 __his_reserved_num 数量的历史
        if len(self.__his_pos) > self.__his_reserved_num:
            self.__his_pos = self.__his_pos[len(self.__his_pos) - self.__his_reserved_num:]
            self.__his_vel = self.__his_vel[len(self.__his_vel) - self.__his_reserved_num:]
            self.__his_acc = self.__his_acc[len(self.__his_acc) - self.__his_reserved_num:]

        # 追加历史记录(位置、速度、加速度)
        self.__append_history(self.__his_pos, self.position)
        self.__append_history(self.__his_vel, self.velocity)
        self.__append_history(self.__his_acc, self.acceleration)
        # print(self.name, "his pos->", self.__his_pos)

    def his_position(self):
        """
        历史位置
        @return:
        """
        return self.__his_pos

    def his_velocity(self):
        """
        历史瞬时速度
        @return:
        """
        return self.__his_vel

    def his_acceleration(self):
        """
        历史瞬时加速度
        @return:
        """
        return self.__his_acc

    @property
    def mass(self):
        """
        对象质量 (单位：kg)
        @return:
        """
        return self.__mass

    @property
    def density(self):
        """
        平均密度 (单位：kg/m³)
        @return:
        """
        return self.__density

    def __repr__(self):
        return '<%s(%s)> m=%.3e(kg), d=%.3e(kg/m³), p=[%.3e,%.3e,%.3e](km), v=%s(km/s)' % \
               (self.name, self.__class__.__name__, self.mass, self.density,
                self.position[0], self.position[1], self.position[2], self.velocity)

    def ignore_gravity_with(self, body):
        """
        是否忽略指定对象的引力
        @param body:
        @return:
        """
        if len(self.gravity_only_for) > 0:
            if body in self.gravity_only_for:
                return False
            return True
        # TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在对象物理学中是不严谨）
        if self.ignore_mass:
            return True

        return False

    def position_au(self):
        """
        获取对象的位置（单位：天文单位 A.U.）
        @return:
        """
        pos = self.position
        pos_au = pos / AU
        return pos_au

    # def change_velocity(self, dv):
    #     self.velocity += dv
    #
    # def move(self, dt):
    #     self.position += self.velocity * dt

    def reset(self):
        """
        重新设置初始速度和初始位置
        @return:
        """
        self.position = copy.deepcopy(self.init_position)
        self.velocity = copy.deepcopy(self.init_velocity)

    # def kinetic_energy(self):
    #     """
    #     计算动能(千焦耳)
    #     表示动能，单位为焦耳j，m为质量，单位为千克，v为速度，单位为米/秒。
    #     ek=(1/2).m.v^2
    #     m(kg) v(m/s) -> j
    #     m(kg) v(km/s) -> kj
    #     """
    #     v = self.velocity
    #     return 0.5 * self.mass * (v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

    @staticmethod
    def build_objs_from_json(json_file):
        """
        JSON文件转为对象对象
        @param json_file:
        @return:
        """
        bodies = []
        params = {}
        from bodies import FixedStar, Body
        with open(json_file, "r", encoding='utf-8') as read_content:
            json_data = json.load(read_content)
            for body_data in json_data["bodies"]:
                try:
                    body_data = Obj.exp(body_data)  # print(body_data)
                except Exception as e:
                    err_msg = f"{json_file} 格式错误：" + str(e)
                    raise Exception(err_msg)
                is_fixed_star = False
                if "is_fixed_star" in body_data:
                    if body_data["is_fixed_star"]:
                        is_fixed_star = True
                if is_fixed_star:
                    body_data.pop("is_fixed_star")
                    body = FixedStar(**body_data)
                else:
                    has_rings = False
                    if "has_rings" in body_data:
                        if body_data["has_rings"]:
                            has_rings = True
                            body_data.pop("has_rings")

                    if "rotation_speed" in body_data:
                        body = Body(**body_data)
                        if has_rings:
                            body.has_rings = True
                    else:
                        body_data.pop("rotation_speed")
                        body_data.pop("is_fixed_star")
                        body = Obj(**body_data)

                # [x, y, z]->[-y, z, x]
                # body.init_velocity = [-body.init_velocity[1],body.init_velocity[2],body.init_velocity[0]]
                # body.init_position = [-body.init_position[1],body.init_position[2],body.init_position[0]]
                bodies.append(body)
            if "params" in json_data:
                params = json_data["params"]
                # print(body.position_au())
        return bodies, params

    @staticmethod
    def exp(body_data):
        """
        进行表达式分析，将表达式改为eval执行后的结果
        @param body_data:
        @return:
        """
        #
        for k in body_data.keys():
            v = body_data[k]
            if isinstance(v, str):
                if v.startswith("$exp:"):
                    exp = v[5:]
                    body_data[k] = eval(exp)
            elif isinstance(v, list):
                for idx, item in enumerate(v):
                    if isinstance(item, str):
                        if item.startswith("$exp:"):
                            exp = item[5:]
                            v[idx] = eval(exp)

        return body_data


if __name__ == '__main__':
    # build_bodies_from_json('../data/sun.json')
    objs, params = Obj.build_objs_from_json('../data/sun_earth.json')

    for obj in objs:
        print(obj)
