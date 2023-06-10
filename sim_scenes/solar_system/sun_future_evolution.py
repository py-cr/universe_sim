# -*- coding:utf-8 -*-
# title           :亿万年后太阳演化模拟
# description     :亿万年后太阳演化模拟（展示的效果为太阳系真实的距离）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Asteroids
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    # 八大行星：木星(♃)、土星(♄)、天王星(♅)、海王星(♆)、地球(⊕)、金星(♀)、火星(♂)、水星(☿)
    # 排列顺序
    # 1、体积：(以地球为1)木星 ：土星 ：天王星 ：海王星 ：地球 ：金星 ：火星 ：水星 = 1330：745：65：60：1：0.86：0.15：0.056
    # 2、质量：(以地球为1)木星 ：土星 ：天王星 ：海王星 ：地球 ：金星 ：火星 ：水星 = 318：95：14.53：17.15：1：0.8：0.11：0.0553
    # 3、离太阳从近到远的顺序：水星、金星、地球、火星、木星、土星、天王星、海王星
    #  =====================================================================
    #  以下展示的效果为太阳系真实的距离
    #  由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
    sun = Sun(name="太阳", size_scale=0.6e2)  # 太阳一开始放大 60 倍，距离保持不变
    bodies = [
        sun,
        Mercury(name="水星", size_scale=2e3),  # 水星放大 2000 倍，距离保持不变
        Venus(name="金星", size_scale=2e3),  # 金星放大 2000 倍，距离保持不变
        Earth(name="地球", size_scale=2e3),  # 地球放大 2000 倍，距离保持不变
        Mars(name="火星", size_scale=2e3),  # 火星放大 2000 倍，距离保持不变
        Jupiter(name="木星", size_scale=0.4e3),  # 木星放大 400 倍，距离保持不变
        Saturn(name="土星", size_scale=0.4e3),  # 土星放大 400 倍，距离保持不变
        Uranus(name="天王星", size_scale=0.4e3),  # 天王星放大 400 倍，距离保持不变
        Neptune(name="海王星", size_scale=0.5e3),  # 海王星放大 500 倍，距离保持不变
        Pluto(name="冥王星", size_scale=5e3),  # 冥王星放大 5000 倍，距离保持不变(从太阳系的行星中排除)
    ]


    def on_ready():
        # 运行前触发
        # 摄像机看向太阳
        camera_look_at(sun)


    def on_timer_changed(time_data: TimeData):
        sun.planet.init_scale = sun.planet.init_scale + 0.1


    # 订阅事件后，上面的函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_YEAR, position=(0, 10 * AU, -10 * AU),
               timer_enabled=True,
               bg_music="sounds/interstellar.mp3")
