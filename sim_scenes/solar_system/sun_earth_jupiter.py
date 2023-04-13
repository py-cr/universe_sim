# -*- coding:utf-8 -*-
# title           :太阳、地球、木星场景模拟
# description     :太阳、地球、木星场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Jupiter
from common.consts import SECONDS_PER_YEAR, SECONDS_PER_MONTH, AU
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from simulators.ursina.ursina_mesh import create_line
from ursina import color

if __name__ == '__main__':
    """
    太阳、地球、木星
    """

    bodies = [
        Sun(size_scale=5e1),                        # 太阳放大 50 倍
        Earth(size_scale=2e3, distance_scale=1),    # 地球放大 2000 倍，距离保持不变
        Jupiter(size_scale=5e2, distance_scale=1),  # 木星放大 500 倍，距离保持不变
    ]
    sun, earth, jupiter = bodies[0], bodies[1], bodies[2]


    def on_ready():
        camera_look_at(sun, rotation_x=None, rotation_y=None, rotation_z=None)
        UrsinaConfig.trail_length = 235
        UrsinaConfig.trail_type = "line"
        pass


    def on_timer_changed(time_data: TimeData):
        if int(time_data.total_days) % 10 == 0:
            # print(time_data.total_hours)
            create_line(from_pos=jupiter.planet.position, to_pos=earth.planet.position, color=color.white)


    UrsinaEvent.on_ready_subscription(on_ready)
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_YEAR, position=(0, 20 * AU, 0), show_timer=True, show_trail=True)
