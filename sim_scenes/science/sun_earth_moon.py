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

if __name__ == '__main__':
    """
    地球年月的关系
    """
    sun = Sun(name="太阳", size_scale=1e2)  # 太阳放大 100 倍，距离保持不变
    earth = Earth(name="地球", size_scale=1.8e3)  # 地球放大 1800 倍，距离保持不变
    earth_moon_d = 20000000  # 因为地球放大 1800 倍，为了较好的效果，地月距离要比实际大才行
    moon = Moon(name="月球", size_scale=3e3,  # 月球球放大 3000 倍，为了较好的效果，地月距离要比实际大
                init_position=[earth_moon_d, 0, AU],
                init_velocity=[0, 0, 0],
                ignore_mass=True,
                rotation_speed=0.4065,
                # gravity_only_for_earth=True
                )# .set_light_disable(True)
    bodies = [
        sun, earth, moon
    ]


    def on_timer_changed(time_data: TimeData):
        # 显示轨迹，并设置轨迹长度
        UrsinaConfig.show_trail = True
        UrsinaConfig.trail_length = 800
        # 设置运行速度（加速10倍）
        UrsinaConfig.run_speed_factor = 10

        # 以下配置可以快速查看4年的轨迹
        # UrsinaConfig.trail_length = 2800
        # # 设置运行速度（加速50倍）
        # UrsinaConfig.run_speed_factor = 50

        # 1个月有29.5天
        days_per_month = 29.5
        # 1天多少角度
        angle_per_day = 360 / days_per_month
        # 当前天数的角度（度）
        angle = time_data.total_days * angle_per_day
        # 当前天数的角度（弧度）
        angle = angle * np.pi / 180
        # 计算月亮的坐标（这里没有用到万有引力）
        px = earth_moon_d * np.cos(angle)
        pz = earth_moon_d * np.sin(angle)
        moon.position = [earth.position[0] + px, 0, earth.position[2] + pz]


    def on_ready():
        camera_look_at(sun)


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    # position=(0, 0, 0) 的位置是站在地球视角，可以观看月相变化的过程
    ursina_run(bodies, SECONDS_PER_DAY, position=(0, 4 * AU, 0), show_timer=True)
