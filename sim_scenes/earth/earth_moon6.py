# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    地球、6个月球
    """
    # 地球在中心位置
    e = Earth(init_position=[0, 0, 0], texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    # 在地球周围创建 6 个月球（初速度为0）
    bodies = [
        e,
        Moon(init_position=[e.diameter, 0, 0], init_velocity=[0, 0, 0]),  # 月球在地球右面
        Moon(init_position=[-e.diameter, 0, 0], init_velocity=[0, 0, 0]),  # 月球在地球左面
        Moon(init_position=[0, e.diameter, 0], init_velocity=[0, 0, 0]),  # 月球在地球上面
        Moon(init_position=[0, -e.diameter, 0], init_velocity=[0, 0, 0]),  # 月球在地球下面
        Moon(init_position=[0, 0, e.diameter], init_velocity=[0, 0, 0]),  # 月球在地球前面
        Moon(init_position=[0, 0, -e.diameter], init_velocity=[0, 0, 0]),  # 月球在地球后面
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 10,
               position=(0, 0, -4 * e.diameter),
               show_trail=True,
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001
