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
    e = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    bodies = [
        e,
        Football(mass=500, size_scale=3e2, trail_color=[255, 0, 0],
                 init_position=[-500, e.raduis + 500, 0],  # 球在地面上 500km
                 init_velocity=[0, 0, 0]),
        Football(mass=5000, size_scale=3.8e2,
                 init_position=[500, e.raduis + 1000, 0],  # 球在地面上 500km
                 init_velocity=[0, 0, 0]),
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_MINUTE,  # 一秒相当于一分钟
               position=(0, e.raduis + 500, -4500),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
