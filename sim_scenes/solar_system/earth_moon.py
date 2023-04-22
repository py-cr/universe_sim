# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from bodies.body import AU
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent

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
             init_velocity=[-1.03, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
    ]


    def on_ready():
        # 运行前触发
        # 运行开始前，将摄像机指向地球
        earth = bodies[0]
        moon = bodies[1]
        # 摄像机看向地球
        camera_look_at(earth)
        # 创建太阳光
        shadows_shader = create_directional_light(position=(200, 0, -300), target=earth,shadows=True)
        earth.planet.shadows = shadows_shader
        moon.planet.shadows = shadows_shader


    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY,
               position=(-300000, 1500000, -1000),
               show_timer=True,
               show_trail=True)
