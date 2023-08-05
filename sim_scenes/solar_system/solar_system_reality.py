# -*- coding:utf-8 -*-
# title           :模拟太阳系给天体真实时间和位置
# description     :模拟太阳系给天体真实时间和位置
# author          :Python超人
# date            :2023-07-23
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com de423


import numpy as np

from bodies import Sun, Mercury, Venus, Earth, Mars, Asteroids, Jupiter, Saturn, Uranus, Neptune, Moon
from common.celestial_data_service import get_body_posvel, recalc_moon_position
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera, application


class SolarSystemRealitySim:
    def __init__(self):
        """

        @param debug_mode: 是否为调试模式
        """
        self.show_asteroids = False
        self.clock_position_center = False
        self.show_earth_clouds = False
        self.debug_mode = False

    def create_bodies(self):
        """
        创建太阳系的天体
        @return:
        """
        self.sun_size_scale = 0.04e2 if self.debug_mode else 0.4e2
        self.earth_size_scale = 10e3 if self.debug_mode else 1e3

        self.sun = Sun(name="太阳", size_scale=self.sun_size_scale)  # 太阳
        self.mercury = Mercury(name="水星", size_scale=1.5e3)  # 水星
        self.venus = Venus(name="金星", size_scale=1e3)  # 金星
        self.earth = Earth(name="地球", texture="earth_hd.jpg", size_scale=self.earth_size_scale)  # 地球
        self.earth_clouds = Earth(name="地球云层", texture="transparent_clouds.png",
                                  size_scale=self.earth_size_scale * 1.01)  # 地球云层
        self.moon = Moon(name="月球", size_scale=2e3)  # 月球
        self.mars = Mars(name="火星", size_scale=1.2e3)  # 火星
        self.asteroids = Asteroids(size_scale=1e2, parent=self.sun, rotate_angle=-20)  # 模拟的小行星带
        self.jupiter = Jupiter(name="木星", size_scale=4e2)  # 木星
        self.saturn = Saturn(name="土星", size_scale=4e2)  # 土星
        self.uranus = Uranus(name="天王星", size_scale=10e2)  # 天王星
        self.neptune = Neptune(name="海王星", size_scale=10e2)  # 海王星
        # 行星
        self.planets = [self.mercury, self.venus, self.earth, self.mars,
                        self.jupiter, self.saturn, self.uranus, self.neptune]
        # 所有天体
        self.bodies = [self.sun] + self.planets + [self.moon]

        if self.show_earth_clouds:
            self.bodies += [self.earth_clouds]

        if self.show_asteroids:
            self.bodies += [self.asteroids]

    def init_earth(self):
        """
        初始化地球
        @return:
        """
        # 让地球显示自转轴线
        self.earth.rotate_axis_color = (255, 255, 50)
        # 如果为调试模式，则太阳光对地球无效，方便查看
        if self.debug_mode:
            self.earth.set_light_disable(True)

    def on_ready(self):
        # 运行前触发
        camera.rotation_z = -20
        if self.debug_mode:
            camera.fov = 20  # 调试时，拉近摄像机距离

        # 需要按照时间和日期来控制地球的自转，所以删除控制地球自转的属性
        delattr(self.earth.planet, "rotation_speed")
        delattr(self.earth.planet, "rotspeed")

        # 设置后，可以调整鼠标键盘的控制速度
        application.time_scale = 2

    def show_timer_text(self, time_data):
        dt = time_data.get_datetime(str(self.start_time))

        # 需要按照时间和日期控制地球的自转，不能随意转动
        # 日期是当年的第几天
        timetuple = dt.timetuple()

        # 计算出：日期当天的偏转角度
        day_of_year = timetuple.tm_yday
        angle_of_day = day_of_year * (360 / 365)
        total_hours = timetuple.tm_hour + timetuple.tm_min / 60 + timetuple.tm_sec / 60 / 60
        self.earth.planet.rotation_y = -total_hours * 15 - angle_of_day
        # print(time_data.get_datetime(str(self.start_time)))
        if self.clock_position_center:
            position, origin = (0, .25), (0, 0),
        else:
            position, origin = (0.60, -0.465), (-0.5, 0.5),

        ControlUI.current_ui.show_message(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                          position=position,
                                          origin=origin,
                                          font="verdana.ttf",
                                          close_time=-1)

    def on_timer_changed(self, time_data: TimeData):
        """
        时时刻刻运行
        @param time_data:
        @return:
        """
        t = self.start_time + time_data.total_days

        earth_pos = None
        sun_pos = None

        for body in self.bodies:
            if isinstance(body, Asteroids):  # 小行星带是模拟，不是正常的天体
                posvel = None
            else:
                # 获取天体的三维位置和矢量速度
                posvel = get_body_posvel(body, t)

            if isinstance(body, Moon):  # 如果是月球，为了好的展示效果，需要对月球的位置重新计算
                posvel = recalc_moon_position(posvel, earth_pos)

            if posvel is None:
                # posvel 为空，则使用太阳的坐标
                position, velocity = [sun_pos.x.value * AU,
                                      sun_pos.z.value * AU,
                                      sun_pos.y.value * AU], [0, 0, 0]
            else:
                # 坐标单位：千米  速度单位：千米/秒
                position, velocity = [posvel[0].x.value * AU, posvel[0].z.value * AU, posvel[0].y.value * AU], \
                                     [posvel[1].x.value * AU / SECONDS_PER_DAY,
                                      posvel[1].z.value * AU / SECONDS_PER_DAY,
                                      posvel[1].y.value * AU / SECONDS_PER_DAY]

            # 实时调整天体的位置和速度
            body.position = np.array(position)
            body.velocity = np.array(velocity)

            if isinstance(body, Earth):
                # 记录地球的位置
                earth_pos = posvel[0]
            elif isinstance(body, Sun):
                # 记录太阳的位置
                sun_pos = posvel[0]

        self.show_timer_text(time_data)

    def bind_events(self):
        # 运行中，每时每刻都会触发 on_timer_changed
        UrsinaEvent.on_timer_changed_subscription(self.on_timer_changed)
        # 运行前会触发 on_ready
        UrsinaEvent.on_ready_subscription(self.on_ready)

    def run(self,
            debug_mode=False,
            start_time=None,
            show_asteroids=False,
            show_earth_clouds=False,
            clock_position_center=False):
        """
        模拟运行
        @return:
        """
        self.debug_mode = debug_mode
        self.clock_position_center = clock_position_center
        self.show_asteroids = show_asteroids
        self.show_earth_clouds = show_earth_clouds
        self.create_bodies()  # 创建太阳系天体
        self.init_earth()  # 初始化地球
        self.bind_events()  # 绑定事件

        if start_time is None:
            from astropy.time import Time
            self.start_time = Time.now()  # 获取默认开始时间为当前时间

        dt = SECONDS_PER_DAY  # 1秒=1天
        dt = 1  # 1秒=1秒
        # 使用 ursina 查看的运行效果
        # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
        # position = 左-右+、上+下-、前+后-
        ursina_run(self.bodies, dt,
                   position=(0, 0.2 * AU, -3 * AU),
                   gravity_works=False,  # 关闭万有引力的计算
                   show_grid=False,
                   show_camera_info=False,
                   timer_enabled=True)


if __name__ == '__main__':
    #  以下展示的效果为太阳系真实的时间和位置
    #  由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大

    sim = SolarSystemRealitySim()
    sim.run(
        debug_mode=True,
        clock_position_center=True
    )
