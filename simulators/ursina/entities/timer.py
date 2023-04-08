# -*- coding:utf-8 -*-
# title           :计时器
# description     :计时器
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import Text, Ursina, application
import datetime

from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


class Timer(Text):

    def __init__(self):
        # 创建一个文本对象来显示计时器的时间
        super().__init__(text='                                 ', position=(0.70, -0.465),
                         origin=(-0.5, 0.5),
                         font=UrsinaConfig.CN_FONT, background=True)
        UrsinaEvent.on_timer_changed_subscription(self.on_timer_changed)

    def on_timer_changed(self, time_data: TimeData):
        self.text = time_data.time_text

    def update(self):
        self.text = "00:00:00"


if __name__ == '__main__':
    app = Ursina()

    t = Timer()


    def update():
        t.update()


    app.run()
