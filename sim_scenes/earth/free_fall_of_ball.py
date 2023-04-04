# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import mayavi_run, ursina_run

if __name__ == '__main__':
    """
    地球、6个月球
    """
    # 地球在中心位置
    e = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    bodies = [
        e,
        Moon(name='小球', mass=4.4e18, init_position=[0, e.raduis + 500, 0], init_velocity=[0, 0, 0]),  # 球在地球上面500km
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, 60, position=(0, e.raduis + 500, -4500), show_trail=True, view_closely=0.001)
