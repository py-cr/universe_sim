# -*- coding:utf-8 -*-
# title           :地球和卫星模拟
# description     :地球和卫星模拟
# author          :Python超人
# date            :2023-04-09
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from objs import Satellite
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at
import math
import random

# def calculate_satellite_velocity(earth: Earth, altitude):
#     """
#
#     @param earth_raduis:
#     @param altitude:
#     @return:
#     """
#     # 地球引力常数
#     G = 6.67430e-11
#     # 地球质量
#     M = earth.mass  # 5.97e24
#     # 地球半径
#     R = earth.raduis + altitude
#     # 地球表面的线速度
#     v_surface = math.sqrt(G * M / R)
#     # 地球卫星轨道速度
#     v_satellite = math.sqrt(G * M / (R + altitude))
#     return v_satellite - v_surface

import random

import random
import math

from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


def get_satellite_position_velocity(earth_mass, earth_position, earth_radius, altitude):
    # 万有引力常数
    G = 6.6743 * 10 ** (-11)
    # 地球质量
    M = earth_mass
    # 地球半径+海拔高度
    R = earth_radius + altitude

    # 随机生成卫星的位置，确保在球面上
    phi = random.uniform(0, 2 * math.pi)
    costheta = random.uniform(-1, 1)
    u = random.uniform(0, 1)

    theta = math.acos(costheta)
    r = R * (u ** (1 / 3))

    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)

    # 计算速度的方向
    # 位置矢量
    r_vec = [x, y, z]
    # 速度方向和位置矢量垂直，采用向量叉积的性质
    v_dir = [-y, x, 0]
    # 归一化
    v_dir_norm = [v / math.sqrt(x ** 2 + y ** 2) for v in v_dir]

    # 计算速度大小
    v = math.sqrt(G * M / R)

    # 计算速度矢量
    v_vec = [v * dir for dir in v_dir_norm]

    # 计算卫星的位置和速度
    position = [earth_position[0] + x, earth_position[1] + y, earth_position[2] + z]
    velocity = v_vec

    return tuple(position), [0, 0, 0]


def generate_satellite_coordinates(earth_radius, altitude):
    theta = random.uniform(0, 2 * math.pi)  # 在0~2π内随机生成一个角度
    phi = random.uniform(0, math.pi)  # 在0~π内随机生成一个角度
    r = earth_radius + altitude  # 地球半径+海拔高度
    x = r * math.sin(phi) * math.cos(theta)  # 计算x坐标
    y = r * math.sin(phi) * math.sin(theta)  # 计算y坐标
    z = r * math.cos(phi)  # 计算z坐标

    return [x, y, z]


if __name__ == '__main__':
    """
    地球、6个月球
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    # 北斗卫星高度为2.13-2.15万千米。GPS卫星平均轨道高度2.02万千米。
    bodies = [earth]
    satellite_infos = [
        {"position": [0, 0, 10000], "velocity": [-6.3, 0, 0]},
        {"position": [0, 0, -12000], "velocity": [5.75, 0, 0]},
        {"position": [0, 8000, 0], "velocity": [7.05, 0, 0]},
        {"position": [0, -12000, 0], "velocity": [-5.75, 0, 0]},
        {"position": [0, 0, 8000], "velocity": [0, 7.05, 0]},
        {"position": [0, 0, -10000], "velocity": [0, -6.3, 0]},
    ]
    for i, info in enumerate(satellite_infos):
        # altitude = random.randint(4000, 10000)
        # position, velocity = get_satellite_position_velocity(earth.mass, earth.init_position, earth.raduis, altitude)

        satellite = Satellite(name=f'卫星{i + 1}', mass=4.4e10, size_scale=2e2, color=(255, 200, 0),
                              init_position=info["position"],
                              init_velocity=info["velocity"])
        bodies.append(satellite)


    def on_ready():
        camera_look_at(earth, rotation_z=0)
        UrsinaConfig.trail_length = 150
        UrsinaConfig.trail_type = "line"
        pass


    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(30000, 5000, -30000),
               show_trail=True,
               view_closely=0.001)
