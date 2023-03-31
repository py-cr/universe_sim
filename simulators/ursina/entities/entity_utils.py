# -*- coding:utf-8 -*-
# title           :ursina entity 工具
# description     :ursina entity 工具
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import Ursina, window, Entity, Mesh, SmoothFollow, Texture, clamp, time, \
    camera, color, mouse, Vec2, Vec3, Vec4, Text, \
    load_texture, held_keys, destroy, PointLight

from simulators.ursina.entities.body_trail import BodyTrail
from simulators.ursina.ursina_config import UrsinaConfig
from common.color_utils import adjust_brightness, conv_to_vec4_color, get_inverse_color
from simulators.ursina.ursina_mesh import create_torus
from common.func import find_file
import math
import numpy as np


def create_name_text(parent):
    """

    @param parent:
    @return:
    """
    b_color = parent.body_view.color
    parent.name_text = Text(parent.body_view.body.name, scale=1, billboard=True, parent=parent,
                            font=UrsinaConfig.CN_FONT, background=True,
                            origin=(0, 0))
    parent.name_text.background.color = color.rgba(b_color[0], b_color[1], b_color[2], 0.3)
    # self.name_text.scale = self.scale
    inverse_color = get_inverse_color(b_color)
    parent.name_text.color = color.rgba(inverse_color[0], inverse_color[1], inverse_color[2], 1)
    return parent.name_text


def trail_init(parent):
    """
    拖尾球体的初始化
    :return:
    """
    # 存放拖尾球体
    parent.trails = {}

    # 根据天体的颜色获取拖尾的颜色
    trail_color = conv_to_vec4_color(parent.body_view.body.trail_color)
    trail_color = adjust_brightness(trail_color, 0.4)
    parent.trail_color = color.rgba(trail_color[0], trail_color[1], trail_color[2], 0.6)
    # 拖尾球体的大小为该天体的 1/5
    parent.trail_scale = parent.scale_x / 5
    if parent.trail_scale < 1:
        # 如果太小，则
        pass


def distance_between_two_points(point_a: Vec3, point_b: Vec3) -> float:
    """

    @param point_a:
    @param point_b:
    @return:
    """
    # 计算两点在 x、y、z 三个坐标轴上的差值
    diff_x = point_a.x - point_b.x
    diff_y = point_a.y - point_b.y
    diff_z = point_a.z - point_b.z

    # 计算两点之间的距离
    distance = math.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)

    return distance


def create_trails(parent):
    """
    创建拖尾
    :return:
    """
    # 当前天体的位置
    try:
        pos = parent.position
    except Exception as e:
        print(parent.body_view.body)
        parent.destroy_all()
        return
    trails_keys = parent.trails.keys()
    # 如果有拖尾
    if len(trails_keys) > 0:
        # 获取最后一个拖尾的位置
        last_key = list(trails_keys)[-1]
        last_pos = parent.trails[last_key]
        # 获取拖尾与当前天体的位置
        last_pos_distance = distance_between_two_points(pos, last_pos)
        self_pos_distance = distance_between_two_points(pos, parent.position)
        # # 如果拖尾在天体的内部也不要生成
        # if self_pos_distance < self.scale_x + (self.trail_scale / 2):
        #     pass
        # 如果位置比较近，就不创建拖尾了，保证拖尾间隔一定的距离
        if last_pos_distance < parent.trail_scale * 1.2:  # 间隔距离不小于1.2倍的拖尾球体
            return

    trail = create_trail(parent, pos)
    create_trail_info(parent.body, trail)
    # 创建拖尾球体，并作为字典的key，存放拖尾球体的位置
    parent.trails[trail] = pos

    # 计算拖尾球体超过的数量
    trail_overflow_count = len(parent.trails) - UrsinaConfig.trail_length

    if trail_overflow_count > 0:
        # 如果拖尾球体超过的数量，就删除之前的拖尾球体
        for entity, pos in parent.trails.items():
            destroy(entity)
            trail_overflow_count -= 1
            if trail_overflow_count <= 0:
                break


