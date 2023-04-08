# -*- coding:utf-8 -*-
# title           :天体计时器
# description     :天体计时器
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body
from common.consts import MO
from common.singleton import Singleton
import os
import random
import math

from simulators.ursina.ursina_event import UrsinaEvent


class BodyTimer(Singleton):
    """
    天体计时器
    """

    def __init__(self):
        if not hasattr(self, "inited"):
            self.velocity_inc = 0.00001
            UrsinaEvent.on_reset_subscription(self.reset)
            UrsinaEvent.on_pause_subscription(self.pause)
            UrsinaEvent.on_start_subscription(self.start)
            self.inited = True

    def pause(self):
        pass

    def start(self):
        pass

    def reset(self):
        self.position_sum = 0.0

    def calc_time(self, dt):
        if not hasattr(self, "position_sum"):
            self.position_sum = 0.0
        self.position_sum += self.velocity_inc * dt
        # 距离(km) / 速度(km/s) = 时间(s)
        seconds = round(self.position_sum / self.velocity_inc)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        years = days // 365
        days = days % 365
        if days > 1:
            s_days = str(days).rjust(3, " ")
            if days >= 20 or years >= 1:
                self.text = f'{int(years)}年{s_days}天'
            else:
                self.text = f'{int(days)}天 {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
        else:
            self.text = f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

        # print(self.text)
        UrsinaEvent.on_timer_changed(self.text, (years, days, hours, minutes, seconds))

    def ignore_gravity(self, body):
        return True


if __name__ == '__main__':
    import time

    t = BodyTimer()
    print(id(t))
    print(id(BodyTimer()))

    for i in range(1000):
        time.sleep(0.01)
        # 距离(km) = 时间(s) * 速度(km/s)
        t.position[0] += 300000 * t.velocity_inc
        t.calc_time()
