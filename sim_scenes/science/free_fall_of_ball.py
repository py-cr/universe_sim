# -*- coding:utf-8 -*-
# title           :自由落地模拟
# description     :自由落地模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth, Body
from objs import Football
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_MINUTE
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    自由落地模拟
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                  size_scale=1, texture="earth_hd.jpg")
    # earth.raduis = 6373.22
    # 创建的3个不同质量，不同高度的球，观察这3个球打到地球表面上的加速度
    ball_1 = Football(mass=500, size_scale=2.65e2, trail_color=[255, 0, 0],
                      # 球在地面上 518 多公里处
                      # 518 = sqrt[(earth.raduis + 500)² + (-500)²] - earth.raduis
                      init_position=[-500, earth.raduis + 500, 0],
                      init_velocity=[0, 0, 0], gravity_only_for=[earth])
    ball_2 = Football(mass=1000, size_scale=3.3e2, trail_color=[0, 255, 0],
                      # 球在地面上 800 多公里处
                      init_position=[0, earth.raduis + 800, 0],
                      init_velocity=[0, 0, 0], gravity_only_for=[earth])
    ball_3 = Football(mass=5000, size_scale=3.8e2, trail_color=[0, 0, 255],
                      # 球在地面上 1016 多公里处
                      # 1016 = sqrt[(earth.raduis + 1000)² + 500²] - earth.raduis
                      init_position=[500, earth.raduis + 1000, 0],
                      init_velocity=[0, 0, 0], gravity_only_for=[earth])

    bodies = [earth, ball_1, ball_2, ball_3]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_MINUTE,  # 一秒相当于一分钟
               position=(0, earth.raduis + 500, -4500),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
