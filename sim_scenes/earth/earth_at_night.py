# -*- coding:utf-8 -*-
# title           :地球晚上模拟运行
# description     :地球晚上模拟运行
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth
from common.consts import SECONDS_PER_HOUR
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    地球晚上模拟运行
    图片来源：
    https://www.nasa.gov/mission_pages/NPP/news/earth-at-night.html
    https://www.nasa.gov/sites/default/files/images/712130main_8246931247_e60f3c09fb_o.jpg
    """
    resolution = 50
    # resolution = 500
    # TODO: ignore_mass=True
    #  注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
    bodies = [
        Earth(texture="earth_at_night_hd.jpg",
              init_position=[0, 0, 0], init_velocity=[0, 0, 0],
              size_scale=100, ignore_mass=True).set_resolution(resolution),
        # Earth(texture="earth_hd.jpg",
        #       init_position=[-10, 0, 0], init_velocity=[0, 0, 0],
        #       size_scale=100, ignore_mass=True).set_resolution(resolution)
    ]
    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(0, 120000, -2000000),
               show_grid=False)
