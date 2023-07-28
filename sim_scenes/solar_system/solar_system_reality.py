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

from bodies import Sun, Mercury, Venus, Earth, Mars, Asteroids, Jupiter, Saturn, Uranus, Neptune, Moon
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera, application


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


def are_planets_in_line(positions, line_width):
    # 检查行星的数量是否足够判断是否在一条线上
    if len(positions) < 3:
        return False
    # 获取第一个行星的坐标
    x1, y1, z1 = positions[0]
    # 计算行星之间的向量差
    dx = positions[1][0] - x1
    dy = positions[1][1] - y1
    dz = positions[1][2] - z1
    # 计算线的宽度的平方
    line_width_squared = line_width ** 2
    # 遍历剩余的行星
    for i in range(2, len(positions)):
        # 获取当前行星的坐标
        x, y, z = positions[i]
        # 计算当前行星与第一个行星之间的向量差
        current_dx = x - x1
        current_dy = y - y1
        current_dz = z - z1
        # 计算当前行星与线之间的距离的平方
        distance_squared = (current_dy * dz - current_dz * dy) ** 2 + (current_dz * dx - current_dx * dz) ** 2 + (
                current_dx * dy - current_dy * dx) ** 2
        # 如果距离的平方大于线的宽度的平方，则行星不在一条线上
        if distance_squared > line_width_squared:
            return False
    # 所有行星都在一条线上
    return True


def are_planets_in_line(planets, line_width):
    if len(planets) < 2:
        return False

    x_coords = [planet[0] for planet in planets]
    y_coords = [planet[1] for planet in planets]
    z_coords = [planet[2] for planet in planets]

    x_diff = [abs(x2 - x1) for (x1, x2) in zip(x_coords, x_coords[1:])]
    y_diff = [abs(y2 - y1) for (y1, y2) in zip(y_coords, y_coords[1:])]
    z_diff = [abs(z2 - z1) for (z1, z2) in zip(z_coords, z_coords[1:])]

    widths = [max(d1, d2, line_width) for (d1, d2) in zip(x_diff, y_diff)] + [line_width] + [max(d1, d2, line_width) for
                                                                                             (d1, d2) in
                                                                                             zip(x_diff[::-1],
                                                                                                 y_diff[::-1])]

    return all(w == widths[0] for w in widths)


def are_planets_in_line(planets, line_width):
    if len(planets) < 2:
        return False

    x_coords = [planet[0] for planet in planets]
    y_coords = [planet[1] for planet in planets]
    z_coords = [planet[2] for planet in planets]

    x_diff = [abs(x2 - x1) for (x1, x2) in zip(x_coords, x_coords[1:])]
    y_diff = [abs(y2 - y1) for (y1, y2) in zip(y_coords, y_coords[1:])]
    z_diff = [abs(z2 - z1) for (z1, z2) in zip(z_coords, z_coords[1:])]

    widths = [max(d1, d2, line_width ** 2) for (d1, d2) in zip(x_diff, y_diff)] + [line_width ** 2] + [
        max(d1, d2, line_width ** 2) for (d1, d2) in zip(x_diff[::-1], y_diff[::-1])]

    return all(w == widths[0] for w in widths)


current_time = Time.now()

# in_line_datetimes = []

