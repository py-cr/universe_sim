# -*- coding:utf-8 -*-
# title           :带有云层地球模拟
# description     :带有云层地球模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    带有云层地球模拟
    """
    earth = Earth(texture="earth_hd.jpg",
                  init_position=[0, 0, 0], init_velocity=[1, 0, 0],
                  size_scale=1)
    clouds = Earth(name="地球云层", texture="transparent_clouds.png",  # 纹理图使用了透明云层的图片
                   size_scale=1.01, show_name=False, parent=earth)  # size_scale 要稍微比

    bodies = [earth, clouds]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2, position=(0, 0, -20000),
               # cosmic_bg="textures/cosmic1.jpg",
               view_closely=0.001)
