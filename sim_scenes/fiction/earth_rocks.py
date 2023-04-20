# -*- coding:utf-8 -*-
# title           :岩石坠落地球
# description     :岩石坠落地球
# author          :Python超人
# date            :2023-04-09
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth, Body
from objs import RockSnow, Rock, create_rock
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY
from sim_scenes.func import ursina_run, camera_look_at, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    岩石坠落地球
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                  rotation_speed=0, size_scale=1, texture="earth_hd.jpg")

    bodies = [earth]
    # 岩石位置和初始速度信息
    infos = [
        {"position": [0, 0, 10002], "velocity": [4.5, 0, 0]},
        {"position": [0, 0, -12000], "velocity": [3.5, 0, 0]},
        {"position": [0, 8000, 0], "velocity": [4.5, 0, 0]},
        {"position": [0, -12002, 0], "velocity": [3.5, 0, 0]},
        {"position": [0, 18000, 0], "velocity": [3.0, 0, 0]},
        {"position": [-20000, 0, 0], "velocity": [0, -2.0, 0]},
        {"position": [0, 0, 18002], "velocity": [0, 2.5, 0]},
        {"position": [0, 0, -10000], "velocity": [0, 3.3, 0]},
    ]
    for i, info in enumerate(infos):
        rock = create_rock(no=i % 7 + 1, name=f'岩石{i + 1}', mass=4.4e10, size_scale=5e2, color=(255, 200, 0),
                           init_position=info["position"],
                           init_velocity=info["velocity"])
        info["rock"] = rock
        bodies.append(rock)


    def on_ready():
        camera_look_at(earth, rotation_z=0)
        UrsinaConfig.trail_length = 150
        UrsinaConfig.trail_type = "line"
        pass


    def on_timer_changed(time_data: TimeData):
        for obj in bodies:
            # 循环判断每个抛出物与地球是否相碰撞
            if two_bodies_colliding(obj, earth):
                # 如果抛出物与地球相碰撞了，则静止不动（抛出物停止并忽略引力）
                obj.stop_and_ignore_gravity()


    UrsinaEvent.on_ready_subscription(on_ready)
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 6,
               position=(30000, 10000, -20000),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
