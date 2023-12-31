# -*- coding:utf-8 -*-
# title           :天体系统
# description     :天体系统，多个天体就是一个系统
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import numpy as np
from numpy.linalg import norm
import math
from common.consts import AU, G
from bodies import Body, Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
from common.func import calculate_distance


class System(object):
    """
    天体系统
    """

    def __init__(self, bodies, max_distance=200 * AU):
        """

        @param bodies:
        @param max_distance:系统的最大范围，超出范围的天体就不显示了
        """
        self.bodies = bodies
        # self.adjust_distance_and_velocity()
        self.max_distance = max_distance

    @staticmethod
    def calc_body_new_velocity_position(body, sun_mass=1.9891e30, G=6.674e-11):
        old_velocity = body.init_velocity
        old_position = body.init_position

        old_distance = np.linalg.norm(old_position - [0, 0, 0], axis=-1)
        new_distance = old_distance * body.distance_scale
        new_position = old_position * body.distance_scale

        new_velocity = System.get_new_velocity(old_velocity, old_distance, new_distance, body.mass)

        return new_velocity, new_position

    @staticmethod
    def get_new_velocity(old_velocity, old_distance, new_distance, mass, sun_mass=1.9891e30, G=6.674e-11):
        # 计算原速度的模长
        old_speed = np.linalg.norm(old_velocity * 1000)
        # 计算原动能和原势能
        old_kinetic_energy = 0.5 * mass * old_speed ** 2
        old_potential_energy = - G * mass * sun_mass / old_distance

        new_potential_energy = - G * mass * sun_mass / new_distance

        # 计算新动能
        new_kinetic_energy = old_kinetic_energy
        # 计算新速度的模长
        new_speed = math.sqrt(2 * (new_kinetic_energy - old_potential_energy) / mass)
        # 计算新速度向量
        new_velocity = old_velocity / old_speed * new_speed / 1000
        return new_velocity

    def get_new_velocity1(old_velocity, old_distance, new_distance, mass, sun_mass=1.9891e30, G=6.674e-11):
        # 计算原来的速度
        old_speed = math.sqrt(G * sun_mass / old_distance)
        # 计算新的速度
        new_speed = math.sqrt(G * sun_mass / new_distance)
        # 计算原来的动能
        old_kinetic_energy = 0.5 * mass * old_velocity ** 2
        # 计算新的动能
        new_kinetic_energy = old_kinetic_energy * new_speed ** 2 / old_speed ** 2
        # 计算新的速度
        new_velocity = math.sqrt(2 * new_kinetic_energy / mass)
        return new_velocity

    def add(self, body):
        self.bodies.append(body)

    def total_mass(self):
        """
        总质量
        @return:
        """
        total_mass = 0.0
        for body in self.bodies:
            total_mass += body.mass
        return total_mass

    def __repr__(self):
        return 'System({})'.format(self.bodies)

    def center_of_mass(self):
        """
        质心
        @return:
        """
        r = np.zeros(2)
        for body in self.bodies:
            r = body.mass * body.position
        return r / self.total_mass()

    def evolve(self, dt):
        """

        @param dt:
        @return:
        """
        self.calc_bodies_acceleration()

        for body in self.bodies:
            # acceleration 加速度
            body.velocity += body.acceleration * dt
            # body.position += 0.5 * body.acceleration * (dt ** 2)
            body.position += body.velocity * dt

    def save_to_json(self, json_file_name, params=None):
        """

        @param json_file_name:
        @param params:
        @return:
        """
        import json
        import os
        # json_file = os.path.join("../data", json_file_name)
        filed_names = ["name", "mass", "init_position", "init_velocity",
                       "density", "color", "texture",
                       "size_scale", "distance_scale",  # "parent"
                       "rotation_speed", "ignore_mass", "is_fixed_star", "trail_color"]
        bodies = []
        for b in self.bodies:
            body = {}
            for filed_name in filed_names:
                filed_value = getattr(b, filed_name)
                if type(filed_value) is np.ndarray:
                    filed_value = filed_value.tolist()
                body[filed_name] = filed_value
            bodies.append(body)
        data = {"bodies": bodies}
        if params is not None:
            data["params"] = params
        json_str = json.dumps(data, indent=2, ensure_ascii=False, separators=(',', ': '))
        with open(json_file_name, "w", encoding='utf-8') as f:
            f.write(json_str)

    def fast_calc(self):
        """
        快速计算（对于天体过多会导致性能急速下降，这样就需要使用快速算法）
        @return: 如果为True，则快速计算成功
        """
        # return False
        if not hasattr(self, "fast_calc_list"):
            return False
        if len(self.fast_calc_list) == 0:
            return

        for body1 in self.fast_calc_list.keys():
            acceleration = np.zeros(3)
            for body2 in self.fast_calc_list[body1]:
                r = body2.position - body1.position
                if np.linalg.norm(r) > 0.0:
                    acceleration += (G * body2.mass * r / np.linalg.norm(r) ** 3) / 1e9
            body1.acceleration = acceleration
        return True

    def calculate_gravitational_accelerations_np(self, masses, positions):
        '''Params:
        - positions: numpy array of size (n,3)
        - masses: numpy array of size (n,)
        '''
        masses = np.array(masses)
        positions = np.array(positions)
        mass_matrix = masses.reshape((1, -1, 1)) * masses.reshape((-1, 1, 1))
        disps = positions.reshape((1, -1, 3)) - positions.reshape((-1, 1, 3))  # displacements
        dists = norm(disps, axis=2)
        dists[dists == 0] = 1  # Avoid divide by zero warnings
        forces = G * disps * mass_matrix / np.expand_dims(dists, 2) ** 3
        return forces.sum(axis=1) / masses.reshape(-1, 1)

    def calculate_gravitational_accelerations_cp(self, masses, positions):
        '''Params:
         - positions: numpy array of size (n,3)
         - masses: numpy array of size (n,)
         pip install -i https://pypi.douban.com/simple/ cupy

 nvcc -V
 nvcc: NVIDIA (R) Cuda compiler driver
 Copyright (c) 2005-2021 NVIDIA Corporation
 Built on Fri_Dec_17_18:28:54_Pacific_Standard_Time_2021
 Cuda compilation tools, release 11.6, V11.6.55
 Build cuda_11.6.r11.6/compiler.30794723_0

 pip install -i https://pypi.douban.com/simple/ cupy-cuda116
 cupy-11.6.0.tar.gz
 https://pypi.doubanio.com/packages/70/e1/acc77e327548cce7cb28eb345b7f31ab85b6a3d99214479f9bcbe78e6e9b/cupy_cuda116-10.6.0-cp39-cp39-win_amd64.whl
 https://pypi.doubanio.com/packages/e3/62/c808623b8000185efebd8b4542efdf76cc93d20dfd3f0a3eaeb5e5697430/cupy-11.6.0.tar.gz#sha256=53dbb840072bb32d4bfbaa6bfa072365a30c98b1fcd1f43e48969071ad98f1a7

         '''
        import cupy as cp
        masses = cp.array(masses)
        positions = cp.array(positions)
        mass_matrix = masses.reshape((1, -1, 1)) * masses.reshape((-1, 1, 1))
        disps = positions.reshape((1, -1, 3)) - positions.reshape((-1, 1, 3))  # displacements
        dists = cp.linalg.norm(disps, axis=2)
        dists[dists == 0] = 1  # Avoid divide by zero warnings
        forces = G * disps * mass_matrix / cp.expand_dims(dists, 2) ** 3
        accelerations = forces.sum(axis=1) / masses.reshape(-1, 1)
        return accelerations.get()

    def calculate_gravitational_accelerations(self, masses, positions):
        return self.calculate_gravitational_accelerations_np(masses, positions)

    def calc_bodies_acceleration_high_performance(self):
        """
        计算加速度(使用矩阵的方式，性能提高很多，不支持指定重力对某天体有效)
        @return:
        """
        valid_bodies = list(filter(lambda b: not b.ignore_mass, self.bodies))
        masses = []
        positions = []
        for body in valid_bodies:
            masses.append(body.mass)
            positions.append(body.position * 1000)

        accelerations = self.calculate_gravitational_accelerations(masses, positions)

        for idx, body in enumerate(valid_bodies):
            body.acceleration = accelerations[idx] / 1000

    def calc_bodies_acceleration(self):
        """
        计算加速度（性能非常低）
        @return:
        """

        if len(self.bodies) > 30:
            self.calc_bodies_acceleration_high_performance()
            return

        # 如果快速计算成功，则无需再计算
        if self.fast_calc():
            return

        def valid_body(body):
            """
            判断是否为有效的天体
            @param body:
            @return:
            """
            if not body.appeared:  # 不显示
                return False
            # if self.max_distance > 0:
            #     # 超过了 max_distance 距离，则不显示，并消失
            #     if calculate_distance(body.position) > self.max_distance:
            #         body.appeared = False
            #         return False

            return True

        # self.bodies = list(filter(valid_body, self.bodies))
        valid_bodies = list(filter(lambda b: not b.ignore_mass, self.bodies))

        # 如果需要计算的天体超过了10个，则启用快速算法
        if len(valid_bodies) > 10:
            if not hasattr(self, "fast_calc_list"):
                self.fast_calc_list = {}

        for body1 in valid_bodies:
            # if body1.ignore_mass:
            #     continue
            if not valid_body(body1):
                continue
            acceleration = np.zeros(3)
            for body2 in valid_bodies:
                # if body2.ignore_mass:
                #     continue
                if self.max_distance > 0:
                    if calculate_distance(body1.position) > self.max_distance:  # 超过了max_distance距离，则消失
                        body1.appeared = False
                    if calculate_distance(body2.position) > self.max_distance:  # 超过了max_distance距离，则消失
                        body2.appeared = False

                if not body1.appeared or not body2.appeared:
                    continue

                if body1 is body2:
                    continue
                elif body1.ignore_gravity_with(body2) or body2.ignore_gravity_with(body1):
                    continue

                if hasattr(self, "fast_calc_list"):
                    #  构建快速计算列表
                    if body1 not in self.fast_calc_list:
                        self.fast_calc_list[body1] = []
                    # 如果 body2 质量太小了，与 body1 悬殊太大，加速度可以忽略不计
                    if body1.mass / body2.mass < 1e10:  # 10亿倍的差距
                        self.fast_calc_list[body1].append(body2)
                    else:
                        # print(f"{body2.name}相对{body1.name}质量太小，加速度可以忽略不计！")
                        continue

                r = body2.position - body1.position
                # G = 6.67e-11 # 万有引力常数
                # m/s² = kg * m / m**3
                # km/s² = kg * m / m**3 / 1e9
                # acceleration = G * body2.mass * dx / (d ** 3)
                if np.linalg.norm(r) > 0.0:
                    acceleration += (G * body2.mass * r / np.linalg.norm(r) ** 3) / 1e9

            body1.acceleration = acceleration