if __name__ == '__main__':
    #  以下展示的效果为太阳系真实的时间和位置
    #  由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
    sun = Sun(name="太阳", size_scale=0.04e2)  # 太阳放大 40 倍，TODO:调试时的大小，size_scale=0.04e2
    bodies = [
        sun,
        Mercury(name="水星", size_scale=1.5e3),  # 水星
        Venus(name="金星", size_scale=1e3),  # 金星
        Earth(name="地球",
              texture="earth_hd.jpg",
              size_scale=10e3),  # 地球 TODO:调试时的大小，size_scale=10e3
        # Earth(name="地球云层",
        #       texture="transparent_clouds.png",
        #       size_scale=1.01e3),  # 地球云层 TODO:调试时的大小，size_scale=10.1e3
        Moon(name="月球", size_scale=2e3),  # 月球
        Mars(name="火星", size_scale=1.2e3),  # 火星
        # Asteroids(size_scale=1e2, parent=sun, rotate_angle=-20),
        Jupiter(name="木星", size_scale=4e2),  # 木星
        Saturn(name="土星", size_scale=4e2),  # 土星
        Uranus(name="天王星", size_scale=10e2),  # 天王星
        Neptune(name="海王星", size_scale=10e2),  # 海王星
    ]

    earth = bodies[3]
    # 显示自转轴线
    earth.rotate_axis_color = (255, 255, 50)
    # earth.set_light_disable(True)  # TODO:调试时，取消注释

    names = get_bodies_names(bodies)
    names = names.replace("Asteroids,", "")


    def get_body_posvel(body, posvels=None, time=None):
        if posvels is None:
            posvel = get_body_barycentric_posvel(body.__class__.__name__, time)
        else:
            posvel = posvels.get(body.__class__.__name__, None)
        return posvel


    def on_ready():
        # 运行前触发
        camera.rotation_z = -20
        # 需要按照时间和日期控制地球的自转，不能随意转动
        delattr(earth.planet, "rotation_speed")
        delattr(earth.planet, "rotspeed")
        application.time_scale = 2


    def on_timer_changed(time_data: TimeData):
        t = current_time + time_data.total_days
        # posvels = get_bodies_posvels(names, t)
        # earth_loc = None
        earth_pos = None
        sun_pos = None

        positions = []
        for body in bodies:
            if isinstance(body, Asteroids):
                posvel = None
            else:
                posvel = get_body_posvel(body, None, t)

            if isinstance(body, Moon):
                posvel = recalc_moon_position(posvel, earth_pos)

            if posvel is None:
                position, velocity = [sun_pos.x.value * AU,
                                      sun_pos.z.value * AU,
                                      sun_pos.y.value * AU], [0, 0, 0]
            else:
                S_OF_D = 24 * 60 * 60
                # 坐标单位：千米  速度单位：千米/秒
                position, velocity = [posvel[0].x.value * AU, posvel[0].z.value * AU, posvel[0].y.value * AU], \
                                     [posvel[1].x.value * AU / S_OF_D, posvel[1].z.value * AU / S_OF_D,
                                      posvel[1].y.value * AU / S_OF_D]

            if isinstance(body, Asteroids) or isinstance(body, Moon) or isinstance(body, Sun):
                pass
            else:
                positions.append(position)

            body.position = np.array(position)
            body.velocity = np.array(velocity)
            if isinstance(body, Earth):
                # earth_loc = EarthLocation(x=posvel[0].x, y=posvel[0].y, z=posvel[0].z)
                earth_pos = posvel[0]
            elif isinstance(body, Sun):
                sun_pos = posvel[0]

        dt = time_data.get_datetime(str(current_time))

        # # 日期当天的偏转角度+误差
        # angle_of_day = day_of_year * (360 / 365) + 75
        # # 控制地球的自转
        # earth.planet.rotation_y = -(time_data.total_hours) * 15 + angle_of_day

        # 需要按照时间和日期控制地球的自转，不能随意转动
        # 日期是当年的第几天
        timetuple = dt.timetuple()

        # 计算出：日期当天的偏转角度 - 贴图的误差
        # angle_of_day = day_of_year * (360 / 365) - 93.5  # 2023.7.25
        # angle_of_day = day_of_year * (360 / 365) - 60    # 2023.7.27
        # 控制地球的自转速度和方向，保障白天，中国面对太阳（会存在一点点的误差，可以通过上面“贴图的误差”进行调整）。
        # earth.planet.rotation_y = -(time_data.total_hours) * 15 - angle_of_day

        # 计算出：日期当天的偏转角度
        day_of_year = timetuple.tm_yday
        angle_of_day = day_of_year * (360 / 365)
        total_hours = timetuple.tm_hour + timetuple.tm_min / 60 + timetuple.tm_sec / 60 / 60
        earth.planet.rotation_y = -total_hours * 15 - angle_of_day

        # if len(in_line_datetimes) == 0:
        #     in_line = are_planets_in_line(positions, 5*AU)
        #     if in_line:
        #         in_line_datetimes.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
        #         print(in_line_datetimes)
        #         UrsinaConfig.seconds_per = 1

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
