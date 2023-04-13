# -*- coding:utf-8 -*-
# title           :太阳、地球、木星场景模拟
# description     :太阳、地球、木星场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Jupiter
from bodies.jupiter_system import Io, Europa, Ganymede, Callisto
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, AU
from sim_scenes.func import mayavi_run, ursina_run

if __name__ == '__main__':
    """
    太阳、地球、木星
    """
    bodies = [
        Io(size_scale=1e1),
        Europa(size_scale=1e1),
        Ganymede(size_scale=1e1),
        Callisto(size_scale=1e1),
        Jupiter(size_scale=1, init_velocity=[0, 0, 0], init_position=[0, 0, 0]),  # 木星放大 500 倍，距离保持不变
    ]

    # 使用 mayavi 查看的运行效果
    # mayavi_run(bodies, SECONDS_PER_WEEK, view_azimuth=-45)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR, position=(0, 0, -AU/100), show_trail=True, view_closely=True)
