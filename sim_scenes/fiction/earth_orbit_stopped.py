# -*- coding:utf-8 -*-
# title           :如果地球停止公转
# description     :如果地球停止公转，那它需要多久才会掉进太阳？ 大约65天
# author          :Python超人
# date            :2023-06-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Mercury, Venus
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from common.func import calculate_distance, get_acceleration_info
from sim_scenes.func import mayavi_run, ursina_run, camera_look_at, two_bodies_colliding, set_camera_parent, \
    create_text_panel
from bodies.body import AU
from simulators.ursina.entities.body_timer import BodyTimer, TimeData
from simulators.ursina.entities.entity_utils import get_value_direction_vectors
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import application, camera, Vec3
import math
from simulators.ursina.ursina_mesh import create_circle_line
from ursina import color


class EarthOrbitStoppedSim:
    """
    地球停止公转模拟类
    """
    # 地球的Y方向初始速度
    EARTH_INIT_VELOCITY = 0  # 0km/s

    def __init__(self):
        self.sun = Sun(init_position=[0, 0, 0], size_scale=1)
        self.earth = Earth(init_position=[0, 0, -AU], # texture="earth2.jpg",
                           init_velocity=[0, self.EARTH_INIT_VELOCITY, 0],
                           size_scale=1).set_light_disable(True)
        # 水星轨道半径
        self.mercury_radius = 0.384 * AU
        # 金星轨道半径
        self.venus_radius = 0.721 * AU
        # 计算得到水星的初始位置和初始速度： [49311300.        0. 28075956.] [ 24.30735    0.       -41.926445]
        self.mercury = Mercury(name="水星",
                               # init_position=[0, 0, -self.mercury_radius],  # 和地球插肩而过的位置，用于找到下面的速度
                               init_position=[49311300., 0, 28075956.],  # 设置的初始位置和初始速度使得与地球插肩而过
                               init_velocity=[-24.282, 0, 41.913],
                               size_scale=1).set_light_disable(True)
        # 计算得到金星的初始位置和初始速度： [-98608848.         0. -42909512.] [-13.869937   0.        32.247845]
        self.venus = Venus(name="金星",
                           # init_position=[0, 0, -self.venus_radius],  # 和地球插肩而过的位置，用于找到下面的速度
                           init_position=[-98608848., 0, -42909512.],  # 设置的初始位置和初始速度使得与地球插肩而过
                           init_velocity=[13.869937, 0, -32.247845],
                           size_scale=1).set_light_disable(True)

        self.bodies = [
            self.sun, self.mercury, self.venus, self.earth
        ]
        # 是否已经到达太阳
        self.arrived_sun = False
        # 是否已经到达水星的轨道
        self.arrived_mercury_orbit_line = False
        # 是否已经到达金星的轨道
        self.arrived_venus_orbit_line = False
        # 显示板信息模板
        self.arrived_info = "　距离太阳：${distance}\n\n　地球速度：${velocity}\n\n地球加速度：${acceleration}\n\n"

    def create_orbit_line(self, radius, color):
        """
        创建行星轨道线
        @param radius: 以太阳中心为中心点的半径
        @param color: 颜色
        @return:
        """
        orbit_line = create_circle_line(parent=self.sun, radius=radius, thickness=5, color=color, alpha=0.3)
        orbit_line.rotation_x = 90
        orbit_line.enabled = False # 默认不显示
        return orbit_line

    def on_ready(self):
        # 运行前触发一次
        # 应用的时间缩放越小，视频更近顺滑（低速运行比较重要）
        application.time_scale = 0.00001
        # FOV是摄像机的视场角，即Field of view（FOV），它的大小决定了摄像机的视野范围。
        camera.fov = 50
        self.text_panel = create_text_panel()
        self.text_panel.text = self.arrived_info. \
            replace("${distance}", "1 AU"). \
            replace("${velocity}", "0"). \
            replace("${acceleration}", "0")

        # 创建水星轨道线
        self.mercury_orbit_line = self.create_orbit_line(
            radius=self.mercury_radius * UrsinaConfig.SCALE_FACTOR,
            color=self.mercury.color)
        # 创建金星轨道线
        self.venus_orbit_line = self.create_orbit_line(
            radius=self.venus_radius * UrsinaConfig.SCALE_FACTOR,
            color=self.venus.color)

    def on_timer_changed(self, time_data: TimeData):
        # 摄像机时时刻刻看向地球
        camera_look_at(self.earth, rotation_z=0)
        # 获取地球当前的位置，让摄像机跟随地球
        earth_pos = self.earth.planet.world_position
        camera.world_position = Vec3(earth_pos[0], earth_pos[1] + 0.01, earth_pos[2] - 0.1)

        acceleration_info = get_acceleration_info(self.earth.acceleration)
        velocity, _ = get_value_direction_vectors(self.earth.velocity)

        # 计算地球和太阳中心点之间的距离
        distance = calculate_distance(self.earth.position, self.sun.position)
        # 减去太阳和地球的半径，得到地球表面和太阳表面的距离
        distance = distance - self.sun.radius - self.earth.radius

        if distance > 100000000:
            distance_str = "%s亿" % round(distance / 100000000.0, 2)
        # elif distance > 10000000:
        #     distance_str = "%s千万" % round(distance / 10000000.0, 2)
        # elif distance > 1000000:
        #     distance_str = "%s百万" % round(distance / 1000000.0, 2)
        elif distance > 10000:
            distance_str = "%s万" % round(distance / 10000.0, 2)
        else:
            distance_str = round(distance, 2)

        if two_bodies_colliding(self.sun, self.earth):
            self.arrived_sun = True
            msg = "地球在[%s]到达太阳" % time_data.time_text
            print(msg)
            self.text_panel.text = self.arrived_info. \
                                       replace("${distance}", "0 km"). \
                                       replace("${acceleration}", "%s" % acceleration_info). \
                                       replace("${velocity}", "%s km/s" % round(velocity, 2)) \
                                   + "\n\n" + msg
            ControlUI.current_ui.show_message(msg, close_time=-1)
            application.pause()
            return

        # 定义慢速运行的范围，这样才可以清楚的看到地球接近金星、水星、太阳的情景
        slow_speed_ranges = [
            (41.2, 41.35, 0.01),  # (40, 41.2, 0.1), (41.2, 42.2, 0.1), (39, 40.2, 0.5), (42, 43, 0.5),
            (56.85, 57.05, 0.01),  # (55, 56.9, 0.1), (57, 58.05, 0.1), (54, 55.2, 0.5), (58.2, 59, 0.5),
            (64.3, 67, 0.01),  # (63, 64.4, 0.1), (64, 64.5, 0.5),
        ]

        venus_range = slow_speed_ranges[0]
        mercury_range = slow_speed_ranges[1]

        # 进入了水星轨道附近，才显示水星轨道线
        if mercury_range[0] - 2 < time_data.total_days < mercury_range[1]:
            self.mercury_orbit_line.enabled = True
        else:
            self.mercury_orbit_line.enabled = False

        # 进入了金星轨道附近，才显示金星轨道线
        if venus_range[0] - 2 < time_data.total_days < venus_range[1]:
            self.venus_orbit_line.enabled = True
        else:
            self.venus_orbit_line.enabled = False

        # 默认运行速度因子为2倍
        run_speed_factor = 2

        for r in slow_speed_ranges:
            if r[0] < time_data.total_days < r[1]:
                # 进入了慢速范围，用指定的运行速度因子
                run_speed_factor = r[2]
            elif (r[0] - 2) < time_data.total_days < (r[1] + 5):
                # 距离慢速范围还有2天或者超出5天，逐步调整运行速度因子
                if time_data.total_days <= r[0]:
                    # 快要进入慢速范围（2天内），逐步减小运行速度因子，速度越来越慢，直到0.01倍
                    run_speed_factor = UrsinaConfig.run_speed_factor - 0.01
                    if run_speed_factor < 0.01:
                        run_speed_factor = 0.01
                elif time_data.total_days >= r[1]:
                    # 超出了慢速范围（5天内），逐步增加运行速度因子，速度越来越快，直到2倍
                    run_speed_factor = UrsinaConfig.run_speed_factor + 0.05
                    if run_speed_factor > 2:
                        run_speed_factor = 2
                break

        UrsinaConfig.run_speed_factor = run_speed_factor

        if abs(self.earth.position[2]) < self.venus_radius and not self.arrived_venus_orbit_line:
            # 地球的位置小于金星轨道半径，则显示消息
            self.arrived_venus_orbit_line = True  # arrived_venus_orbit_line 保证只会运行一次
            msg = "地球在[%s]穿过金星轨道" % time_data.time_text
            print(msg)
            self.arrived_info = self.arrived_info + "\n\n" + msg
            print("金星：", self.venus.position, self.venus.velocity)
            # 显示 “地球在[某个时间]穿过金星轨道” 的消息
            ControlUI.current_ui.show_message(msg, close_time=5)

        if abs(self.earth.position[2]) < self.mercury_radius and not self.arrived_mercury_orbit_line:
            # 地球的位置小于水星轨道半径，则显示消息
            self.arrived_mercury_orbit_line = True  # arrived_mercury_orbit_line 保证只会运行一次
            msg = "地球在[%s]穿过水星轨道" % time_data.time_text
            print(msg)
            self.arrived_info = self.arrived_info + "\n\n" + msg
            print("水星：", self.mercury.position, self.mercury.velocity)
            # 显示 “地球在[某个时间]穿过水星轨道” 的消息
            ControlUI.current_ui.show_message(msg, close_time=5)

        self.text_panel.text = self.arrived_info. \
            replace("${distance}", "%s km" % distance_str). \
            replace("${acceleration}", "%s" % acceleration_info). \
            replace("${velocity}", "%s km/s" % round(velocity, 2))


