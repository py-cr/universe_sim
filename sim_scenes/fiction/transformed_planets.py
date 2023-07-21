# -*- coding:utf-8 -*-
# title           :改造太阳系的宜居带的星球
# description     :改造太阳系的宜居带的星球
# author          :Python超人
# date            :2023-07-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Asteroids
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run
import numpy as np

from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    # 改造太阳系的宜居带的星球
    #  =====================================================================
    #  以下展示的效果为太阳系真实的距离
    #  由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
    sun = Sun(name="太阳", size_scale=0.8e2)  # 太阳放大 80 倍，距离保持不变
    earth_moon_d = 40000000  # 因为地球放大 1800 倍，为了较好的效果，地月距离要比实际大才行
    moon = Moon(name="月球", size_scale=4e3,
                texture="transformed/moon.jpg",
                )
    earth = Earth(name="地球", size_scale=4e3,
                  texture="transformed/earth.jpg",
                  distance_scale=2)
    bodies = [
        sun,
        Mercury(name="水星",
                size_scale=4e3,
                texture="transformed/mercury.jpg",
                distance_scale=2),
        Venus(name="金星", size_scale=4e3,
              texture="transformed/venus.jpg",
              distance_scale=1.8),
        earth,  # 地球放大 4000 倍，距离放大 1.3 倍
        moon,
        Mars(name="火星", size_scale=4e3,
             texture="transformed/mars.jpg",
             distance_scale=1.8),
    ]


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
        moon.position = [earth.position[0] * earth.distance_scale + px,
                         0,
                         earth.position[2] * earth.distance_scale + pz]


    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK,
               timer_enabled=True,
               position=(0, 2 * AU, -11 * AU))
