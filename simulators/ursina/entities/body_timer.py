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


class TimeData:
    def __init__(self, seconds):
        self.total_seconds = seconds
        # 获取到 seconds 后，通过下面的计算得到时分秒、年、天
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        years = days // 365
        days = days % 365

        self.years = int(years)
        self.days = int(days)
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.seconds = int(seconds)

        if days > 1:
            s_days = str(days).rjust(3, " ")
            if days >= 20 or years >= 1:
                self.time_text = f'{self.years}年{s_days}天'
            else:
                self.time_text = f'{self.days}天 {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
        else:
            self.time_text = f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'

    @property
    def total_minutes(self):
        return self.total_seconds / 60

    @property
    def total_hours(self):
        return self.total_seconds / 3600



class BodyTimer(Singleton):
    """
    天体计时器，原理就是:
       以 BodyTimer 为一个天体在宇宙中运行，以速度 self.velocity_inc 递增。
       通过公式： 速度 * 时间 = 距离，获取到累计距离， self.position_sum += self.velocity_inc * dt
       最后通过公式： 时间 = 距离 / 速度， 从而得到天体运行了多长时间
    """

    def __init__(self):
        if not hasattr(self, "inited"):
            self.velocity_inc = 1e-30  # 理论上数值越小越好，可以使用 1e-300 ，但建议使用：1e-30   # 0.00001
            UrsinaEvent.on_reset_subscription(self.reset)
            UrsinaEvent.on_pause_subscription(self.pause)
            UrsinaEvent.on_start_subscription(self.start)
            self.inited = True

    def pause(self):
        pass

    def start(self):
        pass

    def reset(self):
        # 累计距离置零
        self.position_sum = 0.0

    def calc_time(self, dt):
        if not hasattr(self, "position_sum"):
            # 累计距离置零
            self.position_sum = 0.0
        # 通过公式： 速度 * 时间 = 距离，获取到累计距离
        self.position_sum += self.velocity_inc * dt

        # 距离(km) / 速度(km/s) = 时间(s)
        seconds = round(self.position_sum / self.velocity_inc)
        # # 获取到 seconds 后，通过下面的计算得到时分秒、年、天
        # hours, remainder = divmod(seconds, 3600)
        # minutes, seconds = divmod(remainder, 60)
        # days, hours = divmod(hours, 24)
        # years = days // 365
        # days = days % 365
        # if days > 1:
        #     s_days = str(days).rjust(3, " ")
        #     if days >= 20 or years >= 1:
        #         time_text = f'{int(years)}年{s_days}天'
        #     else:
        #         time_text = f'{int(days)}天 {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
        # else:
        #     time_text = f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

        # print(self.text)
        UrsinaEvent.on_timer_changed(TimeData(seconds))

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
