# -*- coding:utf-8 -*-
# title           :地月拉格朗日点模拟
# description     :地月拉格朗日点模拟(理想的拉格朗日点位置)
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth, Moon
from objs import Satellite, Satellite2
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent
from simulators.ursina.ursina_mesh import create_connecting_lines
import math


def get_lagrangian_points(m1, m2, r):
    """
    用于计算理想的拉格朗日点
    @param m1: 大天体的质量
    @param m2: 小天体的质量
    @param r: 小天体绕大天体的半径
    @return: 返回拉格朗日点 L1, L2, L3, L4, L5 的坐标
    """
    a = m2 / (m1 + m2)
    l1 = (0, 0, r * (1 - pow(a / 3, 1 / 3)))
    l2 = (0, 0, r * (1 + pow(a / 3, 1 / 3)))
    l3 = (0, 0, -r * (1 + (5 * a) / 12))
    l4 = (pow(3, 1 / 2) / 2 * r, 0, (r / 2) * ((m1 - m2) / (m1 + m2)))
    l5 = (-pow(3, 1 / 2) / 2 * r, 0, (r / 2) * ((m1 - m2) / (m1 + m2)))

    return l1, l2, l3, l4, l5


# 月球绕地球的半径
R = 363104
# 创建地月
earth = Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
              init_velocity=[0, 0, 0], size_scale=0.8e1)  # 地球放大 8 倍，地月距离保持不变
moon = Moon(init_position=[0, 0, R],  # 距地距离约: 363104 至 405696 km
            init_velocity=[-1.054152222, 0, 0], size_scale=1.2e1)  # 月球放大 12 倍，地月距离保持不变

# 获取地月拉格朗日点(理想数据)
L1_p, L2_p, L3_p, L4_p, L5_p = get_lagrangian_points(earth.mass, moon.mass, R)


# region 在拉格朗日点 L1, L2, L3, L4, L5 上创建卫星

def create_satellite(name, init_position, init_velocity):
    """
    在指定位置创建卫星，并给予卫星一个初速度
    @param name: 卫星名称
    @param init_position: 初始位置
    @param init_velocity: 初始速度
    @return:
    """
    satellite = Satellite(name=name, mass=1.4e10, size_scale=2e3, color=(255, 200, 0),
                          init_position=init_position,
                          init_velocity=init_velocity, gravity_only_for=[earth, moon])
    return satellite


# 在 L1 位置上创建一个具有初速度的卫星
satelliteL1 = create_satellite(name=f'卫星L1', init_position=L1_p,
                               init_velocity=[-0.890136271716, 0, 0])
# 在 L2 位置上创建一个具有初速度的卫星
satelliteL2 = create_satellite(name=f'卫星L2', init_position=L2_p,
                               init_velocity=[-1.24, 0, 0])
vel_L345 = 1.048
# 在 L3 位置上创建一个具有初速度的卫星
satelliteL3 = create_satellite(name=f'卫星L3', init_position=L3_p,
                               init_velocity=[vel_L345, 0, 0])
# 在 L4 位置上创建一个具有初速度的卫星
satelliteL4 = create_satellite(name=f'卫星L4', init_position=L4_p,
                               init_velocity=[-math.sin(math.pi * 30 / 180) * vel_L345, 0,
                                              math.cos(math.pi * 30 / 180) * vel_L345])
# 在 L5 位置上创建一个具有初速度的卫星
satelliteL5 = create_satellite(name=f'卫星L5', init_position=L5_p,
                               init_velocity=[-math.sin(math.pi * 30 / 180) * vel_L345, 0,
                                              -math.cos(math.pi * 30 / 180) * vel_L345])
# endregion


if __name__ == '__main__':
    def on_ready():
        # 运行前触发
        # 摄像机看向地球
        camera_look_at(earth)


    def on_timer_changed(time_data: TimeData):
        # 实时删除和创建连接线
        from ursina import destroy
        if hasattr(earth, "lines"):
            for line in earth.lines:
                destroy(line)
        # 创建连接线（将卫星列表用线条连接起来）
        earth.lines = create_connecting_lines([
            [satelliteL2, satelliteL3],
            [satelliteL4, satelliteL1], [satelliteL5, satelliteL1],
            [satelliteL4, satelliteL2], [satelliteL5, satelliteL2],
            [satelliteL4, satelliteL3], [satelliteL5, satelliteL3],
        ])


    # 订阅事件后，上面的函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    bodies = [earth, moon,
              satelliteL1, satelliteL2, satelliteL3, satelliteL4, satelliteL5]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR * 5,
               position=(0, 1500000, 0),
               show_timer=True,
               # show_trail=True
               )
