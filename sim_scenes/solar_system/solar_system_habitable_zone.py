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
from ursina import Vec3
import numpy as np

if __name__ == '__main__':
    # 目前认为 太阳系 的宜居带范围是从距离太阳0.95个天文单位 (约1.42亿千米)到 2.4个天文单位（约3.59亿千米）的范围为宜居带，
    # 其宽度约为2.17亿千米， 按照这个标准，太阳系的宜居带中只有三个大型天体，分别是地球、 月球 以及火星（1.52天文单位）。
    sun = Sun(name="太阳", size_scale=0.5e2)  # 太阳放大 80 倍，距离保持不变
    earth = Earth(name="地球", size_scale=1.5e3)  # 地球放大 1500 倍，距离保持不变
    moon_d = 10000000
    moon = Moon(name="月球", size_scale=1e2,
                init_position=[moon_d, 0, 0],
                init_velocity=[0, 0, 0],
                distance_scale=0.2,
                gravity_only_for_earth=True
                )
    bodies = [
        sun,
        Venus(name="金星", size_scale=1.5e3),  # 金星放大 1500 倍，距离保持不变
        earth, moon,
        # Moon(name="月球", size_scale=2e3,
        #      # init_position=[0, 0, 363104 + 1.12 * AU],
        #      # init_velocity=[-(29.79 + 1.03), 0, 0]
        #      init_position=[15000000, 0, AU],
        #      init_velocity=[-32.79, 0, 2.03], gravity_only_for_earth=True
        #      ),  # 月球放大 2000 倍，距离保持不变
        Mars(name="火星", size_scale=2e3),  # 火星放大 2000 倍，距离保持不变
        Asteroids(name="小行星群", size_scale=3.2e2,
                  parent=sun),  # 小行星群模拟(仅 ursina 模拟器支持)
        HabitableZone(name="宜居带", size_scale=1e2,
                      parent=sun),  # 宜居带模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=2e2),  # 木星放大 200 倍，距离保持不变
    ]


    def on_ready():
        # 月球就会跟着地球自转而转
        moon.planet.parent = earth.planet


    def on_timer_changed(time_data: TimeData):
        # print(moon.planet.position)
        # moon.planet.rotation = -Vec3(earth.planet.rotation_x, # - earth.planet.ring_rotation_x,
        #                            earth.planet.rotation_y,
        #                            earth.planet.rotation_z)
        # 为了不让月球随着地球的周期旋转，则需要获取地球的旋转角度
        angle = earth.planet.rotation_y
        # TODO:根据旋转的角度对月球的位置进行计算，保证月球公转和地球自转的关系 365天=12月
        # angle = np.array(angle * np.pi)
        #
        # px = moon_d * UrsinaConfig.SCALE_FACTOR * np.cos(angle)
        # pz = moon_d * UrsinaConfig.SCALE_FACTOR * np.sin(angle)
        # moon.planet.world_position = Vec3(0,0,0)


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
