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

from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


class Timer(Text):

    def __init__(self):
        # 创建一个文本对象来显示计时器的时间
        super().__init__(text='00:00', position=(0.65, -0.45), font=UrsinaConfig.CN_FONT)
        UrsinaEvent.on_timer_changed_subscription(self.on_timer_changed)

    def on_timer_changed(self, time_text, time_data):
        self.text = time_text


if __name__ == '__main__':
    app = Ursina()

    t = Timer()


    def update():
        t.update()


    app.run()