if __name__ == '__main__':
    """
    地球停止公转，多久到达太阳
    地球如果停止公转，多久能掉入太阳？
    https://www.zhihu.com/question/310815418
    如果地球停止公转，那它需要多久才会掉进太阳？
    https://www.guokr.com/article/440341
    如果地球停止公转坠向太阳，人类还能活多久？
    https://www.sohu.com/a/303263431_498139
    
    当地球停止公转，如果没有向外的向心力来抵消向内的引力，地球将开始朝着太阳坠落。
    据美国康奈尔大学的天文学家戴夫 · 罗斯坦（Dave Rothstein)的计算，
    地球将在65天后与太阳相撞，期间在第41天穿过金星的轨道，在第57天，我们将穿过水星的轨道
    
    地球[41天 07时]到达金星轨道
    地球[57天 01时]到达水星轨道
    地球[64天 13时]到达太阳表面
    """

    # 设置计时器的最小时间单位为分钟
    BodyTimer().min_unit = BodyTimer.MIN_UNIT_HOURS

    sim = EarthOrbitStoppedSim()

    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(sim.on_ready)
    # 订阅事件后，上面的函数功能才会起作用
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(sim.on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    # position=(0, 0, 0) 的位置是站在地球视角，可以观看月相变化的过程
    ursina_run(sim.bodies, SECONDS_PER_DAY, position=(0, 0.0001 * AU, -0.8 * AU),
               show_timer=True,
               show_grid=True)
