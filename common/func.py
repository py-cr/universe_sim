# -*- coding:utf-8 -*-
# title           :公共库函数
# description     :公共库函数
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from PIL import Image
from common.consts import AU, G
import numpy as np
import random
import os
import math


def get_dominant_colors(infile, resize=(20, 20)):
    """
    获取图片的主要颜色
    @param infile:
    @param resize:
    @return:
    """
    image = Image.open(infile)

    # 缩小图片，否则计算机压力太大
    small_image = image.resize(resize)
    result = small_image.convert(
        "P", palette=Image.ADAPTIVE, colors=10
    )

    # 10个主要颜色的图像

    # 找到主要的颜色
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)

    colors = list()

    for i in range(min(10, len(color_counts))):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index * 3: palette_index * 3 + 3]
        colors.append(tuple(dominant_color))

    return colors


def get_positions_velocitys(angles, velocity=1, radius=1, radius_offset=None, velocity_offset=None):
    """
    以位置 （0, 0, 0）为中心，随机获取空间上的位置和公转方向的速度集合
    （比如：获取大批小行星的位置）
    @param angles: 参考中心位置（0, 0, 0）的角度集合
    @param velocity: 速度
    @param radius: 半径（距离中心位置（0, 0, 0）的距离）
    @param radius_offset:在半径的基础上，随机偏移的值
    @param velocity_offset:在速度的基础上，随机偏移的值
    @return:
    """
    angles = np.array(angles * np.pi)

    if isinstance(radius_offset, float):
        radius = radius + np.random.rand(len(angles)) * radius_offset

    if isinstance(velocity_offset, float):
        velocity = velocity + np.random.rand(len(angles)) * velocity_offset

    pxs = radius * np.cos(angles)
    pzs = radius * np.sin(angles)

    vzs = velocity * np.cos(angles)
    vxs = velocity * np.sin(angles)

    # return pxs, pzs, vxs, vzs
    return np.round(pxs, 2), np.round(pzs, 2), -np.round(vxs, 2), np.round(vzs, 2)


def find_file(file_path, default_val=None, find_deep=5):
    """
    代码可能会放到任意级别的目录下面，该函数能逐级往上级目录进行查找文件
    @param file_path: 文件路径
    @param default_val: 没有找到路径的默认值
    @param find_deep: 查找深度
    @return:
    """
    if file_path is None:
        return default_val

    if os.path.exists(file_path):
        return os.path.normpath(file_path)

    for i in range(find_deep):
        file_path = os.path.join("..", file_path)
        if os.path.exists(file_path):
            return os.path.normpath(file_path)

    return default_val


def calculate_distance(pos1, pos2=[0, 0, 0]):
    """
    计算两点间的距离
    @param pos1:
    @param pos2:
    @return:
    """
    d = pow(pow(np.array(pos1[0]) - np.array(pos2[0]), 2) +
            pow(np.array(pos1[1]) - np.array(pos2[1]), 2) +
            pow(np.array(pos1[2]) - np.array(pos2[2]), 2), 1 / 2)
    return d


def get_acceleration_info(acceleration):
    """

    @param acceleration: 加速度的值（km/s²）
    @return:
    """
    if isinstance(acceleration, list) or isinstance(acceleration, np.ndarray):
        from simulators.ursina.entities.entity_utils import get_value_direction_vectors
        acc_value, direction = get_value_direction_vectors(acceleration)
    else:
        acc_value = acceleration

    acc_m = acc_value * 1000  # 加速度的值（m/s²）

    if acc_m >= 0.01:
        acc_info = "%.2f m/s²" % (acc_m)
    elif acc_m >= 0.00001:
        acc_info = "%.2f mm/s²" % (acc_m * 1000)
    # elif acc_m >= 0.00000001:
    #     acc_info = "%.2fμm/s²" % (acc_m * 1000 * 1000)
    else:
        acc_info = "0 m/s²"
    return acc_info


