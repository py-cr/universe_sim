# -*- coding:utf-8 -*-
# title           :岩石坠落木星
# description     :岩石坠落木星
# author          :Python超人
# date            :2023-04-09
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Jupiter, Body
from objs import RockSnow, Rock, create_rock
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY
from sim_scenes.func import ursina_run, camera_look_at, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    岩石坠落木星
    """
    import random

    # 木星在中心位置
    jupiter = Jupiter(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                      # rotation_speed=0,
                      size_scale=1, texture="jupiter_hd.jpg")

    bodies = [jupiter]
    rocks = []
    r = jupiter.raduis

    for i in range(30):
        # 随机生成岩石位置和初始速度信息
        pos = [-r * random.randint(120, 200) / 100,
               -r * random.randint(120, 200) / 1000,
               -r * random.randint(150, 350) / 100]
        # 随机速度
        vel = [0, -random.randint(90, 200) / 30, 0]
        size_scale = random.randint(400, 600)
        rock = create_rock(no=i % 7 + 1, name=f'岩石{i + 1}', mass=4.4e10, size_scale=size_scale, color=(255, 200, 0),
                           init_position=pos,
                           gravity_only_for=[jupiter],
                           init_velocity=vel)
        # 岩石随机旋转量
        rock.rotation = [0, 0, 0]
        rock.rotation[random.randint(0, 2)] = random.randint(90, 200) / 100

        bodies.append(rock)
        rocks.append(rock)


    def on_reset():
        for rock in rocks:
            rock.set_visible(True)
            rock.ignore_mass = False


    def on_ready():
        camera_look_at(jupiter, rotation_z=0)


    def on_timer_changed(time_data: TimeData):
        for rock in rocks:
            if rock.visibled:
                rock.planet.rotation += rock.rotation
                # 循环判断每个抛出物与木星是否相碰撞
                if two_bodies_colliding(rock, jupiter):
                    # 岩石爆炸
                    rock.explode(jupiter)


    UrsinaEvent.on_reset_subscription(on_reset)
    UrsinaEvent.on_ready_subscription(on_ready)
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 10,
               position=(0, 0, -300000),
               show_timer=True,
               view_closely=0.001)
