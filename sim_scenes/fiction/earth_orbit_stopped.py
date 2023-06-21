# -*- coding:utf-8 -*-
# title           :如果地球停止公转
# description     :如果地球停止公转，那它需要多久才会掉进太阳？ 大约65天
# author          :Python超人
# date            :2023-06-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at, two_bodies_colliding, set_camera_parent
from bodies.body import AU
from simulators.ursina.entities.body_timer import BodyTimer
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import application, camera, Vec3
import math

if __name__ == '__main__':
    """
    地球停止公转，多久到达太阳
    地球如果停止公转，多久能掉入太阳？
    https://www.zhihu.com/question/310815418
    如果地球停止公转，那它需要多久才会掉进太阳？
    https://www.guokr.com/article/440341
    
    """
    # 地球的Y方向初始速度
    EARTH_INIT_VELOCITY = 0  # 0km/s
    sun = Sun(init_position=[AU/math.sqrt(2),0, AU/math.sqrt(2)], size_scale=1)
    sun = Sun(init_position=[0, 0, AU], size_scale=1)
    earth = Earth(init_position=[0, 0, 0],
                  init_velocity=[0, EARTH_INIT_VELOCITY, 0],
                  size_scale=1).set_light_disable(True)
    bodies = [
        sun,
        earth
    ]


    def on_ready():
        # 运行前触发
        application.time_scale = 0.01
        camera.fov = 50


    def on_timer_changed(time_data):

        if time_data.total_days < 18:
            fov_offset = 0.1
        elif time_data.total_days < 30:
            fov_offset = 0.04
        elif time_data.total_days < 40:
            fov_offset = 0.02
        else:
            fov_offset = 0

        if time_data.total_minutes % 3 == 0 and camera.fov > 1.5:
            camera.fov -= fov_offset
        camera_look_at(earth,rotation_z=0)

        if two_bodies_colliding(sun, earth):
            ControlUI.current_ui.show_message("地球已到达太阳表面", close_time=-1)
            application.pause()

    # 设置计时器的最小时间单位为分钟
    BodyTimer().min_unit = BodyTimer.MIN_UNIT_HOURS

    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 订阅事件后，上面的函数功能才会起作用
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    # position=(0, 0, 0) 的位置是站在地球视角，可以观看月相变化的过程
    ursina_run(bodies, SECONDS_PER_DAY, position=(0, 0.002 * AU, -0.002 * AU),
               show_timer=True,
               show_grid=True)
