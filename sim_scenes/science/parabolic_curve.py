# -*- coding:utf-8 -*-
# title           :抛物线模拟
# description     :抛物线模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_MINUTE
from sim_scenes.func import ursina_run, get_vector2d_velocity

if __name__ == '__main__':
    """
    抛物线模拟
    """
    # TODO: 修改抛出物体的速度
    velocity = 8  # 物体飞不出地球太远，就落地
    # velocity = 10  # 物体能飞出地球很远，但还是无法摆脱地球引力
    # velocity = 11.2  # 脱离地球引力直接飞出。速度11.2千米/秒为脱离地球引力的速度叫第二宇宙速度

    # 根据速度、角度获取矢量速度（vx、vy） -> vx² + vy² = velocity²
    vx, vy = get_vector2d_velocity(velocity, angle=10)

    # 地球在中心位置
    e = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    bodies = [
        e,
        Moon(name='小月球', mass=500, size_scale=2e6,
             init_position=[0, e.raduis + 300, 0],  # 在地球表面上
             init_velocity=[vx, vy, 0]),
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,  # 一秒相当于半个小时
               position=(0, 0, -45000),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
