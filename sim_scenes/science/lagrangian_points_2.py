# -*- coding:utf-8 -*-
# title           :拉格朗日点模拟
# description     :拉格朗日点模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Body, Sun, Earth, Moon
from objs import Obj, Satellite, Satellite2
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent
from simulators.ursina.ursina_mesh import create_line
import math

bodies = [
    Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
          init_velocity=[0, 0, 0], size_scale=0.5e1),  # 地球放大 5 倍，距离保持不变
    Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
         init_velocity=[-1.054152222, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
]

earth = bodies[0]
moon = bodies[1]


# 计算地月拉格朗日点
# L1_p, L2_p, L3_p, L4_p, L5_p = get_lagrangian_points(earth.mass, moon.mass, 363104)

def create_satellite(name, init_position, init_velocity):
    """
    在 L1, L2, L3, L4, L5 创建卫星
    @param name:
    @param init_position:
    @param init_velocity:
    @return:
    """
    satellite = Satellite(name=name, mass=1.4e10, size_scale=4e3, color=(255, 200, 0),
                          init_position=init_position,
                          init_velocity=init_velocity, gravity_only_for=[earth, moon])
    return satellite


# L1：point=[0,0,308536.70059015526]  velocity=[-0.890136271716, 0, 0]
satelliteL1 = create_satellite(name=f'卫星L1', init_position=[0, 0, 308536.672],
                               init_velocity=[-0.890136271716, 0, 0])
bodies.append(satelliteL1)

# L2：point=[0,0, 423338.5083198447]  velocity=[-1.24, 0, 0]
satelliteL2 = create_satellite(name=f'卫星L2', init_position=[0, 0, 423338.5083198447],
                               init_velocity=[-1.24, 0, 0])
bodies.append(satelliteL2)

vel_L345 = 1.048
# L3：point=[0,0, -364941.3043941873]  velocity=[1.039 , 0, 0]
satelliteL3 = create_satellite(name=f'卫星L3', init_position=[0, 0, -364941.3043941873],
                               init_velocity=[vel_L345, 0, 0])
bodies.append(satelliteL3)

# L4：point=[0,0, 177142.46945395062]  velocity=[1.039 , 0, 0]
satelliteL4 = create_satellite(name=f'卫星L4', init_position=[314457.2882157448, 0, 177142.46945395062],
                               init_velocity=[-math.sin(math.pi * 30 / 180) * vel_L345, 0,
                                              math.cos(math.pi * 30 / 180) * vel_L345])
bodies.append(satelliteL4)

# L5：point=[0,0, 177142.46945395062]  velocity=[1.039 , 0, 0]
satelliteL5 = create_satellite(name=f'卫星L5', init_position=[-314457.2882157448, 0, 177142.46945395062],
                               init_velocity=[-math.sin(math.pi * 30 / 180) * vel_L345, 0,
                                              -math.cos(math.pi * 30 / 180) * vel_L345])
bodies.append(satelliteL5)


def create_connecting_lines(satellites_list):
    """
    创建连接线（将卫星列表用线条连接起来）
    @param satellites_list:
    @return:
    """
    lines = []
    for satellites in satellites_list:
        line = create_line(from_pos=satellites[0].planet.position,
                           to_pos=satellites[1].planet.position, alpha=0.3)
        lines.append(line)
    return lines


if __name__ == '__main__':
    def on_ready():
        # 运行前触发
        # 摄像机看向地球
        camera_look_at(earth)


    def on_timer_changed(time_data: TimeData):
        # 删除和创建连接线
        from ursina import destroy
        if hasattr(earth, "lines"):
            for line in earth.lines:
                destroy(line)

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

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR * 5,
               # position=(-300000, 1500000, -100),
               position=(0, 1500000, 0),
               show_timer=True,
               # show_trail=True
               )
