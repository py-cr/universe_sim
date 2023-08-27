# -*- coding:utf-8 -*-
# title           :天体数据服务类型
# description     :天体数据服务类型
# author          :Python超人
# date            :2023-08-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import math
from common.consts import G, AU, SECONDS_PER_DAY
from bodies import Body, Sun, Asteroids, Moon, Earth
import numpy as np


def calc_solar_acceleration(body_or_pos, big_body):
    """
    计算天体的加速度
    @param body_or_pos: 需要计算的天体
    @param big_body: 大天体（太阳 或者 地球）
    @return:
    """
    if isinstance(body_or_pos, Body):
        body_pos = body_or_pos.position
    else:
        body_pos = body_or_pos
    x, y, z = body_pos[0] * 1000 - big_body.position[0] * 1000, \
              body_pos[1] * 1000 - big_body.position[1] * 1000, \
              body_pos[2] * 1000 - big_body.position[2] * 1000
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    a = G * big_body.mass / r ** 2
    ax = -a * x / r
    ay = -a * y / r
    az = -a * z / r
    return [ax / 1000, ay / 1000, az / 1000]  # 设置天体的加速度（单位：km/s²）


def get_body_posvel(body, time=None):
    """
    获取太阳系天体指定时间的位置和矢量速度
    pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com de423
    @param body: 天体（天体名称）
    @param time: 时间
    @return:
    """
    from astropy.coordinates import get_body_barycentric_posvel
    from astropy.time import Time
    if time is None:
        time = Time.now()
    if not isinstance(body, str):
        body = body.__class__.__name__

    posvel = get_body_barycentric_posvel(body, time)

    return posvel


def get_bodies_posvels(planet_names="sun,mercury,venus,earth,moon,mars,jupiter,saturn,uranus,neptune", time=None):
    from astropy.coordinates import get_body_barycentric_posvel
    from astropy.time import Time
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
    """
    重新计算月球的位置（由于月球和地球的距离在整个太阳系尺度下非常近，为了较好的显示效果，需要放大月球和地球的距离，但不要改变月球相对地球的位置）
    @param moon_posvel: 月球的三维坐标位置和三维矢量速度
    @param earth_pos: 地球的三维坐标位置
    @return:
    """
    moon_pos, moon_vel = moon_posvel[0], moon_posvel[1]
    moon_pos_to_earth = moon_pos - earth_pos
    moon_pos_to_earth = moon_pos_to_earth * 50

    return moon_pos_to_earth + earth_pos, moon_vel


def get_celestial_body_data(body_name):
    # pip install ephem
    import ephem
    # 创建一个Observer对象，用于指定观测者的位置
    observer = ephem.Observer()
    observer.lat = '0'  # 观测者的纬度，这里使用0度作为示例
    observer.lon = '0'  # 观测者的经度，这里使用0度作为示例
    # 创建一个Date对象，表示当前时间
    current_time = ephem.now()
    # 根据天体名称创建一个CelestialBody对象
    body = getattr(ephem, body_name)()
    # 计算天体的位置和速度
    body.compute(observer)
    # 获取天体的实时位置和速度信息
    position = (body.ra, body.dec)  # 天体的赤经和赤纬
    velocity = (body.ra_velocity, body.dec_velocity)  # 天体的赤经速度和赤纬速度
    return position, velocity


