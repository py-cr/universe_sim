# -*- coding:utf-8 -*-
# title           :验证万有引力（为什么旋转的球体会导致被吸引天体轨道偏转）
# description     :太验证万有引力（为什么旋转的球体会导致被吸引天体轨道偏转）
# author          :Python超人
# date            :2023-07-06
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Moon
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, AU
from sim_scenes.func import mayavi_run, ursina_run
import numpy as np


def ignore_gravity_with(body):
    if isinstance(body, Sun):
        return True

    return False

def create_circle_bodies(radius):
    bodies = []
    for i in range(0, 360, 30):
        # 当前天数的角度（弧度）
        angle = i * np.pi / 180
        # 计算月亮的坐标（这里没有用到万有引力）
        px = radius * np.cos(angle)
        pz = radius * np.sin(angle)
        body = Sun(size_scale=1e-3,
                     init_velocity=[0, 0, 0],
                     init_position=[px, 0, pz],
                     # ignore_mass=True,
                     rotation_speed=0)
        body.ignore_gravity_with = ignore_gravity_with
        bodies.append(body)
    return bodies


if __name__ == '__main__':
    """
    太阳、地球
    """
    bodies = create_circle_bodies(100000)
    bodies.append(Moon(size_scale=100,
                       init_position=[0, 0, 500000000],
                       init_velocity=[0, 0, 0],
                       # ignore_mass=True,
                       ))
    # bodies = [
    #     Sun(size_scale=5e1),  # 太阳放大 50 倍
    #     Earth(size_scale=2e3, distance_scale=1),  # 地球放大 2000 倍，距离保持不变
    # ]

    # 使用 mayavi 查看的运行效果
    # mayavi_run(bodies, SECONDS_PER_WEEK, view_azimuth=-45)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY, position=(0, 0, 0), show_trail=True)
