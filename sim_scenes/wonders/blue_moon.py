# -*- coding:utf-8 -*-
# title           :地球年月的关系
# description     :地球年月的关系
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at, set_camera_parent
from bodies.body import AU
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
import numpy as np

sky, moon, moon_blue = None, None, None
if __name__ == '__main__':
    """
    地球年月的关系
    """
    resolution = 100
    # sun = Sun(name="太阳", size_scale=1e2)  # 太阳放大 100 倍，距离保持不变
    # earth = Earth(name="地球", size_scale=1.8e3)  # 地球放大 1800 倍，距离保持不变
    # earth_moon_d = 20000000  # 因为地球放大 1800 倍，为了较好的效果，地月距离要比实际大才行
    moon = Moon(name="月球", size_scale=9.002e3,  # 月球球放大 3000 倍，为了较好的效果，地月距离要比实际大
                init_position=[0, 0, 0],
                init_velocity=[0, 0, 0],
                rotation_speed=0,
                ignore_mass=True,
                ).set_resolution(resolution)

    moon_blue = Moon(name="月球", size_scale=9.00e3,  # 月球球放大 3000 倍，为了较好的效果，地月距离要比实际大
                     init_position=[0, 0, 0],
                     init_velocity=[0, 0, 0],
                     rotation_speed=0,
                     texture='moon_blue.jpg',
                     ignore_mass=True,
                     ).set_resolution(resolution)
    bodies = [
        # sun, earth,
        moon, moon_blue
    ]


    def on_timer_changed(time_data: TimeData):
        global sky, moon, moon_blue
        from ursina import camera
        if sky is not None:
            sky.rotation_y += 0.005
            sky.rotation_x += 0.005

        opacity = round((time_data.total_hours - 1) / 10, 2)

        if opacity > 1.0:
            opacity = 1.0
        elif opacity < 0.0:
            opacity = 0.0

        if opacity >= 1.0:
            moon.planet.enabled = False  # 原火星完全消失

        moon.planet.alpha = 1 - opacity  # 原火星渐渐消失


    def on_ready():
        global sky, moon, moon_blue
        camera_look_at(moon)
        from ursina import camera
        from simulators.ursina.entities.sphere_sky import SphereSky
        from common.image_utils import find_texture
        sky_texture = find_texture("bg_pan.jpg", None)
        sky = SphereSky(texture=sky_texture)
        sky.scale = 800
        sky.rotation_y = 90
        camera.fov = 65
        pass


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    # position=(0, 0, 0) 的位置是站在地球视角，可以观看月相变化的过程
    ursina_run(bodies,
               SECONDS_PER_HOUR / 2,
               # SECONDS_PER_DAY / 10,
               cosmic_bg='',
               show_grid=False,
               position=(0, AU / 2, 0),
               show_control_info=False,
               show_camera_info=False,
               show_timer=False,
               timer_enabled=True
               )
