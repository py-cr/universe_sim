# -*- coding:utf-8 -*-
# title           :太阳系宜居带模拟场景
# description     :太阳系宜居带模拟场景（展示的效果为太阳系真实的距离）
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, HabitableZone, \
    Asteroids
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import Vec3, time
import numpy as np
import math

if __name__ == '__main__':
    # 目前认为 太阳系 的宜居带范围是从距离太阳0.95个天文单位 (约1.42亿千米)到 2.4个天文单位（约3.59亿千米）的范围为宜居带，
    # 其宽度约为2.17亿千米， 按照这个标准，太阳系的宜居带中只有三个大型天体，分别是地球、 月球 以及火星（1.52天文单位）。
    sun = Sun(name="太阳", size_scale=0.5e2)  # 太阳放大 50 倍，距离保持不变
    earth = Earth(name="地球", size_scale=1.2e3)  # 地球放大 1200 倍，距离保持不变
    earth_moon_d = 13000000  # 因为地球放大 1200 倍，已经占据了月球的轨道，为了较好的效果，地月距离要比实际大才行
    moon = Moon(name="月球", size_scale=1.3e3,
                init_position=[earth_moon_d, 0, AU],
                init_velocity=[0, 0, 0],
                ignore_mass=True,
                # gravity_only_for_earth=True
                )
    bodies = [
        sun,
        Venus(name="金星", size_scale=1.2e3),  # 金星放大 1200 倍，距离保持不变
        earth, moon,
        Mars(name="火星", size_scale=1.2e3),  # 火星放大 1200 倍，距离保持不变
        Asteroids(name="小行星群", size_scale=3.2e2,
                  parent=sun),  # 小行星群模拟(仅 ursina 模拟器支持)
        HabitableZone(name="宜居带", size_scale=1e2,
                      parent=sun),  # 宜居带模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=2e2),  # 木星放大 200 倍，距离保持不变
    ]


    def on_ready():
        # UrsinaConfig.trail_length = 1000
        pass


    def on_timer_changed(time_data: TimeData):
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


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY, position=(0, 2 * AU, -11 * AU),
               show_timer=True,
               bg_music="sounds/interstellar.mp3")
