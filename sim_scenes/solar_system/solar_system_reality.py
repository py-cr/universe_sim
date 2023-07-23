# -*- coding:utf-8 -*-
# title           :模拟太阳系给天体真实时间和位置
# description     :模拟太阳系给天体真实时间和位置
# author          :Python超人
# date            :2023-07-23
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import numpy as np

from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Asteroids
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_event import UrsinaEvent
from astropy.coordinates import get_body_barycentric
from astropy.time import Time


def get_bodies_positions(planet_names="sun,mercury,venus,earth,moon,mars,jupiter,saturn,uranus,neptune", time=None):
    if time is None:
        time = Time.now()
    planets = planet_names.split(",")
    positions = {}
    for planet in planets:
        try:
            position = get_body_barycentric(planet, time)
            positions[planet] = position
            print(planet, position)
        except Exception as e:
            print(planet, str(e))
    return positions


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
    sun = Sun(name="太阳", size_scale=0.4e2)  # 太阳放大 80 倍，距离保持不变
    bodies = [
        sun,
        Mercury(name="水星", size_scale=3e3),  # 水星
        Venus(name="金星", size_scale=3e3),  # 金星
        Earth(name="地球", size_scale=3e3),  # 地球
        Moon(name="月球", size_scale=3e3),  # 月球
        Mars(name="火星", size_scale=3e3),  # 火星
        Jupiter(name="木星", size_scale=6e2),  # 木星
        Saturn(name="土星", size_scale=6e2),  # 土星
        Uranus(name="天王星", size_scale=10e2),  # 天王星
        Neptune(name="海王星", size_scale=10e2),  # 海王星
    ]
    # pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com de423
    names = get_bodies_names(bodies)


    def get_body_position(body, positions):
        position = positions.get(body.__class__.__name__, None)
        if position is None:
            return [0, 0, 0]

        # return [position.x.value * AU, position.y.value * AU, position.z.value * AU]
        return [position.x.value * AU, position.z.value * AU, position.y.value * AU]


    def on_ready():
        # 运行前触发
        pass


    def on_timer_changed(time_data: TimeData):
        t = current_time + time_data.total_days
        positions = get_bodies_positions(names, t)
        for body in bodies:
            position = get_body_position(body, positions)
            body.position = np.array(position)

        dt = time_data.get_datetime(str(current_time))
        # print(time_data.get_datetime(str(current_time)))
        ControlUI.current_ui.show_message(dt.strftime('%Y-%m-%d %H:%M:%S'), font="simsun.ttc", close_time=-1)


    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK,
               position=(0, 2 * AU, -11 * AU),
               gravity_works=False,  # 关闭万有引力的计算
               show_grid=False,
               show_timer=True)
