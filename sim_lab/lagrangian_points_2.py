"""
https://www.163.com/dy/article/G5F1016F053102ZV.html
https://www.sciencedirect.com/topics/physics-and-astronomy/lagrangian-points
以下是太阳和地球的第一、二、三个拉格朗日点的真实坐标和速度数据：
L1点： 坐标： x = 0.010205 AU， y = 0 AU， z = 0 AU 速度： vx = 0 m/s， vy = 246.593 m/s， vz = 0 m/s
L2点： 坐标： x = -0.010205 AU， y = 0 AU， z = 0 AU 速度： vx = 0 m/s， vy = -246.593 m/s， vz = 0 m/s
L3点： 坐标： x = 0.990445 AU， y = 0 AU， z = 0 AU 速度： vx = 0 m/s， vy = 11.168 m/s， vz = 0 m/s
L4点： 坐标： x = 0.500 AU， y = 0.866025 AU， z = 0 AU 速度： vx = -2446.292 m/s， vy = -1412.901 m/s， vz = 0 m/s
L5点： 坐标： x = 0.500 AU， y = -0.866025 AU， z = 0 AU 速度： vx = -2446.292 m/s， vy = 1412.901 m/s， vz = 0 m/s
https://baike.baidu.com/pic/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E7%82%B9/731078/0/dbb44aed2e738bd4510fa07aa98b87d6277ff94b?fr=lemma&fromModule=lemma_content-image&ct=single#aid=0&pic=dbb44aed2e738bd4510fa07aa98b87d6277ff94b
"""
#
# AU = 1.496e8
#
#
# def compute_barycenter(masses, positions):
#     """
#     Compute the barycenter position of celestial objects in 3D space
#     masses: a list of masses of celestial objects
#     positions: a list of positions of celestial objects, each position is a tuple (x, y, z)
#     """
#     m_sum = sum(masses)
#     x_sum = 0
#     y_sum = 0
#     z_sum = 0
#     for i in range(len(masses)):
#         x_sum += masses[i] * positions[i][0] / m_sum
#         y_sum += masses[i] * positions[i][1] / m_sum
#         z_sum += masses[i] * positions[i][2] / m_sum
#     return (x_sum, y_sum, z_sum)
#
#
# def get_lagrangian_points(m1, m2, r):
#     """
#     https://baike.baidu.com/item/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E7%82%B9/731078
#
#     @param m1: 大质量
#     @param m2: 小质量
#     @param r: 半径
#     @return:
#     """
#     a = m2 / (m1 + m2)
#     l1 = (r * (1 - pow(a / 3, 1 / 3)), 0)
#     l2 = (r * (1 + pow(a / 3, 1 / 3)), 0)
#     l3 = (-r * (1 + (5 * a) / 12), 0)
#     l4 = ((r / 2) * ((m1 - m2) / (m1 + m2)), pow(3, 1 / 2) / 2 * r)
#     l5 = ((r / 2) * ((m1 - m2) / (m1 + m2)), -pow(3, 1 / 2) / 2 * r)
#
#     # print(l1[0]/AU, l2[0]/AU, l3[0]/AU, l4[0]/AU, l5[0]/AU)
#     return l1, l2, l3, l4, l5
#
#
# def show_figure(points, p1_name, p2_name, unit, barycenter=None):
#     import matplotlib.pyplot as plt
#
#     plt.figure(figsize=(16, 12))
#     plt.plot(0, 0, "ro", markersize=20, label=p1_name)
#     plt.text(-unit / 20, -unit / 10, p1_name, fontsize=30, color="r")
#     plt.plot(unit, 0, "b.", markersize=4, label=p2_name)
#     plt.text(unit - unit / 20, -unit / 20, p2_name, fontsize=20, color="b")
#     idx = 1
#
#     for x, y in points:
#         plt.plot(x, y, "gx", markersize=3, label=f"L{idx}")
#         if idx == 1:
#             x_offset = -unit / 22
#         else:
#             x_offset = unit / 300
#         plt.text(x + x_offset, y + unit / 300, f"L{idx}", fontsize=18, color="g")
#         idx += 1
#
#     if barycenter is not None:
#         plt.plot(barycenter[0], barycenter[1], "gx", markersize=10, label=f"L{idx}")
#
#     # plt.plot(x, y, "b.")  # b：蓝色，.：点
#     # plt.plot(x, y1, "ro")  # r：红色，o：圆圈
#     # plt.plot(x, y2, "kx")  # k：黑色，x：x字符(小叉)
#     plt.show()  # 在窗口显示该图片
#
#
# barycenter = compute_barycenter([5.97237e24, 7.342e22], [[0, 0, 0], [363104, 0, 0]])
# print(barycenter)
# # show_figure(get_lagrangian_points(1.9891e30, 5.97237e24, AU), "Sun", "Earth", AU)
# show_figure(get_lagrangian_points(5.97237e24, 7.342e22, 363104), "Earth", "Moon", 363104, barycenter)

