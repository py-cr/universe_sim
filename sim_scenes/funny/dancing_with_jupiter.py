# -*- coding:utf-8 -*-
# title           :与木星跳舞
# description     :与木星跳舞
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Jupiter, Mars, Venus
from common.consts import SECONDS_PER_YEAR, SECONDS_PER_MONTH, AU
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from simulators.ursina.ursina_mesh import create_connecting_line

if __name__ == '__main__':
    """
    与木星跳舞
    """
    # 选择舞者
    # Dancer = Earth  # 舞者为地球
    # Dancer = Mars  # 舞者为火星

    sun = Sun(size_scale=0.8e2)  # 太阳放大 80 倍
    jupiter = Jupiter(size_scale=5e2)  # 木星放大 500 倍
    bodies = [sun, jupiter]

    dancers = [Earth(size_scale=5e3), Mars(size_scale=5e3)]  # 两个舞者放大 5000 倍
    dancers = [Earth(size_scale=5e3)]  # 舞者为地球，放大 5000 倍
    dancers = [Mars(size_scale=5e3)]  # 舞者为火星，放大 5000 倍

    bodies = bodies + dancers


    def on_ready():
        camera_look_at(sun)
        UrsinaConfig.trail_length = 235
        UrsinaConfig.trail_type = "line"
        pass


    def on_timer_changed(time_data: TimeData):
        if int(time_data.total_days) % 10 == 0:
            for dancer in dancers:
                line_color = dancer.color
                line_color = (255, 255, 100)
                create_connecting_line(jupiter, dancer, line_color=line_color)


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_YEAR,
               position=(0, 20 * AU, 0),
               show_timer=True,
               show_trail=True)
