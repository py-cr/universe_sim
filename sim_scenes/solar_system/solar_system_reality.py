# -*- coding:utf-8 -*-
# title           :模拟太阳系给天体真实时间和位置
# description     :模拟太阳系给天体真实时间和位置
# author          :Python超人
# date            :2023-07-23
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com de423
# solar_system_ephemeris.bodies
# ('earth', 'sun', 'moon', 'mercury', 'venus', 'earth-moon-barycenter', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune')


import numpy as np
from astropy.coordinates import get_body_barycentric_posvel
from astropy.time import Time

from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Moon
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera


def get_bodies_posvels(planet_names="sun,mercury,venus,earth,moon,mars,jupiter,saturn,uranus,neptune", time=None):
    if time is None:
        time = Time.now()
    planets = planet_names.split(",")
    posvels = {}
    for planet in planets:
        try:
            position, velocity = get_body_barycentric_posvel(planet, time)
            posvels[planet] = position, velocity
            # print(planet, position)
        except Exception as e:
            print(planet, str(e))
    return posvels


def recalc_moon_position(moon_posvel, earth_pos):
    moon_pos, moon_vel = moon_posvel[0], moon_posvel[1]
    moon_pos_to_earth = moon_pos - earth_pos
    moon_pos_to_earth = moon_pos_to_earth * 50

    return moon_pos_to_earth + earth_pos, moon_vel


def get_bodies_names(bodies):
    names = ""
    for body in bodies:
        names += body.__class__.__name__ + ","
    return names[0:-1]


current_time = Time.now()

if __name__ == '__main__':
    # 八大行星：木星(♃)、土星(♄)、天王星(♅)、海王星(♆)、地球(⊕)、金星(♀)、火星(♂)、水星(☿)
    # 排列顺序
    # 1、体积：(以地球为1)木星 ：土星 ：天王星 ：海王星 ：地球 ：金星 ：火星 ：水星 = 1330：745：65：60：1：0.86：0.15：0.056
    # 2、质量：(以地球为1)木星 ：土星 ：天王星 ：海王星 ：地球 ：金星 ：火星 ：水星 = 318：95：14.53：17.15：1：0.8：0.11：0.0553
    # 3、离太阳从近到远的顺序：水星、金星、地球、火星、木星、土星、天王星、海王星
    #  =====================================================================
    #  以下展示的效果为太阳系真实的距离
    #  由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
    sun = Sun(name="太阳", size_scale=0.4e2)  # 太阳放大 40 倍，距离保持不变
    bodies = [
        sun,
        Mercury(name="水星", size_scale=1.5e3),  # 水星
        Venus(name="金星", size_scale=1e3),  # 金星
        Earth(name="地球", size_scale=1e3),  # 地球
        Moon(name="月球", size_scale=2e3),  # 月球
        Mars(name="火星", size_scale=1.2e3),  # 火星
        Jupiter(name="木星", size_scale=4e2),  # 木星
        Saturn(name="土星", size_scale=4e2),  # 土星
        Uranus(name="天王星", size_scale=10e2),  # 天王星
        Neptune(name="海王星", size_scale=10e2),  # 海王星
    ]

    names = get_bodies_names(bodies)


    def get_body_posvel(body, posvels):
        posvel = posvels.get(body.__class__.__name__, None)
        return posvel


    def on_ready():
        # 运行前触发
        camera.rotation_z = -20


    def on_timer_changed(time_data: TimeData):
        t = current_time + time_data.total_days
        posvels = get_bodies_posvels(names, t)
        # earth_loc = None
        earth_pos = None
        for body in bodies:

            posvel = get_body_posvel(body, posvels)
            if isinstance(body, Moon):
                posvel = recalc_moon_position(posvel, earth_pos)

            if posvel is None:
                position, velocity = [0, 0, 0], [0, 0, 0]
            else:
                S_OF_D = 24 * 60 * 60
                # 坐标单位：千米  速度单位：千米/秒
                position, velocity = [posvel[0].x.value * AU, posvel[0].z.value * AU, posvel[0].y.value * AU], \
                                     [posvel[1].x.value * AU / S_OF_D, posvel[1].z.value * AU / S_OF_D,
                                      posvel[1].y.value * AU / S_OF_D]

            body.position = np.array(position)
            body.velocity = np.array(velocity)
            if isinstance(body, Earth):
                # earth_loc = EarthLocation(x=posvel[0].x, y=posvel[0].y, z=posvel[0].z)
                earth_pos = posvel[0]

        dt = time_data.get_datetime(str(current_time))
        # print(time_data.get_datetime(str(current_time)))
        ControlUI.current_ui.show_message(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                          font="verdana.ttf",
                                          close_time=-1)


    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    dt = SECONDS_PER_DAY  # 1秒=1天
    dt = 1  # 1秒=1秒
    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, dt,
               position=(0, 0.2 * AU, -3 * AU),
               gravity_works=False,  # 关闭万有引力的计算
               show_grid=False,
               timer_enabled=True)
