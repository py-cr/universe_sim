# -*- coding:utf-8 -*-
# title           :彗木相撞模拟
# description     :天象奇观：彗木相撞模拟
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
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent


def create_comet(index, gravity_only_for):
    """
    随机生成石头
    @param index: 索引号
    @param gravity_only_for: 指定一个天体，石头的引力只对该天体有效
    @return:
    """
    # 随机生成石头的位置和初始速度信息
    pos = [-r * random.randint(120, 200) / 100,
           -r * random.randint(120, 200) / 1000,
           -r * random.randint(100, 300) / 100]
    # 随机速度
    vel = [0, -random.randint(90, 200) / 30, 0]
    # 石头随机大小
    size_scale = random.randint(600, 1200)
    # 随机创建石头
    comet = create_rock(no=index % 8 + 1, name=f'岩石{index + 1}', mass=4.4e10,
                        size_scale=size_scale, color=(255, 200, 0),
                        init_position=pos, init_velocity=vel,
                        gravity_only_for=[gravity_only_for],
                        )

    # 给石头一个随机旋转的方向和值
    comet.rotation = [0, 0, 0]
    comet.rotation[random.randint(0, 2)] = random.randint(90, 200) / 100
    return comet


if __name__ == '__main__':
    """
    彗木相撞模拟
    """
    import random

    # 木星在中心位置
    jupiter = Jupiter(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                      size_scale=1, texture="jupiter_hd.jpg")

    bodies = [jupiter]
    comets = []
    r = jupiter.raduis

    for i in range(20):
        # 随机生成石头
        comet = create_comet(i, gravity_only_for=jupiter)
        bodies.append(comet)
        comets.append(comet)


    def on_reset():
        # 重置后恢复所有石头的状态（石头可见、引力有效）
        for comet in comets:
            comet.set_visible(True)
            comet.ignore_mass = False


    def on_ready():
        # 运行前触发
        # 创建太阳光
        create_directional_light(position=(200, 0, -300), target=jupiter)
        # 摄像机看向木星
        camera_look_at(jupiter, rotation_z=0)


    def on_timer_changed(time_data: TimeData):
        # 运行中，每时每刻都会触发
        for comet in comets:
            if comet.visibled:
                # 如果是否可见，则旋转石头
                comet.planet.rotation += comet.rotation
                # 循环判断每个石头与木星是否相碰撞，如果相碰撞就爆炸
                if two_bodies_colliding(comet, jupiter):
                    # 将石头隐藏、设置引力无效后，展示爆炸效果
                    comet.explode(jupiter)


    # 订阅事件
    UrsinaEvent.on_reset_subscription(on_reset)  # 重置了会触发 on_reset
    UrsinaEvent.on_ready_subscription(on_ready)  # 运行前会触发 on_ready
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)  # 运行中，每时每刻都会触发 on_timer_changed

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 10,
               position=(0, 0, -300000),
               show_timer=True,
               view_closely=0.001)
