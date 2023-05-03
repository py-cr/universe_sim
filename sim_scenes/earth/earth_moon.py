# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟（月球对地球的扰动）
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth, Moon
from common.consts import SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    月球对地球的扰动
    """
    OFFSETTING = 0
    # TODO: 可以抵消月球带动地球的力，保持地球在原地
    # OFFSETTING = 0.01265

    earth = Earth(init_position=[0, 0, 0],
                  init_velocity=[OFFSETTING, 0, 0], size_scale=0.5e1)  # 地球放大 5 倍，距离保持不变
    moon = Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
                init_velocity=[-1.03, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变

    earth.rotation_speed /= 50  # 地球的转速降低50倍

    bodies = [earth, moon]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK,
               position=(0, 100000, -1000000),
               show_trail=True)
