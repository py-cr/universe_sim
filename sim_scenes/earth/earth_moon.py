# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟（月球对地球的扰动）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth, Moon
from common.consts import SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    月球对地球的扰动
    """
    OFFSETTING = 0
    # TODO: 可以抵消月球带动地球的力，保持地球在原地
    # OFFSETTING = 0.01265

    earth = Earth(init_position=[0, 0, 0],
                  init_velocity=[OFFSETTING, 0, 0], size_scale=0.5e1)  # 地球放大 5 倍，距离保持不变
    moon = Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
                init_velocity=[-1.03, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
    bodies = [earth, moon]


    def on_ready():
        # 运行前触发
        # 运行开始前，将摄像机指向地球

        # 摄像机看向地球
        camera_look_at(earth)


    # 订阅事件后，上面的函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK,
               position=(-300000, 1500000, -1000),
               show_timer=True,
               show_trail=True)
