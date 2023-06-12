# -*- coding:utf-8 -*-
# title           :太阳和史蒂文森2-18
# description     :太阳和史蒂文森2-18
# author          :Python超人
# date            :2023-06-10
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Stephenson_2_18
from bodies import Sun, Earth
from bodies.body import AU
from common.consts import SECONDS_PER_WEEK
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    太阳和史蒂文森2-18
    """
    # 构建恒星天体对象
    SIZE_SCALE = 0.5  # 所有天体尺寸缩放保持一致
    # TODO: ignore_mass=True
    #  注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
    bodies = [
        Earth(size_scale=SIZE_SCALE, ignore_mass=True,
              init_position=[-2896.9165, 2896.9165, 0]),
        Sun(size_scale=SIZE_SCALE, ignore_mass=True,
            init_position=[-316397.06, 316397.06, 386345.72]),  # 太阳
        Stephenson_2_18(size_scale=SIZE_SCALE,
                        color=(28, 2, 1),
                        ignore_mass=True,
                        init_position=[-10e+08, 6.802537e+08, 8.234898e+08])  # 史蒂文森2-18 质量倍数 40.0   半径倍数 2150
    ]

    # 循环为每个恒星的初始位置进行赋值，方便演示
    for idx, body in enumerate(bodies):
        body.rotation_speed /= 10  # 恒星的旋转速度减小10倍
        if body.is_fixed_star:
            body.light_on = False  # 关闭灯光效果
        # 所有天体的初始速度为 0
        body.init_velocity = [0, 0, 0]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    #             M：摄像机移动加速  N:摄像机移动减速
    # position = (左-右+、上+下-、前+后-)
    ursina_run(bodies, SECONDS_PER_WEEK,
               position=(0, 30000, -AU / 500),
               show_grid=False,
               show_name=True, bg_music="sounds/universe_03.mp3")
