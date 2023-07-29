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

from bodies import FixedStar, Body
from simulators.ursina.ursina_event import UrsinaEvent


class BlackHole(FixedStar):
    def __init__(self, name="黑洞", mass=1.9891e35,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 color=(0, 0, 0),
                 # texture="cosmic3.jpg",  # 虫洞
                 texture="",  # 黑洞
                 size_scale=1.0, distance_scale=1.0,
                 rotation_speed=0.6130, ignore_mass=False, trail_color=None, show_name=False):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": 1.408e20,
            "color": color,
            "texture": texture,
            "size_scale": size_scale * 10000,
            "distance_scale": distance_scale,
            "rotation_speed": rotation_speed,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name
        }
        super().__init__(**params)
        # self.glows = (0, 1.015, 0.08, (255, 255, 255))


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
        BlackHole(init_position=[-100 * RUN_DIAMETER, 100 * RUN_DIAMETER, 0], size_scale=SIZE_SCALE)
    ]

    # TODO: 开启3D摄像机
    from simulators.ursina.entities.camera3d import Camera3d

    # 3D摄像机初始化(两眼到鼻梁的距离为1000公里效果)
    # Camera3d.init(eye_distance=5000000)

    def on_ready():
        from ursina import window
        window.size = (3840, 1920)
        # 黑色背景的宇宙背景
        # SphereSky(texture='../../textures/bg_black.png')

    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, 3, position=(1.5 * AU, 0, -5 * AU), show_trail=True)
