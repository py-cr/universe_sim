# -*- coding:utf-8 -*-
# title           :彗木保护地球模拟
# description     :彗木保护地球模拟
# author          :Python超人
# date            :2023-06-27
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Jupiter, Earth
from objs import RockSnow, Rock, create_rock
from common.consts import SECONDS_PER_MONTH, SECONDS_PER_YEAR
from sim_scenes.func import ursina_run, camera_look_at, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent
import random


def create_comet(index, raduis):
    """
    随机生成石头（随机位置、随机初始速度、随机大小、随机旋转）
    @param index: 索引号
    @param raduis: 木星的半径，保证生成的石头在木星半径外
    @param gravity_only_for: 指定一个天体，石头只对该天体引力有效
    @return:
    """
    # 随机生成石头的位置和初始速度信息
    pos = [-raduis * random.randint(120, 200) / 100,
           -raduis * random.randint(120, 200) / 1000,
           -raduis * random.randint(100, 300) / 100]
    # 随机速度
    vel = [-random.randint(90, 200) / 300, 0, 0]
    # vel = [0, 0, 0]
    # 石头随机大小
    size_scale = random.randint(600, 1200) * 2e4
    # 随机创建石头
    rock = create_rock(
        no=index % 8 + 1, name=f'岩石{index + 1}', mass=4.4e10,
        size_scale=size_scale, color=(255, 200, 0),
        init_position=pos, init_velocity=vel,
    )

    # 给石头一个随机旋转的方向和值
    rock.rotation = [0, 0, 0]
    rock.rotation[random.randint(0, 2)] = random.randint(90, 200) / 100
    return rock


if __name__ == '__main__':
    """
    彗木保护地球模拟
    """
    sun = Sun(name="太阳", size_scale=0.8e2)  # 太阳放大 80 倍，距离保持不变
    jupiter = Jupiter(name="木星", size_scale=0.6e3)  # 木星放大 600 倍，距离保持不变
    earth = Earth(name="地球", size_scale=2e3)  # 地球放大 2000 倍，距离保持不变
    bodies = [sun, jupiter, earth]

    for body in bodies:
        body.rotation_speed /= 20  # 自转速度降低100倍

    comets = []

    for i in range(15):
        # 随机生成石头
        comet = create_comet(i, jupiter.position[2] * 2)
        bodies.append(comet)
        comets.append(comet)


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
                elif two_bodies_colliding(comet, sun):
                    # 将石头隐藏、设置引力无效后，展示爆炸效果
                    comet.explode(sun)
                elif two_bodies_colliding(comet, earth):
                    # 将石头隐藏、设置引力无效后，展示爆炸效果
                    comet.explode(earth)

        # def on_reset():
        """
        当按键盘的 “O” 键重置后，恢复所有石头的状态（石头可见、引力有效），这样就可以反复观看
        @return:
        """
        # for comet in comets:
        #     comet.set_visible(True)
        #     comet.ignore_mass = False


    def on_ready():
        # 运行前触发
        # 为了较好的立体效果，可以增加太阳光线，光线指向木星（target=jupiter）
        create_directional_light(position=(200, 0, -300), light_num=3, target=jupiter)
        # 摄像机看向木星
        camera_look_at(jupiter, rotation_z=0)


    # 订阅事件后，上面3个函数功能才会起作用
    # 按键盘的 “O” 重置键会触发 on_reset
    # UrsinaEvent.on_reset_subscription(on_reset)
    # 运行前会触发 on_ready
    # UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_YEAR,
               position=(30000000, 0, -3000000000),
               show_timer=True)
