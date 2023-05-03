# -*- coding:utf-8 -*-
# title           :地月球场景模拟
# description     :地球、6个月球场景模拟
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY
from sim_scenes.func import ursina_run, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    地球、6个月球
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                  rotation_speed=0, texture="earth_hd.jpg")
    D = earth.diameter * 1.2
    init_vel = 5.116
    # 在地球周围创建 6 个月球（初速度为0）
    bodies = [
        earth,
        Moon(init_position=[D, 0, 0], init_velocity=[0, 0, init_vel]),  # 月球在地球右面
        Moon(init_position=[-D, 0, 0], init_velocity=[0, 0, -init_vel]),  # 月球在地球左面
        Moon(init_position=[0, D, 0], init_velocity=[init_vel, 0, 0]),  # 月球在地球上面
        Moon(init_position=[0, -D, 0], init_velocity=[-init_vel, 0, 0]),  # 月球在地球下面
        Moon(init_position=[0, 0, D], init_velocity=[0, init_vel, 0]),  # 月球在地球前面
        Moon(init_position=[0, 0, -D], init_velocity=[0, -init_vel, 0]),  # 月球在地球后面
    ]

    moons = bodies[1:]


    def on_reset():
        """
        当按键盘的 “O” 键重置后，恢复所有抛出物的状态（引力有效），这样就可以反复观看
        @return:
        """
        for moon in moons:
            moon.ignore_mass = False


    def on_timer_changed(time_data: TimeData):
        """
        在运行中，每时每刻都会触发，对抛出物与地球的碰撞进行判断，如果碰到地球，则停止运动
        @param time_data:
        @return:
        """
        for moon in moons:
            # 循环判断每个抛出物与地球是否相碰撞
            if two_bodies_colliding(moon, earth):
                # 如果抛出物与地球相碰撞了，则静止不动（抛出物停止并忽略引力）
                moon.stop_and_ignore_gravity()


    # 订阅事件后，上面2个函数功能才会起作用
    # 按键盘的 “O” 重置键会触发 on_reset
    UrsinaEvent.on_reset_subscription(on_reset)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(0, 0, -4 * earth.diameter),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001
