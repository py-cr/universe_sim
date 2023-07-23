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
    def __init__(self, seconds, min_unit):
        from ursina import time
        if not hasattr(TimeData, "app_start_time"):
            setattr(TimeData, "app_start_time", time.time())
            self.app_time = 0
        else:
            self.app_time = time.time() - getattr(TimeData, "app_start_time")

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
        self.min_unit = min_unit

        s_days = str(days).rjust(3, " ")

        if self.min_unit in [BodyTimer.MIN_UNIT_YEARS]:
            self.time_text = f'{self.years}年'
        elif self.min_unit in [BodyTimer.MIN_UNIT_DAYS]:
            self.time_text = f'{self.years}年{s_days}天'
        elif self.min_unit in [BodyTimer.MIN_UNIT_MINUTES]:
            self.time_text = f'{self.days}天 {self.hours:02d}:{self.minutes:02d}'
        elif self.min_unit in [BodyTimer.MIN_UNIT_HOURS]:
            self.time_text = f'{self.days}天 {self.hours:02d}时'
        else:
            if days > 1 or years >= 1:
                if days >= 20 or years >= 1:
                    self.time_text = f'{self.years}年{s_days}天'
                else:
                    self.time_text = f'{self.days}天 {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
            else:
                self.time_text = f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'


    def get_datetime(self, init_datetime):
        import datetime
        # UTC_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        UTC = datetime.datetime.strptime(init_datetime + "Z", "%Y-%m-%d %H:%M:%S.%fZ")
        # BJS_format = "%Y-%m-%d %H:%M:%S"
        BJS = UTC + datetime.timedelta(hours=8+self.total_hours)
        # BJS = BJS.strftime(BJS_format)
        # dt = datetime(init_datetime)
        return BJS

    @property
    def total_minutes(self):
        return self.total_seconds / 60

    @property
    def total_hours(self):
        return self.total_seconds / 3600

    @property
    def total_days(self):
        return self.total_hours / 24


class AppTimeUtil:
    """
    应用计数器工具类
    """
    def __init__(self):
        self.arrival_time = -1
        self.current_time = 0
        self.params = {}

    def is_first_arrival(self, target_time, time_data: TimeData):
        """
        是否是第一次到达时间
        @param target_time: 目标时间
        @param time_data: 计时器数据
        @return:
        """
        self.current_time = int(time_data.app_time)
        if self.current_time == self.arrival_time:
            return False

        if self.current_time >= int(target_time):
            self.arrival_time = self.current_time
            return True

        return False

    def update(self, time_data: TimeData):
        self.current_time = int(time_data.app_time)

    def clear(self):
        self.arrival_time = -1

    def set_param(self, param_name, val):
        self.params[param_name] = val

    def get_param(self, param_name, default_val=None):
        if param_name in self.params.keys():
            return self.params[param_name]
        self.set_param(param_name, default_val)
        return default_val

    def inc_param(self, param_name, inc_val=1, init_val=0):
        val = self.params.get(param_name, init_val)
        self.set_param(param_name, val + inc_val)


class BodyTimer(Singleton):
    """
    天体计时器，原理就是:
       以 BodyTimer 为一个天体在宇宙中运行，以速度 self.velocity_inc 递增。
       通过公式： 速度 * 时间 = 距离，获取到累计距离， self.position_sum += self.velocity_inc * dt
       最后通过公式： 时间 = 距离 / 速度， 从而得到天体运行了多长时间
    """
    MIN_UNIT_SECONDS = "seconds"
    MIN_UNIT_MINUTES = "minutes"
    MIN_UNIT_HOURS = "hours"
    MIN_UNIT_DAYS = "days"
    MIN_UNIT_YEARS = "years"

    def __init__(self):
        if not hasattr(self, "inited"):
            self.velocity_inc = 1e-30  # 理论上数值越小越好，可以使用 1e-300 ，但建议使用：1e-30   # 0.00001
            # 按键盘的 “O” 重置键会触发 on_reset
            UrsinaEvent.on_reset_subscription(self.reset)
            UrsinaEvent.on_pause_subscription(self.pause)
            UrsinaEvent.on_start_subscription(self.start)
            self.inited = True
            self.min_unit = BodyTimer.MIN_UNIT_SECONDS

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
        UrsinaEvent.on_timer_changed(TimeData(seconds, self.min_unit))

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
