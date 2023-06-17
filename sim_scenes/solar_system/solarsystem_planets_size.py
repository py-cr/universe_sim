# -*- coding:utf-8 -*-
# title           :太阳系行星大小比较
# description     :太阳系行星大小比较
# author          :Python超人
# date            :2023-06-17
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, AU
from sim_scenes.func import mayavi_run, ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent

# 可以调整整体放大倍数 ，比例会保持不变
FACTOR = 10
# 地球和月球之间的距离常量，距地距离约: 363104 至 405696 km，平均距离 384000 km
E_M_DISTANCE = 405696 * FACTOR
earth1 = Earth("地球1", size_scale=FACTOR, init_position=[0, 0, 0])
moon = Moon("月球", size_scale=FACTOR, init_position=[E_M_DISTANCE, 0, 0])
earth2 = Earth("地球2", texture="earth2.jpg", size_scale=FACTOR)
bodies = [
    earth1, moon,
    Mercury(name="水星", size_scale=FACTOR),
    Venus(name="金星", size_scale=FACTOR),
    earth2,
    Mars(name="火星", size_scale=FACTOR),
    Jupiter(name="木星", size_scale=FACTOR),
    Saturn(name="土星", size_scale=FACTOR).show_rings(False),
    Uranus(name="天王星", size_scale=FACTOR),
    Neptune(name="海王星", size_scale=FACTOR),
    Pluto(name="冥王星", size_scale=FACTOR)
]

# 从第三个星球（水星）开始
index = 2
last_total_hours = 0

if __name__ == '__main__':
    last_diameter = earth1.diameter * FACTOR / 2
    plant_positions = []
    for i, body in enumerate(bodies):
        body.rotation_speed /= 10  # 星体的旋转速度减小10倍
        body.ignore_mass = True
        body.init_velocity = [0, 0, 0]
        if i >= 2:  # 从第三个星球（水星）开始
            plant_positions.append([(body.diameter * FACTOR / 2) + last_diameter, 0, 0])
            last_diameter += body.diameter * FACTOR
            # print(body)


    def on_ready():
        # 运行前触发
        # 为了较好的立体效果，可以增加太阳光线，光线直射地球（target=earth）
        create_directional_light(position=(E_M_DISTANCE / 2, E_M_DISTANCE * 20, -E_M_DISTANCE * 100),
                                 light_num=3,
                                 target=earth1)


    def on_timer_changed(time_data: TimeData):
        global index, last_total_hours

        if index >= len(bodies):
            return
        total_hours = int(time_data.total_hours)
        # 每间隔3个小时，将行星按顺序进行摆放在地球和月球之间
        if total_hours % 3 == 0 and last_total_hours != total_hours:
            last_total_hours = total_hours
            bodies[index].init_position = plant_positions[index - 2]
            index += 1


    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR,
               position=(E_M_DISTANCE / 2, 0, -E_M_DISTANCE * 1),
               view_closely=True,
               timer_enabled=True)
