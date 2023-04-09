# -*- coding:utf-8 -*-
# title           :公共库函数
# description     :公共库函数
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from PIL import Image
from common.consts import AU
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

G = 6.67408e-11
# AU = 149597870700.0

def calculate_velocity(mass, semimajor_axis, eccentricity):
    """
    计算天体在椭圆轨道上的速度。

    参数：
        - mass: 天体质量，单位 kg
        - semimajor_axis: 轨道半长轴，单位 m
        - eccentricity: 轨道离心率

    返回值：
        天体在轨道上的速度，单位 m/s。
    """
    # 计算轨道的半短轴和半焦距
    semiminor_axis = semimajor_axis * math.sqrt(1 - eccentricity ** 2)
    focus_distance = semimajor_axis * eccentricity

    # 计算轨道的第一和第二离心率角
    theta = math.atan2(focus_distance, semiminor_axis)
    psi = math.atan2(math.sqrt(1 - eccentricity ** 2) * math.sin(theta), eccentricity + math.cos(theta))

    # 计算轨道的速率
    v = math.sqrt(G * mass * (2 / semimajor_axis - 1 / semiminor_axis))

    # 计算天体在轨道上的速度，注意要考虑太阳的质量
    return v * math.sqrt(1 + (2 * mass) / (v ** 2 * AU)) * math.sin(psi)


if __name__ == '__main__':
    # print(calculate_distance([6, 8, 0], [3, 4, 0]))
    # print(find_file("common/func.py"))

    # 使用地球数据测试
    mass_earth = 5.972e24
    semimajor_axis_earth = AU
    eccentricity_earth = 0.0167

    velocity_earth = calculate_velocity(mass_earth, semimajor_axis_earth, eccentricity_earth)

    print("地球在轨道上的速度是：{:.2f} km/s".format(velocity_earth / 1000))