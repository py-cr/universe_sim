# -*- coding:utf-8 -*-
# title           :地球季节模拟（四季和24节气）
# description     :地球季节模拟（四季和24节气）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import camera

from bodies import Sun, Earth
from common.consts import SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData, BodyTimer
from simulators.ursina.ursina_event import UrsinaEvent


def create_earth(name, text_color, position):
    """
    创建透明的地球
    @param name: 名称
    @param text_color: 文字颜色
    @param position: 地球的位置
    @return:
    """
    return Earth(name=name, size_scale=5e3, texture="earth_transparent.png",  # 明的地球纹理
                 text_color=text_color, rotation_speed=0,
                 init_position=position, init_velocity=[0, 0, 0]).set_ignore_gravity(True)  # 忽略重力


if __name__ == '__main__':
    """
    摄像机以太阳的视角看地球（四季和24节气）
    """
    sun = Sun(size_scale=5e1, texture="transparent.png")  # 太阳使用透明纹理，不会遮挡摄像机
    # 在 4 个节气的位置创建固定不动的透明地球
    earth_1 = create_earth(name="春分", text_color=(0, 255, 0), position=[-1.05 * AU, 0, 0])
    earth_2 = create_earth(name="夏至", text_color=(255, 0, 0), position=[0, 0, -1.05 * AU])
    earth_3 = create_earth(name="秋分", text_color=(255, 255, 0), position=[1.05 * AU, 0, 0])
    earth_4 = create_earth(name="冬至", text_color=(0, 255, 255), position=[0, 0, 1.05 * AU])
    # 运动的地球
    earth = Earth(size_scale=5e3, texture="earth_hd.jpg",
                  text_color=[255, 255, 255], rotation_speed=0.5,  # 为演示效果，自转角速度取0.5度/小时，实际为15度/小时
                  init_position=[-1 * AU, 0, 0], init_velocity=[0, 0, -29.79])

    # 地球立春的位置和速度
    earth.init_position = [-9.1507536e+07, 0.0000000e+00, 1.1907757e+08]
    earth.init_velocity = [-23.550875, 0., -18.05398]

    earth.rotate_axis_color = (255, 255, 50)
    earth.rotate_axis_scale = 0.75

    bodies = [
        sun, earth,
        earth_1, earth_2, earth_3, earth_4,
    ]

    # 中国农历24节气表，数据为 节气名称 和 camera.rotation_y 的角度范围值
    solar_terms_angles = [
        ("小寒", -22.5, -7.5), ("大寒", -37.5, -22.5), ("立春", -52.5, -37.5), ("雨水", -67.5, -52.5),
        ("惊蛰", -82.5, -67.5), ("春分", -97.5, -82.5), ("清明", -112.5, -97.5), ("谷雨", -127.5, -112.5),
        ("立夏", -142.5, -127.5), ("小满", -157.5, -142.5), ("芒种", -172.5, -157.5),
        ("夏至", -180, -172.5), ("夏至", 172.5, 180),
        ("小暑", 157.5, 172.5), ("大暑", 142.5, 157.5), ("立秋", 127.5, 142.5), ("处暑", 112.5, 127.5),
        ("白露", 97.5, 112.5), ("秋分", 82.5, 97.5), ("寒露", 67.5, 82.5), ("霜降", 52.5, 67.5),
        ("立冬", 37.5, 52.5), ("小雪", 22.5, 37.5), ("大雪", 7.5, 22.5), ("冬至", -7.5, 7.5)]


    def on_ready():
        # 将 4 个节气位置的地球进行旋转，让中国面对太阳
        earth_1.planet.rotation_y += 115  # 春分
        earth_2.planet.rotation_y += 15  # 夏至
        earth_3.planet.rotation_y -= 80  # 秋分
        earth_4.planet.rotation_y -= 145  # 冬至


    def earth_text_display(term_name):
        """
        控制4个透明地球文本是否显示，防止地球文字的叠加
        @param term_name:
        @return:
        """
        for e in [earth_1, earth_2, earth_3, earth_4]:
            if term_name == e.name:
                e.name_text.enabled = False
            else:
                e.name_text.enabled = True


    def on_timer_changed(time_data: TimeData):
        # 摄像机始终看向移动的地球
        camera_look_at(earth, rotation_z=0)
        # 根据角度范围判断，显示中国农历24节气
        for info in solar_terms_angles:
            if info[1] <= camera.rotation_y < info[2]:
                term_name = info[0]
                # 控制4个透明地球文本是否显示，防止地球文字的叠加
                earth_text_display(term_name)
                # 地球名称文字显示为相应的节气
                earth.name_text.text = term_name
                # if term_name == "立春": # 找到立春的位置和速度
                #     print("position", earth.position)
                #     print("velocity", earth.velocity)

        # print(camera.rotation_y)


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    # 设置计时器的最小时间单位为天
    BodyTimer().min_unit = BodyTimer.MIN_UNIT_DAYS
    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY * 2,
               position=(0, 0, 0),  # 摄像机和太阳是相同位置
               show_name=True,
               show_timer=True)
