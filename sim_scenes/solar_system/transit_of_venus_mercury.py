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
    earth = Earth(name="地球")
    sun = Sun(name="太阳", size_scale=5e1)  # 太阳放大 20 倍
    bodies = [
        sun,
        Mercury(name="水星",
                init_position=[0.384 * AU, 0, 0],
                init_velocity=[0, 0, 47.87],
                size_scale=5e1),  # 水星放大 10 倍，距离保持不变
        Venus(name="金星",
              init_position=[0.721 * AU, 0, 0],
              init_velocity=[0, 0, 35],
              size_scale=5e1)  # 金星放大 10 倍，距离保持不变
    ]


    def on_ready():
        camera_look_at(sun, rotation_x=None, rotation_y=None, rotation_z=0)
        pass


    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY * 3,
               position=earth.init_position)
