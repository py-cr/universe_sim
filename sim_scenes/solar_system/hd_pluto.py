# -*- coding:utf-8 -*-
# title           :高清冥王星模拟运行
# description     :高清冥王星模拟运行
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Pluto
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    高清冥王星模拟运行
    """
    bodies = [
        Pluto(texture="pluto.png",
              init_position=[0, 0, 0], init_velocity=[0, 0, 0],
              size_scale=2, show_name=True)
    ]
    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR, position=(0, 0, -9000),
               # cosmic_bg="textures/cosmic1.jpg",
               view_closely=0.001)