def find_intersection(sphere_center, sphere_radius, line_start_pos, line_end_pos):
    """
    计算线段与球体表面的交点坐标
     参数:
    sphere_center (tuple): 球体中心位置的三维坐标 (x, y, z)
    sphere_radius (float): 球体的半径
    line_start_pos (tuple): 线段的起始位置的三维坐标 (x, y, z)
    line_end_pos (tuple): 线段的结束位置的三维坐标 (x, y, z)
     返回:
    tuple: 交点的三维坐标 (x, y, z)，如果没有交点则返回None
    """
    # 计算线段的方向向量
    line_direction = (
        line_end_pos[0] - line_start_pos[0],
        line_end_pos[1] - line_start_pos[1],
        line_end_pos[2] - line_start_pos[2]
    )
    # 计算线段的长度
    line_length = math.sqrt(
        line_direction[0] ** 2 +
        line_direction[1] ** 2 +
        line_direction[2] ** 2
    )
    # 将线段方向向量归一化
    line_direction = (
        line_direction[0] / line_length,
        line_direction[1] / line_length,
        line_direction[2] / line_length
    )
    # 计算线段起始位置到球心的向量
    start_to_center = (
        sphere_center[0] - line_start_pos[0],
        sphere_center[1] - line_start_pos[1],
        sphere_center[2] - line_start_pos[2]
    )
    # 计算线段起始位置到球心的距离
    distance = (
            start_to_center[0] * line_direction[0] +
            start_to_center[1] * line_direction[1] +
            start_to_center[2] * line_direction[2]
    )
    # 如果距离小于0，则线段与球体没有交点
    if distance < 0:
        return None
    # 计算最短距离的投影点坐标
    closest_point = (
        line_start_pos[0] + distance * line_direction[0],
        line_start_pos[1] + distance * line_direction[1],
        line_start_pos[2] + distance * line_direction[2]
    )
    # 计算最短距离的投影点到球心的距离
    closest_distance = math.sqrt(
        (closest_point[0] - sphere_center[0]) ** 2 +
        (closest_point[1] - sphere_center[1]) ** 2 +
        (closest_point[2] - sphere_center[2]) ** 2
    )
    # 如果最短距离大于球体半径，则线段与球体没有交点
    if closest_distance > sphere_radius:
        return None
    # 计算交点坐标
    intersection = (
        closest_point[0] + (sphere_radius - closest_distance) * line_direction[0],
        closest_point[1] + (sphere_radius - closest_distance) * line_direction[1],
        closest_point[2] + (sphere_radius - closest_distance) * line_direction[2]
    )
    return intersection


if __name__ == '__main__':
    sphere_center = (0, 0, 0)
    sphere_radius = 1
    line_start_pos = (-1, 0, 0)
    line_end_pos = (1, 0, 0)
    intersection = find_intersection(sphere_center, sphere_radius, line_start_pos, line_end_pos)
    print(intersection)
#
# def calculate_velocity(mass, semimajor_axis, eccentricity):
#     """
#     计算天体在椭圆轨道上的速度。
#
#     参数：
#         - mass: 天体质量，单位 kg
#         - semimajor_axis: 轨道半长轴，单位 m
#         - eccentricity: 轨道离心率
#
#     返回值：
#         天体在轨道上的速度，单位 m/s。
#     """
#     # 计算轨道的半短轴和半焦距
#     semiminor_axis = semimajor_axis * math.sqrt(1 - eccentricity ** 2)
#     focus_distance = semimajor_axis * eccentricity
#
#     # 计算轨道的第一和第二离心率角
#     theta = math.atan2(focus_distance, semiminor_axis)
#     psi = math.atan2(math.sqrt(1 - eccentricity ** 2) * math.sin(theta), eccentricity + math.cos(theta))
#
#     # 计算轨道的速率
#     v = math.sqrt(G * mass * (2 / semimajor_axis - 1 / semiminor_axis))
#
#     # 计算天体在轨道上的速度，注意要考虑太阳的质量
#     return v * math.sqrt(1 + (2 * mass) / (v ** 2 * AU)) * math.sin(psi)