def create_trail(parent, pos):
    """
    在天体当前的位置创建一个拖尾球体
    :param pos:
    :return:
    """
    # sphere = create_sphere(1,6)  diamond sphere
    trail = BodyTrail(color=parent.trail_color, scale=parent.trail_scale, position=pos)
    trail.set_light_off()
    # trail.set_color_off()
    # trail.set_color_scale_off()
    # trail.enabled = False
    return trail


def create_rings(self):
    """
    创建行星环（使用土星贴图）
    :return:
    """
    rings_texture = 'textures/saturnRings.jpg'
    rings_texture = find_file(rings_texture)

    # 行星环偏移角度
    # self.ring_rotation_x = 80
    # 创建行星环
    # self.ring = Entity(parent=self.planet, model='circle', texture=rings_texture, scale=3.5,
    #                    rotation=(self.ring_rotation_x, 0, 0), double_sided=True)

    # 行星环偏移角度
    self.ring_rotation_x = 80
    # 创建行星环
    torus = create_torus(0.7, 1.2, 64)
    self.ring = Entity(parent=self, model=torus, texture=rings_texture, scale=1,
                       rotation=(self.ring_rotation_x, 0, 0), double_sided=True)

    # 设置行星环不受灯光影响，否则看不清行星环
    self.ring.set_light_off()


def clear_trails(self):
    """

    @param self:
    @return:
    """
    if not hasattr(self, "trails"):
        return
    # 删除拖尾
    for entity, pos in self.trails.items():
        destroy(entity)
    self.trails.clear()


def create_fixed_star_lights(parent):
    """
    创建恒星的发光的效果、并作为灯光源
    :param entity:
    :return:
    """

    # 如果是恒星（如：太阳），自身会发光，则需要关闭灯光
    parent.set_light_off()

    # lights = []
    # # 创建多个新的 Entity 对象，作为光晕的容器
    # _color = color.rgba(1.0, 0.6, 0.2, 1)
    if hasattr(parent.body_view.body, "glows"):
        # glows = (glow_num:10, glow_scale:1.03 glow_alpha:0.1~1)
        glows = parent.body_view.body.glows
        if glows is not None:
            if isinstance(glows, tuple):
                if len(glows) == 3:
                    glow_num, glow_scale, glow_alpha = glows
                elif len(glows) == 2:
                    glow_num, glow_scale = glows
                    glow_alpha = None
            else:
                glow_num = glows
                glow_scale = 1.02
                glow_alpha = None

            if glow_num > 0:
                glow_alphas = [0, 0.5, 0.4, 0.3, 0.2, 0.1]
                if glow_alpha is None:
                    if glow_num < len(glow_alphas) - 1:
                        glow_alpha = glow_alphas[glow_num]
                    else:
                        glow_alpha = glow_alphas[-1]

                # _color = color.white
                _color = parent.body_view.body.color
                _color = color.rgba(_color[0] / 255, _color[1] / 255, _color[2] / 255, 1)
                for i in range(glow_num):
                    glow_entity = Entity(parent=parent, model='sphere', color=_color,
                                         scale=math.pow(glow_scale, i + 1), alpha=glow_alpha)
    if hasattr(parent.body_view.body, "light_on"):
        if parent.body_view.body.light_on:
            for i in range(2):
                # 创建 PointLight 对象，作为恒星的灯光源
                light = PointLight(parent=parent, intensity=10, range=10, color=color.white)


def merge_vectors(vectors):
    # 计算速度的大小
    x, y, z = vectors[0], vectors[1], vectors[2]
    value = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    # 计算速度的方向
    direction = (x / value, y / value, z / value)
    # 返回速度大小和速度方向
    # return value, direction

    # return value,  (direction[1], direction[0], direction[2])
    # return value, (direction[1], direction[2], direction[0])
    return value, (-direction[1], direction[2], direction[0])


