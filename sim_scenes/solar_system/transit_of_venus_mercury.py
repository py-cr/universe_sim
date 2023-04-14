# -*- coding:utf-8 -*-
# title           :水星、金星凌日
# description     :水星、金星凌日
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_HOUR, AU
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    # 水星、金星凌日
    earth = Earth(name="地球", rotation_speed=0, texture="transparent.png")  # 地球纹理透明，不会挡住摄像机视线
    sun = Sun(name="太阳", size_scale=5e1)  # 太阳放大 50 倍
    bodies = [
        sun,
        earth,
        Mercury(name="水星",
                init_position=[0.384 * AU, 0, 0],
                init_velocity=[0, 0, 47.87],
                size_scale=5e1),  # 水星放大 50 倍，距离保持不变
        Venus(name="金星",
              init_position=[0.721 * AU, 0, 0],
              init_velocity=[0, 0, 35],
              size_scale=5e1)  # 金星放大 50 倍，距离保持不变
    ]


    def on_ready():
        from ursina import camera
        # 摄像机跟随地球（模拟在地球上看到的效果）
        camera.parent = earth.planet

        if hasattr(camera, "sky"):
            # 摄像机跟随地球后，需要对深空背景进行调整，否则看到的是黑色背景
            camera.sky.scale = 800
            camera.clip_plane_near = 0.1
            camera.clip_plane_far = 1000000

        # 让太阳的旋转速度放慢10倍
        sun.rotation_speed /= 10


    def on_timer_changed(time_data: TimeData):
        # 时时刻刻的让地球看向太阳（摄像机跟随地球看向太阳）
        earth.planet.look_at(sun.planet)
        earth.planet.rotation_z = 0


    UrsinaEvent.on_ready_subscription(on_ready)
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK,
               position=[0, 0, 0],  # 以地球为中心的位置
               show_timer=True)
