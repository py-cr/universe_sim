# -*- coding:utf-8 -*-
# title           :地球和卫星模拟
# description     :地球和卫星模拟
# author          :Python超人
# date            :2023-04-09
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from objs import Satellite, Satellite2
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    地球和卫星模拟
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])

    bodies = [earth]
    # 卫星位置和初始速度信息
    satellite_infos = [
        {"position": [0, 0, 10002], "velocity": [6.3, 0, 0]},
        {"position": [0, 0, -12000], "velocity": [5.75, 0, 0]},
        {"position": [0, 8000, 0], "velocity": [7.05, 0, 0]},
        {"position": [0, -12002, 0], "velocity": [5.75, 0, 0]},
        {"position": [0, 0, 8002], "velocity": [0, 7.05, 0]},
        {"position": [0, 0, -10000], "velocity": [0, 6.3, 0]},
    ]
    for i, info in enumerate(satellite_infos):
        satellite = Satellite(name=f'卫星{i + 1}', mass=4.4e10, size_scale=1e2, color=(255, 200, 0),
                              init_position=info["position"],
                              init_velocity=info["velocity"])
        info["satellite"] = satellite
        bodies.append(satellite)


    def on_ready():
        camera_look_at(earth, rotation_z=0)
        UrsinaConfig.trail_length = 150
        UrsinaConfig.trail_type = "line"
        pass


    def on_timer_changed(time_data: TimeData):
        for info in satellite_infos:
            info["satellite"].planet.look_at(earth.planet)


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(30000, 10000, -20000),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001