#
# def get_lagrange_points(m1, m2, r, R, omega):
#     """
#     函数需要5个输入参数：
#
#     m1: 大质点的质量（单位：kg）
#     m2: 小质点的质量（单位：kg）
#     r: 小质点到拉格朗日点的距离（单位：km）
#     R: 大质点到拉格朗日点的距离（单位：km）
#     omega: 两个星体之间的夹角（单位：rad）
#     函数返回一个元组，其中包括五个元素（Tuple），每个元素又是由七个数据（Tuple）组成：
#
#     @param m1:
#     @param m2:
#     @param r:
#     @param R:
#     @param omega:
#     @return:
#     x: 拉格朗日点的x坐标（单位：km）
#     y: 拉格朗日点的y坐标（单位：km）
#     z: 拉格朗日点的z坐标（单位：km）
#     vx: 拉格朗日点物体的x方向速度（单位：km/s）
#     vy: 拉格朗日点物体的y方向速度（单位：km/s）
#     vz: 拉格朗日点物体的z方向速度（单位：km/s）
#     """
#     G = 6.673e-20  # gravitational constant in km^3/kg*s^2
#     M = m1 + m2
#
#     # Calculate mass ratio
#     mu = m2 / M
#
#     # Calculate distance between primary and secondary bodies
#     d = np.sqrt((R * mu) ** 2 + r ** 2 - 2 * R * r * mu * np.cos(omega))
#
#     # Calculate L1 point
#     a = (d - R) / (2 - mu)
#     x1 = R - a
#     y1 = 0
#     z1 = 0
#     v1 = np.sqrt(G * m2 * a / d) * (1 - mu)
#     vx1 = 0
#     vy1 = v1 * (R - x1) / d
#     vz1 = v1 * y1 / d
#
#     # Calculate L2 point
#     a = (d - R) / (2 - mu)
#     x2 = R + a
#     y2 = 0
#     z2 = 0
#     v2 = np.sqrt(G * m2 * a / d) * (1 - mu)
#     vx2 = 0
#     vy2 = v1 * (R - x2) / d
#     vz2 = v1 * y2 / d
#
#     # Calculate L3 point
#     a = (d + R) / (2 + mu)
#     x3 = -a
#     y3 = 0
#     z3 = 0
#     v3 = np.sqrt(G * m1 * a / d) * (1 + mu)
#     vx3 = 0
#     vy3 = v3 * (R - x3) / d
#     vz3 = v3 * -y3 / d
#
#     # Calculate L4 and L5 points
#     x4, y4, z4, v4, vx4, vy4, vz4 = get_l4_l5_points(m1, m2, R, omega, 1)
#     x5, y5, z5, v5, vx5, vy5, vz5 = get_l4_l5_points(m1, m2, R, omega, -1)
#
#     return ((x1, y1, z1, vx1, vy1, vz1),
#             (x2, y2, z2, vx2, vy2, vz2),
#             (x3, y3, z3, vx3, vy3, vz3),
#             (x4, y4, z4, vx4, vy4, vz4),
#             (x5, y5, z5, vx5, vy5, vz5))
#
#
# def get_l4_l5_points(m1, m2, R, omega, sign):
#     # G = 6.673e-20  # gravitational constant in km^3/kg*s^2
#     M = m1 + m2
#
#     # Calculate mass ratio
#     mu = m2 / M
#
#     # Calculate position of L4 or L5 point
#     x = R * np.cos(omega + sign * 60 * np.pi / 180)
#     y = R * np.sin(omega + sign * 60 * np.pi / 180)
#     z = 0
#
#     # Calculate velocity of L4 or L5 point
#     v = np.sqrt(G * M / (3 * R))
#     vx = -v * y / R
#     vy = v * x / R
#     vz = 0
#
#     return x, y, z, v, vx, vy, vz
#
#
# def get_v(M, m, r):
#     import math
#
#     G = 6.67e-11  # 引力常数，单位为N·m²/kg²
#     v = math.sqrt(G * M / r)  # 计算地球的线速度，单位为米/秒
#     return v
#
#
# if __name__ == '__main__':
#     M = 5.97237e24
#     r = 363104*1000
#     m = 5.97e24
#     print(get_v(M, m, r))
# import math
#
# G = 6.67e-11  # 引力常数，单位为N·m²/kg²
# M = 1.99e30  # 太阳质量，单位为kg
# # m = 5.97e24  # 地球质量，单位为kg
# r = 1.5e11  # 地球到太阳的距离，单位为米
#
# v = math.sqrt(G * M / r)  # 计算地球的线速度，单位为米/秒
#
# print("天体的线速度为：%.2f 公里/秒" % (v / 1000))
#     # print(calculate_distance([6, 8, 0], [3, 4, 0]))
#     # print(find_file("common/func.py"))
#
#     # 使用地球数据测试
#     mass_earth = 5.972e24
#     semimajor_axis_earth = AU
#     eccentricity_earth = 0.0167
#
#     velocity_earth = calculate_velocity(mass_earth, semimajor_axis_earth, eccentricity_earth)
#
#     print("地球在轨道上的速度是：{:.2f} km/s".format(velocity_earth / 1000))
#
# """
# 你现在是一位资深的天体学家、请使用python完成一个获取拉格朗日点的函数，获取拉格朗日点的坐标(px,py 单位：km)同时，也要返回拉格朗日点物体的速度（vx,vy 单位：km/s）,需要返回L1-L5所有的点和速度。返回的L1、L2、L3、L4、L5 格式为：(x1, y1, vx1, vy1),(x2, y2, vx2, vy2), (x3, y3, vx3, vy3), (x4, y4, vx4, vy4) (x5, y5, vx5, vy5)，并针对太阳、地球拉格朗日点以及 地球、月球拉格朗日点举例。并使用matlibplot画图，并写上详细的注释。
# """