def create_trail_info(body, trail):
    velocity = merge_vectors(body.velocity)
    acceleration = merge_vectors(body.acceleration)
    vel_info = "%.2fkm/s" % (velocity[0])

    acc_m = acceleration[0] * 1000

    if acc_m >= 0.01:
        acc_info = "%.2fm/s²" % (acc_m)
    else:
        acc_info = "%.2fmm/s²" % (acc_m * 1000)


    vel_direction = velocity[1]
    vel_direction = np.array(vel_direction) * 5

    acc_direction = acceleration[1]
    acc_direction = np.array(acc_direction) * 2

    verts_acc = [(0, 0, 0), tuple(acc_direction)]
    verts_vel = [(0, 0, 0), tuple(vel_direction)]

    vel_position = vel_direction
    vel_position = (vel_position[0], vel_position[1], vel_position[2])

    acc_position = acc_direction
    acc_position = (acc_position[0], acc_position[1], acc_position[2])

    trail.entity_infos = {"velocity": [vel_info, vel_direction, vel_position],
                          "acceleration": [acc_info, acc_direction, acc_position]}


def create_trail_text_xxx(body, trail):
    velocity = merge_vectors(body.velocity)
    acceleration = merge_vectors(body.acceleration)
    vel_info = "%.2fkm/s" % (velocity[0])
    acc_m = acceleration[0] * 1000

    if acc_m >= 0.01:
        acc_info = "%.2fm/s²" % (acc_m)
    else:
        acc_info = "%.2fmm/s²" % (acc_m * 1000)

    vel_direction = velocity[1]
    vel_direction = np.array(vel_direction) * 5

    acc_direction = acceleration[1]
    acc_direction = np.array(acc_direction) * 2
    # acc_direction = np.array(acc_direction)*UrsinaConfig.SCALE_FACTOR
    # vertsyz = [tuple(body.position),tuple(acc_direction)] #  [(0, 0, 0), (0, 10, 0), (0, 0, 0), (0, 0, 10)]
    verts_acc = [(0, 0, 0), tuple(acc_direction)]
    acc_line = Entity(parent=trail, model=Mesh(vertices=verts_acc, mode='line', thickness=3),
                      color=color.yellow, alpha=0.5)
    acc_line.set_light_off()

    verts_vel = [(0, 0, 0), tuple(vel_direction)]
    vel_line = Entity(parent=trail, model=Mesh(vertices=verts_vel, mode='line', thickness=3),
                      color=color.red, alpha=0.5)
    vel_line.set_light_off()

    vel_position = vel_direction
    vel_position = (vel_position[0], vel_position[1], vel_position[2])

    vel_text = Text(vel_info, scale=50, billboard=True, parent=trail,
                    font=UrsinaConfig.CN_FONT, background=False, color=color.red,
                    position=vel_position, alpha=0.5)
    vel_text.set_light_off()
    acc_position = acc_direction
    acc_position = (acc_position[0], acc_position[1], acc_position[2])

    acc_text = Text(acc_info, scale=50, billboard=True, parent=trail,
                    font=UrsinaConfig.CN_FONT, background=False, color=color.yellow,
                    position=acc_position, alpha=0.5)
    acc_text.set_light_off()
    # self.name_text.background.color = color.rgba(b_color[0], b_color[1], b_color[2], 0.3)
    # # self.name_text.scale = self.scale
    # inverse_color = get_inverse_color(b_color)
    # self.name_text.color = color.rgba(inverse_color[0], inverse_color[1], inverse_color[2], 1)
    # acc_line.enabled = False
    # vel_line.enabled = False
    # vel_text.enabled = False
    # acc_text.enabled = False

    trail.entity_infos = [acc_line, vel_line, vel_text, acc_text]
    return acc_line, vel_line, vel_text, acc_text