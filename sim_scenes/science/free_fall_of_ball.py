# -*- coding:utf-8 -*-
# title           :自由落地模拟
# description     :自由落地模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from objs import Football
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_MINUTE
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    自由落地模拟
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    # e.raduis = 6373.22
    # math.sqrt(pow(6373.22 + 500, 2) + pow(500, 2))-6373.22
    # math.sqrt(pow(6373.22 + 1000, 2) + pow(500, 2))-6373.22
    # 创建的3个不同质量，不同高度的物体，观察地球表面上的加速度
    bodies = [
        earth,
        Football(mass=500, size_scale=3e2, trail_color=[255, 0, 0],
                 init_position=[-500, earth.raduis + 500, 0],  # 球在地面上 518 多公里（向左偏移500公里）
                 init_velocity=[0, 0, 0], gravity_only_for=[earth]),
        Football(mass=1000, size_scale=3e2, trail_color=[0, 255, 0],
                 init_position=[0, earth.raduis + 800, 0],  # 球在地面上 800 多公里
                 init_velocity=[0, 0, 0], gravity_only_for=[earth]),
        Football(mass=5000, size_scale=3.8e2, trail_color=[0, 0, 255],
                 init_position=[500, earth.raduis + 1000, 0],  # 球在地面上 1016 多公里（向右偏移500公里）
                 init_velocity=[0, 0, 0], gravity_only_for=[earth]),
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_MINUTE,  # 一秒相当于一分钟
               position=(0, earth.raduis + 500, -4500),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