def set_solar_system_celestial_position(bodies, dt, recalc_moon_pos):
    """
    根据日期时间 dt 设置太阳系中天体的真实位置
    @param bodies: 太阳系中天体
    @param dt: 时间
    @param recalc_moon_pos: 是否对月球的位置进行重新计算。
     为了更好的展示效果，需要对月球的位置重新计算（使得地月距离放大，月球相对地球方向不变），
     重新计算位置后，地球和月球可以放大1000倍以上
    @return:
    """
    earth_pos = None
    sun_pos = None
    earth = None
    sun = None
    moon = None

    for body in bodies:
        if isinstance(body, Sun):
            sun = body
        elif isinstance(body, Earth):
            earth = body
        elif isinstance(body, Moon):
            moon = body

    for body in bodies:
        if isinstance(body, Asteroids):  # 小行星带是模拟，不是正常的天体
            posvel = None
        else:
            # 获取天体的三维位置和矢量速度
            posvel = get_body_posvel(body, dt)

        if isinstance(body, Moon):  # 如果是月球，为了更好的展示效果，需要对月球的位置重新计算
            moon_real_pos = [posvel[0].x.value * AU, posvel[0].z.value * AU, posvel[0].y.value * AU]
            # TODO:注释下行，月球就会在真实的位置
            if recalc_moon_pos:
                posvel = recalc_moon_position(posvel, earth_pos)

        if posvel is None:
            # posvel 为空，则使用太阳的坐标
            position, velocity = [sun_pos.x.value * AU,
                                  sun_pos.z.value * AU,
                                  sun_pos.y.value * AU], [0, 0, 0]
        else:
            # 坐标单位：千米  速度单位：千米/秒
            position, velocity = [posvel[0].x.value * AU, posvel[0].z.value * AU, posvel[0].y.value * AU], \
                                 [posvel[1].x.value * AU / SECONDS_PER_DAY,
                                  posvel[1].z.value * AU / SECONDS_PER_DAY,
                                  posvel[1].y.value * AU / SECONDS_PER_DAY]

        # 实时调整天体的位置和速度
        body.position = np.array(position)
        body.velocity = np.array(velocity)

        if isinstance(body, Asteroids):
            pass
        elif isinstance(body, Sun):
            # 记录太阳的位置
            sun_pos = posvel[0]
        elif isinstance(body, Moon):
            # 月球受到2个影响比较大的天体引力（地球和太阳），计算引力引起的加速度和
            acc_earth = calc_solar_acceleration(moon_real_pos, earth)
            acc_sun = calc_solar_acceleration(moon_real_pos, sun)
            body.acceleration = [acc_earth[0] + acc_sun[0],
                                 acc_earth[1] + acc_sun[1],
                                 acc_earth[2] + acc_sun[2]]
        # elif isinstance(body, Earth):
        #     # 月球受到2个影响比较大的天体引力（地球和太阳），计算引力引起的加速度和
        #     acc_earth = calc_solar_acceleration(earth, moon)
        #     acc_sun = calc_solar_acceleration(earth, sun)
        #     body.acceleration = [acc_earth[0] + acc_sun[0],
        #                          acc_earth[1] + acc_sun[1],
        #                          acc_earth[2] + acc_sun[2]]
        else:
            # 其他天体受到太阳引力
            body.acceleration = calc_solar_acceleration(body, sun)

        if isinstance(body, Earth):
            # 记录地球的位置
            earth_pos = posvel[0]


def set_earth_rotation(earth, dt):
    """
    根据指定的时间控制地球的旋转角度（保证地球的自转和北京时间同步）
    @param dt: 时间 datetime
    @return:
    """

    # timetuple 可以获取当天的小时数、分数钟、秒数
    timetuple = dt.timetuple()
    # 当年的第几天
    day_of_year = timetuple.tm_yday
    # 根据当年的第几天计算出该日期当天的偏转角度：360度 / 365天 = 当天的偏转角度
    angle_of_day = day_of_year * (360 / 365)
    # 计算出精确的小时数
    total_hours = timetuple.tm_hour + timetuple.tm_min / 60 + timetuple.tm_sec / 60 / 60
    # -total_hours： 负号控制地球的旋转方向、1天24小时，360度/24=15
    # total_hours * 15：1天24小时，360度/24小时=1小时15度
    # angle_of_day： 1年第几天的角度
    earth.planet.rotation_y = -total_hours * 15 - angle_of_day + 15  # 精确调整


# pip install Astropysics

if __name__ == '__main__':
    # pip install astropy
    from astropy.coordinates import get_body_barycentric_posvel
    from astropy.time import Time
    import astropy.units as u

    t = Time.now()
    print("日期时间：", t)
    posvel = get_body_barycentric_posvel('earth', t)
    print("坐标(公里)：", [posvel[0].x.to(u.km), posvel[0].y.to(u.km), posvel[0].z.to(u.km)])
    print("速度(公里/秒)：",
          [posvel[1].x.to(u.km / u.second), posvel[1].y.to(u.km / u.second), posvel[1].z.to(u.km / u.second)])

    # print("速度(公里/秒)：", posvel[1] * AU / SECONDS_PER_DAY)
