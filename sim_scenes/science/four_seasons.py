# -*- coding:utf-8 -*-
# title           :太阳、地球场景模拟
# description     :太阳、地球场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Sirius
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera

if __name__ == '__main__':
    """
    太阳、地球
    """
    bodies = [
        Sun(size_scale=5e1, texture="transparent.png"),  # 太阳透明
        Earth(name="中国春天", size_scale=6e3, texture="earth_hd.jpg", text_color=(0, 255, 0),
              init_position=[-1 * AU, 0, 0], init_velocity=[0, 0, -29.79]),
        Earth(name="中国夏天", size_scale=6e3, texture="earth_hd.jpg", text_color=(255, 0, 0),
              init_position=[0, 0, -1 * AU], init_velocity=[29.79, 0, 0]),
        Earth(name="中国秋天", size_scale=6e3, texture="earth_hd.jpg", text_color=(255, 255, 0),
              init_position=[1 * AU, 0, 0], init_velocity=[0, 0, 29.79]),
        Earth(name="中国冬天", size_scale=6e3, texture="earth_hd.jpg", text_color=(0, 255, 255),
              init_position=[0, 0, 1 * AU], init_velocity=[-29.79, 0, 0]),
    ]
    sun = bodies[0]
    earth_1 = bodies[1]
    earth_2 = bodies[2]
    earth_3 = bodies[3]
    earth_4 = bodies[4]


    def on_ready():
        # 摄像机跟随地球（模拟在地球上看到的效果）
        # camera.position = earth.planet.position
        # camera.forward = -10 * AU
        # # camera.x = camera.x - AU / 100
        # camera.look_at(earth.planet)
        earth_1.planet.rotation_y += 115  # 春天
        earth_2.planet.rotation_y += 15  # 夏天
        earth_3.planet.rotation_y -= 80  # 秋天
        earth_4.planet.rotation_y -= 145  # 冬天

        # camera.parent = sun.planet
        camera.look_at(earth_4.planet)
        camera.rotation_z = 0
        # camera.position=[0,0,0]
        pass

        # if hasattr(camera, "sky"):
        #     # 摄像机跟随地球后，需要对深空背景进行调整，否则看到的是黑色背景
        #     camera.sky.scale = 800
        #     camera.clip_plane_near = 0.1
        #     camera.clip_plane_far = 1000000
        #     # camera.fov = 40


    def on_timer_changed(time_data: TimeData):
        # 时时刻刻的让地球看向太阳（摄像机跟随地球看向太阳）
        # earth.planet.look_at(sun.planet)
        # earth.planet.rotation_z = 0
        # camera.look_at(earth.planet)
        pass


    UrsinaEvent.on_ready_subscription(on_ready)
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, 1, position=(0, 0, 0),
               show_name=True,
               show_trail=True)
