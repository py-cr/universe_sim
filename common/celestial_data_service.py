# -*- coding:utf-8 -*-
# title           :天体数据服务类型
# description     :天体数据服务类型
# author          :Python超人
# date            :2023-08-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import math
from common.consts import G
from bodies import Body


def calc_solar_acceleration(body_or_pos, big_body):
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
