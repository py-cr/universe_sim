# -*- coding:utf-8 -*-
# title           :天体数据服务类型
# description     :天体数据服务类型
# author          :Python超人
# date            :2023-08-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================


def get_body_posvel(body, time=None):
    """
    获取太阳系天体指定时间的位置和矢量速度
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

    # # 示例用法
    # body_name = 'Mars'  # 天体名称，这里以火星为例
    # position, velocity = get_celestial_body_data(body_name)
    # print(f"The current position of {body_name} is: {position}")
    # print(f"The current velocity of {body_name} is: {velocity}")
