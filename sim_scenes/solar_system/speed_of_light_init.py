# -*- coding:utf-8 -*-
# title           :在太阳系中以光速运行
# description     :在太阳系中以光速运行
# author          :Python超人
# date            :2023-04-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Asteroids, Body
from common.consts import AU, LIGHT_SPEED, SECONDS_PER_MINUTE, SECONDS_PER_HOUR
from sim_scenes.func import create_text_panel
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera
import datetime


class SpeedOfLightInit:
    def __init__(self, camera_follow_light):
        """
        @param camera_follow_light: 三种不同的摄像机视角
                None         # 摄像机固定，不会跟随光
                ForwardView  # 摄像机跟随光，方向是向前看
                SideView     # 摄像机跟随光，方向是侧面看
        """
        # 存放记录光体已到达天体列表
        self.arrived_bodies = []
        # 显示消息面板（记录光体已到达天体的时间）
        self.text_panel = None
        # 显示消息面板的信息（记录光体已到达天体的时间）
        self.arrived_info = ""

        self.__camera_follow_light = camera_follow_light
        self.__light_body = None
        self.__bodies = None
        self.view_closely = False
        if self.__camera_follow_light in ["SideView", "SideViewActualSize"]:
            # 摄像机位置 = 前-后+、上+下-、左-右+、
            self.camera_position = (AU, 0, 0)
            self.show_trail = True
            self.light_size_scale = 1e3
            self.light_init_position = [AU / 3, 0, 0]
        elif self.__camera_follow_light == "ForwardView":
            # 摄像机位置 = 左-右+、上+下-、前+后-
            self.camera_position = (0, AU / 10, -AU)
            self.show_trail = True
            self.light_size_scale = 1e2
            self.light_init_position = [AU / 12, 0, 0]
        else:
            # 摄像机位置 = 左-右+、上+下-、前+后-
            self.camera_position = (0, AU, -6 * AU)
            self.show_trail = True
            self.light_size_scale = 2e3
            self.light_init_position = [AU / 3, 0, 0]

    @property
    def light_body(self):
        return self.__light_body

    @light_body.setter
    def light_body(self, value):
        self.__light_body = value

    @property
    def bodies(self):
        return self.__bodies

    @bodies.setter
    def bodies(self, value):
        self.__bodies = value
        if self.__camera_follow_light == "SideViewActualSize":
            # TODO: 将天体的大小不进行缩放
            for body in self.__bodies:
                if body is self.light_body:
                    continue
                body.size_scale = 1
            self.camera_position = [-self.light_init_position[0] / 1.35, 0, 0]
            self.view_closely = True

    def on_reset(self):
        """
        点击了重置按钮触发
        @return:
        """
        self.arrived_bodies.clear()  # 重置存放记录光体已到达天体列表
        self.arrived_info = "距离[太阳]：${distance}\n\n"
        if self.text_panel is not None:
            self.text_panel.text = self.arrived_info.replace("${distance}", "0 AU")

    def event_subscription(self):
        """
        订阅事件
        @return:
        """
        if self.light_body is None:
            raise Exception("请指定 SpeedOfLightInit.light_body")

        if self.bodies is None:
            raise Exception("请指定 SpeedOfLightInit.bodies")

        # 订阅重新开始事件
        UrsinaEvent.on_reset_subscription(self.on_reset)
        UrsinaEvent.on_ready_subscription(self.on_ready)
        # 订阅计时器事件（记录已到达天体列表）
        UrsinaEvent.on_timer_changed_subscription(self.on_timer_changed)

    def light_body_input(self, key):
        # TODO: 在这里控制光体的运动
        # if self.light_body.planet.hovered:
        if key == "w":
            # 上
            pass
        elif key == "s":
            # 上
            pass
        elif key == "a":
            # 左
            pass
        elif key == "d":
            # 右
            pass
            # self.light_body.velocity[1] = 1
            # self.light_body.planet.update()

    def on_ready(self):
        """
        模拟器开始运行前触发
        @return:
        """
        self.text_panel = create_text_panel()
        self.text_panel.text = self.arrived_info.replace("${distance}", "0 AU")

        if self.__camera_follow_light in ["SideView", "SideViewActualSize"]:
            camera.parent = self.light_body.planet
            camera.rotation_y = -85
        elif self.__camera_follow_light == "ForwardView":
            # self.light_body.planet.enabled = False
            camera.parent = self.light_body.planet
            self.light_body.planet.input = self.light_body_input
            camera.rotation_y = -15

    def auto_run_speed(self):
        # if self.__camera_follow_light != "SideViewActualSize":
        #     return

        run_speed_maps = [
            {"au": 0.008, "secs": 1},
            {"au": 0.36, "secs": SECONDS_PER_MINUTE * 2},
            {"au": 0.376, "secs": SECONDS_PER_MINUTE},
            {"au": 0.386, "secs": 1},  # [00:03:12] 到达 [水星] 0.384 AU
            {"au": 0.715, "secs": SECONDS_PER_MINUTE},
            {"au": 0.723, "secs": 1},  # [00:06:00] 到达 [金星] 0.721 AU
            {"au": 0.996, "secs": SECONDS_PER_MINUTE},
            {"au": 1.002, "secs": 1},  # [00:08:19] 到达 [地球] 1.0 AU
            {"au": 1.50, "secs": SECONDS_PER_MINUTE * 2},
            {"au": 1.516, "secs": SECONDS_PER_MINUTE},
            {"au": 1.522, "secs": 1},  # [00:12:39] 到达 [火星] 1.52 AU
            {"au": 5.1, "secs": SECONDS_PER_HOUR},
            {"au": 5.182, "secs": SECONDS_PER_MINUTE * 2},
            {"au": 5.192, "secs": 1},  # [00:43:10] 到达 [木星] 5.19 AU
            {"au": 9.44, "secs": SECONDS_PER_HOUR},
            {"au": 9.492, "secs": SECONDS_PER_MINUTE},
            {"au": 9.502, "secs": 1},  # [01:19:01] 到达 [土星] 9.5 AU
            {"au": 19.15, "secs": SECONDS_PER_HOUR},
            {"au": 19.192, "secs": SECONDS_PER_MINUTE},
            {"au": 19.202, "secs": 1},  # [02:39:41] 到达 [天王星] 19.2 AU
            {"au": 30.67, "secs": SECONDS_PER_HOUR},
            {"au": 30.692, "secs": SECONDS_PER_MINUTE},
            {"au": 30.702, "secs": 1},  # [04:15:19] 到达 [海王星] 30.7 AU
            {"au": 39.52, "secs": SECONDS_PER_HOUR * 1.2},
            {"au": 39.53, "secs": SECONDS_PER_MINUTE},
            {"au": 1000, "secs": 1}  # [05:28:55] 到达 [冥王星] 39.55 AU
        ]
        light_distance = self.light_body.position[2]
        for i, m in enumerate(run_speed_maps):
            if i == 0:
                au_min = 0
            else:
                au_min = run_speed_maps[i - 1]["au"]

            au_max = m["au"]

            if au_max * AU > light_distance >= au_min * AU:
                UrsinaConfig.seconds_per = m["secs"]

    def on_timer_changed(self, time_data: TimeData):
        """
        计时器触发
        @param time_data: 计时器时间数据
        @return:
        """
        self.auto_run_speed()

        for body in self.bodies:
            if body is self.light_body or isinstance(body, Sun) \
                    or body in self.arrived_bodies or isinstance(body, Asteroids):
                # 对于光速天体、太阳、小行星群、“已到达天体列表”中的天体无需计算
                continue
            # 计算判断，如果光速天体距离到达了某个天体，就记录到“已到达天体列表”中
            if self.light_body.position[2] >= body.position[2]:
                self.arrived_bodies.append(body)
                if self.text_panel is not None:
                    self.arrived_info += f"[{time_data.time_text}]\t到达\t[{body.name}]\n\n"
                    distance = round(self.light_body.position[2] / AU, 2)
                    self.text_panel.text = self.arrived_info.replace("${distance}", f"{distance} AU")
                    print(f"[{time_data.time_text}] 到达 [{body.name}] {round(self.light_body.position[2] / AU, 4)} AU")
                    return

        if not hasattr(self, "last_time"):
            self.last_time = datetime.datetime.now()
        else:
            if datetime.datetime.now() - datetime.timedelta(milliseconds=1000) > self.last_time:
                distance = round(self.light_body.position[2] / AU, 2)
                self.text_panel.text = self.arrived_info.replace("${distance}", f"{distance} AU")
                self.last_time = datetime.datetime.now()
