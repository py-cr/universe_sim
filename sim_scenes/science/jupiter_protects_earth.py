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
from sim_scenes.func import ursina_run, camera_look_at, two_bodies_colliding, create_text_panel
from simulators.ursina.entities.body_timer import TimeData, BodyTimer
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent
import random
import math


class JupiterProtectsEarthSim:

    def __init__(self, comet_num=20):
        """

        @param comet_num: 随机生成 comet_num 个石头
        """
        self.colliding_count = [0, 0, 0, 0] # 分别保存太阳碰撞次数、木星碰撞次数、地球碰撞次数、木星保护次数
        self.sun = Sun(name="太阳", size_scale=0.8e2)  # 太阳放大 80 倍，距离保持不变
        self.jupiter = Jupiter(name="木星", size_scale=0.6e3)  # 木星放大 600 倍，距离保持不变
        self.earth = Earth(name="地球", size_scale=2e3)  # 地球放大 2000 倍，距离保持不变
        self.bodies = [self.sun, self.jupiter, self.earth]

        for body in self.bodies:
            body.rotation_speed /= 10  # 自转速度降低10倍

        self.comets = []

        self.comet_radius = self.jupiter.position[2] * 2

        for i in range(comet_num):
            # 随机生成 comet_num 个石头
            comet = self.create_comet(i, self.comet_radius, gravity_only_for=[self.sun, self.jupiter, self.earth])
            self.bodies.append(comet)
            self.comets.append(comet)

        # 显示板信息模板
        self.colliding_info = "太阳碰撞：%s次（%s）\n\n木星碰撞：%s次（%s）\n\n地球碰撞：%s次（%s）\n\n木星保护：%s次\n\n"

    def random_pos_vel(self, radius):
        # 随机生成石头的位置和初始速度信息
        # pos = [-radius * random.randint(120, 200) / 100,
        #        -radius * random.randint(120, 200) / 1000,
        #        -radius * random.randint(100, 300) / 100]

        x = radius * math.cos(random.uniform(0, 2 * math.pi)) * random.randint(80, 150) / 100
        z = radius * math.sin(random.uniform(0, 2 * math.pi)) * random.randint(80, 150) / 100
        pos = [x, 0, z]

        # 随机速度
        vel = [-random.randint(90, 200) / 300, 0, 0]
        return pos, vel

    def create_comet(self, index, radius, gravity_only_for):
        """
        随机生成石头（随机位置、随机初始速度、随机大小、随机旋转）
        @param index: 索引号
        @param radius: 木星的半径，保证生成的石头在木星半径外
        @param gravity_only_for: 指定一个天体，石头只对该天体引力有效
        @return:
        """
        # 随机生成石头的位置和初始速度信息
        pos, vel = self.random_pos_vel(radius)

        # vel = [0, 0, 0]
        # 石头随机大小
        size_scale = random.randint(600, 1200) * 1.5e4
        # 随机创建石头
        rock = create_rock(
            no=index % 8 + 1, name=f'岩石{index + 1}', mass=size_scale / 1000,
            size_scale=size_scale, color=(255, 200, 0),
            init_position=pos, init_velocity=vel, gravity_only_for=gravity_only_for
        )

        # 给石头一个随机旋转的方向和值
        rock.rotation = [0, 0, 0]
        rock.rotation[random.randint(0, 2)] = random.randint(90, 200) / 100
        return rock

    def on_timer_changed(self, time_data: TimeData):
        # 运行中，每时每刻都会触发
        for comet in self.comets:
            if comet.planet.enabled:
                collided = False
                # 如果是否可见，则旋转石头
                comet.planet.rotation += comet.rotation
                # 循环判断每个石头与木星是否相碰撞，如果相碰撞就爆炸
                if two_bodies_colliding(comet, self.jupiter):
                    # 将石头隐藏、设置引力无效后，展示爆炸效果
                    # comet.explode(self.jupiter)
                    # 碰撞到木星，该石头不要爆炸，尝试看看是否会碰撞到地球，如果碰撞了地球，则“木星保护”统计加一
                    self.colliding_count[1] += 1
                    # 加入标记，说明该石头已经碰撞到木星
                    setattr(comet, "jupiter_collided", True)
                    # collided = True
                elif two_bodies_colliding(comet, self.sun):
                    # 将石头隐藏、设置引力无效后，展示爆炸效果
                    comet.explode(self.sun)
                    if not hasattr(comet, "jupiter_collided"):
                        # 该石头没有碰撞到木星，才算一次
                        self.colliding_count[0] += 1
                    collided = True
                elif two_bodies_colliding(comet, self.earth):
                    if hasattr(comet, "jupiter_collided"):
                        # 说明该石头已经碰撞到木星,也就是说木星保护了地球一次
                        self.colliding_count[3] += 1
                    else:
                        # 该石头没有碰撞到木星，才算一次
                        self.colliding_count[2] += 1

                    # 将石头隐藏、设置引力无效后，展示爆炸效果
                    comet.explode(self.earth)
                    collided = True
                if collided:
                    # 如果碰撞了，则该石头重复再利用，这样才保证有无限个石头可用
                    pos, vel = self.random_pos_vel(self.comet_radius)
                    comet.init_position = pos
                    comet.init_velocity = vel
                    comet.set_visible(True)
                    comet.ignore_mass = False
                    comet.planet.enabled = True
                    if hasattr(comet, "jupiter_collided"):
                        delattr(comet, "jupiter_collided")

        print("Sun:%s Jupiter:%s Earth:%s" % (self.colliding_count[0],
                                              self.colliding_count[1],
                                              self.colliding_count[2]))
        sun_cnt, jupiter_cnt, earth_cnt, protected_cnt = self.colliding_count
        total_cnt = sun_cnt + jupiter_cnt + earth_cnt
        if total_cnt == 0:
            colliding_info = self.colliding_info % (0, "0.0%",
                                                    0, "0.0%",
                                                    0, "0.0%",
                                                    0)
        else:
            colliding_info = self.colliding_info % (sun_cnt, str(round(sun_cnt * 100 / total_cnt, 2)) + "%",
                                                    jupiter_cnt, str(round(jupiter_cnt * 100 / total_cnt, 2)) + "%",
                                                    earth_cnt, str(round(earth_cnt * 100 / total_cnt, 2)) + "%",
                                                    protected_cnt)

        self.text_panel.text = colliding_info

    def on_ready(self):
        # 运行前触发
        self.text_panel = create_text_panel()
        self.text_panel.text = self.colliding_info % (0, "0.0%",
                                                      0, "0.0%",
                                                      0, "0.0%",
                                                      0)


if __name__ == '__main__':
    """
    彗木保护地球模拟
    """

    # 设置计时器的最小时间单位为年
    BodyTimer().min_unit = BodyTimer.MIN_UNIT_YEARS

    sim = JupiterProtectsEarthSim(comet_num=30)

    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(sim.on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(sim.on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(sim.bodies, SECONDS_PER_MONTH * 3,
               position=(30000000, 0, -3000000000),
               show_timer=True)
