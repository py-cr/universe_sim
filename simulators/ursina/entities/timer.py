from ursina import Text, Ursina, application
import datetime

from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


class Timer(Text):

    def __init__(self):
        # 创建一个文本对象来显示计时器的时间
        super().__init__(text='00:00', position=(-0.85, 0.49), font=UrsinaConfig.CN_FONT)
        # 用来计时的变量
        # self.start_time = time.time()
        self.reset()
        UrsinaEvent.on_timer_changed_subscription(self.update)
        UrsinaEvent.on_reset_subscription(self.reset)
        UrsinaEvent.on_pause_subscription(self.pause)
        UrsinaEvent.on_start_subscription(self.start)
        self.elapsed_time_offset = datetime.timedelta(microseconds=1)

    def pause(self):
        pass

    def start(self):
        self.last_time = datetime.datetime.now()

    def reset(self):
        self.last_time = datetime.datetime.now()
        self.elapsed_time = datetime.timedelta(0)

    def update(self, evolve_dt=1):
        # # 计算当前的时间
        # elapsed_time = time.time() - self.start_time
        #
        # # 将时间转换成“分钟：秒”的形式
        # minutes = int(elapsed_time // 60)
        # seconds = int(elapsed_time % 60)
        # self.text = f'{minutes:02d}:{seconds:02d}'
        time_scale = UrsinaConfig.get_app_time_scale()
        current_time = datetime.datetime.now()
        # 0.653 是对测试太阳系时间的纠正
        self.elapsed_time += (current_time - self.last_time) * evolve_dt * time_scale * 0.653
        # datetime.timedelta(microseconds=1)  0:00:00.000001
        # datetime.timedelta(milliseconds=1)  0:00:00.001000
        self.elapsed_time += self.elapsed_time_offset  # 按区域取值
        self.last_time = current_time
        hours, remainder = divmod(self.elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        days = self.elapsed_time.days
        self.text = f'{days}天, {hours:02d}:{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    app = Ursina()

    t = Timer()


    def update():
        t.update()


    app.run()
