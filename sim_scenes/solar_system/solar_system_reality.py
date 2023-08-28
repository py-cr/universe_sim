# -*- coding:utf-8 -*-
# title           :模拟太阳系给天体真实时间和位置
# description     :模拟太阳系给天体真实时间和位置
# author          :Python超人
# date            :2023-07-23
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================

import numpy as np

from bodies import Sun, Mercury, Venus, Earth, Mars, Asteroids, Jupiter, Saturn, Uranus, Neptune, Moon
from common.celestial_data_service import get_body_posvel, recalc_moon_position, calc_solar_acceleration, \
    set_solar_system_celestial_position, set_earth_rotation
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
        self.recalc_moon_pos = True

    def create_bodies(self):
        """
        创建太阳系的天体
        @return:
        """
        # 由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
        # 太阳缩放比例
        self.sun_size_scale = 0.04e2 if self.debug_mode else 0.4e2

        # 地月缩放比例
        # 为了更好的展示效果，需要对月球的位置重新计算（使得地月距离放大，月球相对地球方向不变），重新计算位置后，地球和月球可以放大1000倍以上
        if self.recalc_moon_pos:  # 重新计算月球位置
            self.earth_size_scale = 10e3 if self.debug_mode else 1e3
            self.moon_size_scale = 2e3
        else:
            # 不重新计算，则地月的距离相对整个太阳系会非常近，因此，月球只放大了10倍
            self.earth_size_scale = 1e1
            self.moon_size_scale = 1e1

        self.sun = Sun(name="太阳", size_scale=self.sun_size_scale)  # 太阳
        self.mercury = Mercury(name="水星", size_scale=1.5e3)  # 水星
        self.venus = Venus(name="金星", size_scale=1e3)  # 金星
        self.earth = Earth(name="地球", texture="earth_hd.jpg",
                           rotate_angle=3.44,
                           size_scale=self.earth_size_scale)  # 地球
        self.earth_clouds = Earth(name="地球云层", texture="transparent_clouds.png", show_trail=False,
                                  rotate_angle=3.44,
                                  size_scale=self.earth_size_scale * 1.01)  # 地球云层
        self.moon = Moon(name="月球", size_scale=self.moon_size_scale)  # 月球
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
        # self.earth.rotate_axis_color = (255, 255, 50)
        # 如果为调试模式，则太阳光对地球无效，方便查看
        if self.debug_mode:
            self.earth.set_light_disable(True)

    def show_clock(self, dt):
        """
        显示时钟
        @param dt: 时间 datetime
        @return:
        """
        if self.clock_position_center:
            position, origin = (0, .25), (0, 0),
        else:
            position, origin = (0.60, -0.465), (-0.5, 0.5),

        ControlUI.current_ui.show_message(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                          position=position,
                                          origin=origin,
                                          font="verdana.ttf",
                                          close_time=-1)

    def set_bodies_position(self, time_data: TimeData):
        """
        设置天体的位置（包含速度和加速度的信息）
        @param time_data:
        @return:
        """
        t = self.start_time + time_data.total_days
        set_solar_system_celestial_position(self.bodies, t, self.recalc_moon_pos)

    def on_ready(self):
        """
        事件绑定后，模拟器运行前会触发
        @return:
        """
        # 运行前触发

        if self.sky_texture is not None:
            from simulators.ursina.entities.sphere_sky import SphereSky
            SphereSky(texture=self.sky_texture).scale = 80000

        camera.clip_plane_near = 0.1
        camera.clip_plane_far = 100000

        # camera.rotation_z = -20
        if self.debug_mode:
            camera.fov = 30  # 调试时，拉近摄像机距离

        # 需要按照时间和日期来控制地球的自转，所以删除控制地球自转的属性
        delattr(self.earth.planet, "rotation_speed")
        delattr(self.earth.planet, "rotspeed")

        # 设置后，可以调整鼠标键盘的控制速度
        application.time_scale = 1

    def on_timer_changed(self, time_data: TimeData):
        """
        事件绑定后，时时刻刻都会触发
        @param time_data:
        @return:
        """
        dt = time_data.get_datetime(str(self.start_time))
        # 设置天体的位置（包含速度和加速度的信息）
        self.set_bodies_position(time_data)
        # 保证地球的自转和北京时间同步
        set_earth_rotation(self.earth, dt)
        # 显示时钟
        self.show_clock(dt)

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
            recalc_moon_pos=True,
            clock_position_center=False):
        """
        模拟运行
        @param debug_mode: 是否调试模式
        @param start_time: 运行的开始时间
        @param show_asteroids: 是否显示小行星带
        @param show_earth_clouds: 地球是否显示云层（图片效果，不是真实的云层）
        @param recalc_moon_pos: 为了更好的展示效果，需要对月球的位置重新计算（使得地月距离放大，月球相对地球方向不变）
        @param clock_position_center: 时钟是否显示在中间
        @return:
        """
        self.recalc_moon_pos = recalc_moon_pos
        self.debug_mode = debug_mode
        self.clock_position_center = clock_position_center
        self.show_asteroids = show_asteroids
        self.show_earth_clouds = show_earth_clouds
        # 创建太阳系天体
        self.create_bodies()
        # 对地球进行初始化
        self.init_earth()
        # 绑定事件
        self.bind_events()

        from astropy.time import Time
        from datetime import datetime
        # 开始时间为空，则默认为当前时间
        if start_time is None:
            self.start_time = Time.now()  # 获取默认开始时间为当前时间
        elif isinstance(start_time, str):
            self.start_time = Time(datetime.strptime(start_time + '+0800', '%Y-%m-%d %H:%M:%S%z'),
                                   format='datetime')

        from common.image_utils import find_texture
        self.sky_texture = find_texture("bg_pan.jpg", None)
        if self.sky_texture is None:
            cosmic_bg = None
        else:
            cosmic_bg = ''

        dt = SECONDS_PER_DAY  # 1秒=1天
        dt = 1  # 1秒=1秒
        # 使用 ursina 查看的运行效果
        # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
        # position = 左-右+、上+下-、前+后-
        ursina_run(self.bodies, dt,
                   position=(0, 0.2 * AU, -3 * AU),
                   gravity_works=False,  # 关闭万有引力的计算
                   show_grid=False,
                   cosmic_bg=cosmic_bg,
                   show_camera_info=False,
                   timer_enabled=True)


if __name__ == '__main__':
    #  以下展示的效果为太阳系真实的时间和位置
    sim = SolarSystemRealitySim()
    sim.run(
        # debug_mode=True,  # 是否调试模式
        start_time='2050-01-01 12:00:00',  # 指定运行的开始时间，不指定为当前时间
        # show_asteroids=True,  # 是否显示小行星带（图片模拟）
        # show_earth_clouds=True,  # 地球是否显示云层（图片效果，不是真实的云层）
        # recalc_moon_pos=False,  # 为了更好的展示效果，需要对月球的位置重新计算（使得地月距离放大，月球相对地球方向不变）
        # clock_position_center=True  # 时钟是否显示在中间
    )