# **************************************************************************************************************
# **************************************************************************************************************

# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon
from objs import Satellite, Satellite2
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from bodies.body import AU
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent
from simulators.ursina.ursina_mesh import create_line


def compute_barycenter(masses, positions):
    """
    Compute the barycenter position of celestial objects in 3D space
    masses: a list of masses of celestial objects
    positions: a list of positions of celestial objects, each position is a tuple (x, y, z)
    """
    m_sum = sum(masses)
    x_sum = 0
    y_sum = 0
    z_sum = 0
    for i in range(len(masses)):
        x_sum += masses[i] * positions[i][0] / m_sum
        y_sum += masses[i] * positions[i][1] / m_sum
        z_sum += masses[i] * positions[i][2] / m_sum
    return (x_sum, y_sum, z_sum)


def get_lagrangian_points(m1, m2, r):
    """
    https://baike.baidu.com/item/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E7%82%B9/731078

    @param m1: 大质量
    @param m2: 小质量
    @param r: 半径
    @return:
    """
    a = m2 / (m1 + m2)
    l1 = (0, 0, r * (1 - pow(a / 3, 1 / 3)))
    l2 = (0, 0, r * (1 + pow(a / 3, 1 / 3)))
    l3 = (0, 0, -r * (1 + (5 * a) / 12))
    l4 = (pow(3, 1 / 2) / 2 * r, 0, (r / 2) * ((m1 - m2) / (m1 + m2)))
    l5 = (-pow(3, 1 / 2) / 2 * r, 0, (r / 2) * ((m1 - m2) / (m1 + m2)))

    return l1, l2, l3, l4, l5


if __name__ == '__main__':
    """
    地球、月球
    """
    OFFSETTING = 0
    # TODO: 可以抵消月球带动地球的力，保持地球在原地
    # OFFSETTING = 0.01265
    bodies = [
        Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
              init_velocity=[OFFSETTING, 0, 0], size_scale=0.5e1),  # 地球放大 5 倍，距离保持不变
        Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
             init_velocity=[-1.054152222, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
    ]  # -1.0543 <  -1.05435 <  -1.0545
    earth = bodies[0]
    moon = bodies[1]

    points = get_lagrangian_points(earth.mass, moon.mass, 363104)
    offset_points = [
        [0, 0, 3301.05],  # TODO:调整
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    velocities = [
        [-0.889, -0.1, 0],  # [-0.859, 0, 0],
        [-1.265, 0, 0],
        [1.03, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    velocities = [
        [-0.885, 0, 0],  # [-0.859, 0, 0],
        [-0.879, 0, 0],
        [-0.869, 0, 0],
    ]
    velocities = []
    for i in range(10):
        v = round(-0.890205 - (i / 1000000), 20)  # TODO:调整
        print(v)
        velocities.append([v, 0, 0])

    satellites = []
    for i, point in enumerate(points[0:1]):
        for j, velocitie in enumerate(velocities):
            satellite = Satellite(name=f'卫星{j + 1}', mass=1.4e10, size_scale=1e3, color=(255, 200, 0),
                                  init_position=[point[0] + offset_points[i][0],
                                                 point[1] + offset_points[i][1],
                                                 point[2] + offset_points[i][2]],
                                  init_velocity=velocities[j], gravity_only_for=[earth, moon])
            bodies.append(satellite)
            satellites.append(satellite)


    def on_ready():
        # 运行前触发
        # 运行开始前，将摄像机指向地球

        # 摄像机看向地球
        camera_look_at(moon)


    def on_timer_changed(time_data: TimeData):
        from ursina import destroy
        if hasattr(earth, "line"):
            destroy(earth.line)
        earth.line = create_line(from_pos=earth.planet.position, to_pos=moon.planet.main_entity.position)
        for satellite in satellites:
            satellite.look_at(earth)


    # 订阅事件后，上面的函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR * 10,
               position=(-5000, 500000, -10),
               show_timer=True,
               show_trail=True)
