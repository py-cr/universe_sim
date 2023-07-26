# -*- coding:utf-8 -*-
# title           :三体场景模拟02
# description     :三体场景模拟（3个太阳、1个地球）
# author          :Python超人
# date            :2023-07-26
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth
from common.consts import SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, mpl_run, ursina_run

if __name__ == '__main__':
    """
    注释： 3个太阳
    可以修改影响效果的参数为： 
    1、三个方向的初始位置 init_position[x, y, z]
    2、三个方向的初始速度 init_velocity[x, y, z]
    3、天体质量 mass    
    """
    # 代码案例如下：
    SIZE_SCALE = 5e1  # 生成的太阳放大 50 倍
    RUN_DIAMETER = 1.392e6  # 真实太阳的直径
    velocity_rate = 22
    bodies = [
        Sun(name="太阳1", mass=1e30, color=(111, 140, 255), rotation_speed=0.1,
            init_position=[-100 * RUN_DIAMETER, 0, 0],
            init_velocity=[0.347113 * velocity_rate, 0.532727 * velocity_rate, 0],
            size_scale=SIZE_SCALE, texture="fixed_star.png"),
        Sun(name="太阳2", mass=1e30, color=(250, 195, 47), rotation_speed=0.1,
            init_position=[100 * RUN_DIAMETER, 0, 0],
            init_velocity=[0.347113 * velocity_rate, 0.532727 * velocity_rate, 0],
            size_scale=SIZE_SCALE, texture="fixed_star.png"),
        Sun(name="太阳3", mass=1e30, color=(198, 29, 3), rotation_speed=0.1,
            init_position=[0, 0, 0],
            init_velocity=[-0.694226 * velocity_rate, -1.065454 * velocity_rate, 0],
            size_scale=SIZE_SCALE, texture="fixed_star.png"),
    ]

    # TODO: 开启3D摄像机
    from simulators.ursina.entities.camera3d import Camera3d

    # 3D摄像机初始化(眼睛的距离为1000公里效果)
    Camera3d.init(eye_distance=5000000)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK * 3, position=(1.5 * AU, 0, -5 * AU), show_trail=True)