if __name__ == '__main__':
    # body_sys = System([
    #     Sun(),  # 太阳
    #     Mercury(),  # 水星
    #     Venus(),  # 金星
    #     Earth(),  # 地球
    #     Mars(),  # 火星
    #     Jupiter(),  # 木星
    #     Saturn(),  # 土星
    #     Uranus(),  # 天王星
    #     Neptune(),  # 海王星
    #     Pluto()  # 冥王星(从太阳系的行星中排除)
    # ])
    # import math
    #
    # mass = 2e30
    # r = 2 * AU
    # # p = 14.9
    # p = 14.89
    # bodies = [
    #     Sun(name="太阳A红色", mass=mass,
    #         init_position=[0, r * math.sqrt(3), 0],  # 位置
    #         init_velocity=[-p, 0, 0],  # 速度（km/s）
    #         size_scale=5e1, texture="sun2.jpg", color=(255, 0, 0)),  # 太阳放大 100 倍
    #     Sun(name="太阳B绿色", mass=mass,
    #         init_position=[-r, 0, 0],
    #         init_velocity=[1 / 2 * p, -math.sqrt(3) / 2 * p, 0],
    #         size_scale=5e1, texture="sun2.jpg", color=(0, 255, 0)),  # 太阳放大 100 倍
    #     Sun(name="太阳C蓝色", mass=mass,
    #         init_position=[r, 0, 0],
    #         init_velocity=[1 / 2 * p, math.sqrt(3) / 2 * p, 0],
    #         size_scale=5e1, texture="sun2.jpg", color=(0, 0, 255)),  # 太阳放大 100 倍
    #     Earth(name="地球",
    #           # init_position=[0, -AU * -2, 5 * AU],
    #           init_position=[0, math.sqrt(3) * r / 6, 5 * AU],
    #           init_velocity=[0, 0, -10],
    #           size_scale=4e3, distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    # ]
    # body_sys = System(bodies)
    # print(body_sys.save_to_json("../data/tri_bodies_sim_perfect_01.json"))
    earth = Earth(name="地球",
                  # init_position=[0, -AU * -2, 5 * AU],
                  init_position=[0, 1000000, 500000],
                  init_velocity=[0, 0, -10],
                  size_scale=4e3, distance_scale=1)
    new_velocity, new_position = System.calc_body_new_velocity_position(earth)

    print(new_velocity, new_position)
    print(earth.init_velocity, earth.init_position)
