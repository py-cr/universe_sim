# -*- coding:utf-8 -*-
# title           :模拟太阳系给天体真实时间和位置
# description     :模拟太阳系给天体真实时间和位置
# author          :Python超人
# date            :2023-07-23
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import math

import numpy as np

from bodies import Sun, Mercury, Venus, Earth, Mars, Asteroids, Jupiter, Saturn, Uranus, Neptune, Moon
from common.celestial_data_service import get_body_posvel, recalc_moon_position, calc_solar_acceleration, \
    set_solar_system_celestial_position, set_earth_rotation
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run, camera_look_at, create_text_panel
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import clear_trails
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera, application


class SolarSystemRealitySim:
    def __init__(self):
        """

        @param debug_mode: 是否为调试模式
        """
        self.clock_position_center = False
        self.debug_mode = False
        self.recalc_moon_pos = True

    def create_bodies(self):
        """
        创建太阳系的天体
        @return:
        """
        # 由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
        # 太阳缩放比例

        # 地月缩放比例
        # 为了更好的展示效果，需要对月球的位置重新计算（使得地月距离放大，月球相对地球方向不变），重新计算位置后，地球和月球可以放大1000倍以上
        # if self.recalc_moon_pos:  # 重新计算月球位置
        #     self.earth_size_scale = 10e3 if self.debug_mode else 1e3
        #     self.sun_size_scale = 0.04e2 if self.debug_mode else 0.4e2
        #     self.moon_size_scale = 2e3
        # else:
        #     # 不重新计算，则地月的距离相对整个太阳系会非常近，因此，月球只放大了30倍
        #     self.earth_size_scale = 2.5e1
        #     self.moon_size_scale = 5e1
        #     self.sun_size_scale = 1e1

        self.earth_size_scale = 1
        self.moon_size_scale = 1
        self.sun_size_scale = 1

        self.sun = Sun(name="太阳", size_scale=self.sun_size_scale)  # 太阳
        self.earth = Earth(name="地球",  # texture="earth_hd.jpg",
                           rotate_angle=3.44,
                           size_scale=self.earth_size_scale)  # 地球
        self.earth_camera = Earth(name="地球摄像机", texture="transparent.png",
                                  rotate_angle=0,
                                  rotation_speed=0,
                                  show_trail=False,
                                  size_scale=1)  # 地球摄像机
        self.earth_camera.camera_init_val = 0
        self.moon = Moon(name="月球", size_scale=self.moon_size_scale,
                         rotation_speed=0.4065)  # 月球
        self.sun.show_trail = False
        self.earth.trail_scale_factor = 0.2
        self.moon.trail_scale_factor = 0.3
        # 所有天体
        self.bodies = [self.sun, self.earth, self.earth_camera, self.moon]

    # def init_earth(self):
    #     """
    #     初始化地球
    #     @return:
    #     """
    #     # 让地球显示自转轴线
    #     self.earth.rotate_axis_color = (255, 255, 50)
    #     # 如果为调试模式，则太阳光对地球无效，方便查看
    #     if self.debug_mode:
    #         self.earth.set_light_disable(True)

    def show_clock(self, dt):
        """
        显示时钟
        @param dt: 时间 datetime
        @return:
        """
        if self.clock_position_center:
            position, origin = (0, .25), (0, 0)
        else:
            # position, origin = (0.60, -0.465), (-0.5, 0.5)
            position, origin = (-0.60, -0.465), (-0.5, 0.5)

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

        self.text_panel = create_text_panel()
        self.text_panel.text = "太阳缩放：1.0\n地球缩放：1.0\n月球缩放：1.0"

        # camera.rotation_z = -20
        # if self.debug_mode:
        #     camera.fov = 30  # 调试时，拉近摄像机距离
        # camera.fov = 40
        camera.clip_plane_near = 10
        # camera.clip_plane_far = 1000000
        camera.parent = self.earth_camera.planet
        # camera.update = self.camera_update

        # 需要按照时间和日期来控制地球的自转，所以删除控制地球自转的属性
        delattr(self.earth.planet, "rotation_speed")
        delattr(self.earth.planet, "rotspeed")

        # 以下配置可以快速查看4年的轨迹
        UrsinaConfig.trail_length = 2800
        # UrsinaConfig.trail_type = 'line'
        UrsinaConfig.trail_factor = 3
        UrsinaConfig.trail_thickness_factor = 10

        # 设置后，可以调整鼠标键盘的控制速度
        application.time_scale = 2

    #
    # def camera_update(self):
    #     camera.x = -50  # 100
    #     # camera.z = -10
    #     camera.y = 20
    #     camera.z = -10
    #     # 摄像机看向地球
    #     camera_look_at(self.earth)

    def body_show(self, body):
        body.planet.enabled = True
        body.show_trail = True

    def body_hide(self, body):
        body.planet.enabled = False
        body.show_trail = False
        # clear_trails(body.planet)

    def body_scale(self, body, value):
        body.planet.init_scale *= value
        if hasattr(body.planet.main_entity, "trail_scale"):
            body.planet.main_entity.trail_scale *= value

    def set_camera_pos(self, time_data: TimeData):
        if time_data.total_days > 120:
            self.earth_camera.camera_init_val += 300000
        elif time_data.total_days > 90:
            self.earth_camera.camera_init_val += 60000
        elif time_data.total_days > 90:
            self.earth_camera.camera_init_val += 20000
        elif time_data.total_days > 30:
            self.earth_camera.camera_init_val += 18000
        elif time_data.total_days > 10:
            self.earth_camera.camera_init_val += 4000
        elif time_data.total_days > 2:
            self.earth_camera.camera_init_val += 500

        # if UrsinaConfig.trail_factor < 50:
        #     self.body_scale(1.002)
        if time_data.total_days < 5:
            self.earth.show_trail = False
            self.moon.show_trail = False
        if 30 > time_data.total_days > 5:
            self.earth.show_trail = True
            self.moon.show_trail = True
            self.body_scale(self.moon, 1.0025)
            self.body_scale(self.earth, 1.002)
        elif 60 > time_data.total_days > 30:
            # self.body_hide(self.moon)
            self.body_scale(self.moon, 1.002)
            self.body_scale(self.earth, 1.002)
            self.body_scale(self.sun, 1.002)
        elif 150 > time_data.total_days > 60:
            self.earth.planet.init_scale = 0.01
            self.earth.planet.main_entity.trail_scale = 0.03
            # self.body_scale(self.earth, 0.02)
            # self.body_hide(self.earth)
            # self.earth.planet.init_scale = 0.01
            # self.body_show(self.moon)
            # self.body_scale(1.0015)
            # self.sun_scale(1.0015)
        # else:
        #     self.body_scale(1.002)
        #     self.sun_scale(1.0005)

        print("%s,%s" % (round(self.moon.planet.body_scale, 1), time_data.total_days))

        # camera.x = -300  # 100
        # camera.z = 200
        # camera.y += self.earth_camera.camera_init_val * UrsinaConfig.SCALE_FACTOR

        # camera.x = -80  # 100
        # camera.z = -10
        dis_au = round(camera.y / UrsinaConfig.SCALE_FACTOR / AU, 2)

        if dis_au < 400:
            if self.earth_camera.camera_init_val > 0:
                camera.y += self.earth_camera.camera_init_val * UrsinaConfig.SCALE_FACTOR
            else:
                camera.y = 80

        self.text_panel.text = "太阳大小缩放：%.1f\n地球大小缩放：%.1f\n月球大小缩放：%.1f\n摄像机距地球：%.2f天文单位" % \
                               (self.sun.planet.body_scale,
                                self.earth.planet.body_scale,
                                self.moon.planet.body_scale,
                                dis_au)

        # UrsinaConfig.trail_factor = 3 * math.sqrt(camera.y / 250)
        pass

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
        # 调整摄像机的位置
        self.set_camera_pos(time_data)
        # 摄像机看向地球
        camera_look_at(self.sun)
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
        # 创建太阳系天体
        self.create_bodies()
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

        dt = SECONDS_PER_DAY  # 1秒=1天
        # dt = 1  # 1秒=1秒
        # 使用 ursina 查看的运行效果
        # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
        # position = 左-右+、上+下-、前+后-
        ursina_run(self.bodies, dt,
                   position=(0, 0, 0),
                   # position=(0, 0.2 * AU, -3 * AU),
                   gravity_works=False,  # 关闭万有引力的计算
                   show_grid=False,
                   show_trail=True,
                   # cosmic_bg='',
                   show_camera_info=False,
                   timer_enabled=True)


if __name__ == '__main__':
    #  以下展示的效果为太阳系真实的时间和位置
    sim = SolarSystemRealitySim()
    sim.run(
        # debug_mode=True,  # 是否调试模式
        # start_time='2023-01-01 02:20:00',  # 指定运行的开始时间，不指定为当前时间
        recalc_moon_pos=False,  # 为了更好的展示效果，需要对月球的位置重新计算（使得地月距离放大，月球相对地球方向不变）
        # clock_position_center=True  # 时钟是否显示在中间
    )
