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
from sim_scenes.func import calc_run
from bodies.body import AU
from simulators.calc_simulator import CalcSimulator


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
    bodies = [
        Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
              init_velocity=[OFFSETTING, 0, 0], size_scale=0.5e1),  # 地球放大 5 倍，距离保持不变
        Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
             init_velocity=[-1.054152222, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
    ]  # -1.0543 <  -1.05435 <  -1.0545   ？-1.4935  OK：-1.05918
    #  -1.05415<    <-1.05425
    # 1047.4197364163992
    earth = bodies[0]
    moon = bodies[1]
    # -1.0648500185012806  -1.05435
    # 1.0544061918995067 3.02326384371554e-06 <月球(Moon)> m=7.342e+22(kg), r|d=1.737e+03|3.474e+03(km), v=2.196e+10(km³), d=3.344e+03(kg/m³), p=[-3.796e+03,0.000e+00,3.631e+05](km), v=[-1.05435     0.         -0.01088375](km/s)
    # 1.0544608857544382 3.023593683297842e
    points = get_lagrangian_points(earth.mass, moon.mass, 363104)
    velocities = []
    for i in range(30):
        v = round(-0.846 - (i / 10000), 4)
        velocities.append([v, 0, 0])

    satellites = []
    point = points[0]
    for j, velocitie in enumerate(velocities):
        satellite = Satellite(name=f'卫星{j + 1}', mass=1.4e10, size_scale=1e3, color=(255, 200, 0),
                              init_position=[point[0],
                                             point[1],
                                             point[2]],
                              init_velocity=velocities[j])
        # bodies.append(satellite)
        satellites.append(satellite)

    CalcSimulator.init_velocity_x = moon.init_velocity[0]
    CalcSimulator.offset_rate_x = 0.0001
    CalcSimulator.accelerations = []
    CalcSimulator.velocities = []


    def on_init(bodies):
        return bodies


    def on_ready(simulator):
        pass


    def evolve_next(simulator):
        if not hasattr(simulator, "loop"):
            simulator.loop = 1000
        else:
            simulator.loop -= 1
        # print(simulator.bodies_sys.bodies)
        moon = simulator.bodies_sys.bodies[1]

        from simulators.ursina.entities.entity_utils import get_value_direction_vectors

        velocity = get_value_direction_vectors(moon.velocity)
        acceleration = get_value_direction_vectors(moon.acceleration)
        vel_value = velocity[0]  # km/s
        acc_value = acceleration[0]  # km/s²
        print(vel_value, acc_value, moon)

        CalcSimulator.accelerations.append(acc_value)
        CalcSimulator.velocities.append(vel_value)

        # if not hasattr(simulator, "init_acc_value") and acc_value > 0:
        #     simulator.init_acc_value = acc_value
        # elif hasattr(simulator, "init_acc_value"):
        #     if simulator.loop == 1:
        #         diff = acc_value - simulator.init_acc_value
        #         if CalcSimulator.init_velocity_x > 0:
        #             d = 1
        #         else:
        #             d = -1
        #         if abs(diff) < 1e-10:
        #             print("完成", CalcSimulator.init_velocity_x)
        #             exit(0)
        #         elif diff > 0:
        #             CalcSimulator.init_velocity_x += CalcSimulator.offset_rate_x * d
        #             print("慢慢靠近", CalcSimulator.init_velocity_x)
        #         else:
        #             CalcSimulator.init_velocity_x -= CalcSimulator.offset_rate_x * d
        #             print("慢慢远离", CalcSimulator.init_velocity_x)

        return simulator.loop > 0


    loop = 1
    while loop > 0:
        moon.init_velocity = [CalcSimulator.init_velocity_x, moon.init_velocity[1], moon.init_velocity[2]]
        calc_run(bodies, SECONDS_PER_HOUR,
                 on_init=on_init,
                 on_ready=on_ready,
                 evolve_next=evolve_next)
        loop -= 1

    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6))
    max_value = max(CalcSimulator.accelerations[1:])
    min_value = min(CalcSimulator.accelerations[1:])
    x = []
    for i in range(len(CalcSimulator.accelerations)):
        x.append(i)
    plt.title("%s max:%.4f mix:%.4f diff:%.4f" % (moon.init_velocity[0], max_value*1e6, min_value*1e6, (max_value - min_value)*1e6))
    plt.ylim(2.95e-6, 3.06e-6)
    plt.plot(x[1:], CalcSimulator.accelerations[1:], label="accelerations")
    # plt.plot(x, CalcSimulator.velocities, label="velocities")

    plt.legend()
    plt.show()
