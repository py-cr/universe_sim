# -*- coding:utf-8 -*-
# title           :三体场景模拟01
# description     :三体场景模拟（3个太阳、1个地球）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_YEAR, SECONDS_PER_MONTH, AU
from sim_scenes.func import mayavi_run, ursina_run

if __name__ == '__main__':
    """
    3个太阳、1个地球（效果1）
    可以修改影响效果的参数为： 
    1、三个方向的初始位置 init_position[x, y, z]
    2、三个方向的初始速度 init_velocity[x, y, z]
    3、天体质量 mass    
    """
    bodies = [
        Sun(mass=1.5e30, init_position=[849597870.700, 0, 0], init_velocity=[0, 7.0, 0],
            size_scale=5e1, texture="sun2.jpg"),  # 太阳放大 50 倍
        Sun(mass=2e30, init_position=[0, 0, 0], init_velocity=[0, -8.0, 0],
            size_scale=5e1, texture="sun2.jpg"),  # 太阳放大 50 倍
        Sun(mass=2.5e30, init_position=[0, -849597870.700, 0], init_velocity=[18.0, 0, 0],
            size_scale=5e1, texture="sun2.jpg"),  # 太阳放大 50 倍
        Earth(init_position=[0, -349597870.700, 0], init_velocity=[15.50, 0, 0],
              size_scale=4e3, distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    ]
    # 使用 mayavi 查看的运行效果
    # mayavi_run(bodies, SECONDS_PER_WEEK, view_azimuth=0)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_YEAR, position=(20 * AU, 0, -40 * AU), show_trail=True)