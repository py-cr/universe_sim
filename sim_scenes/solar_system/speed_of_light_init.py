# -*- coding:utf-8 -*-
# title           :在太阳系中以光速运行
# description     :在太阳系中以光速运行
# author          :Python超人
# date            :2023-04-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Asteroids, Body
from common.consts import AU
from sim_scenes.func import create_text_panel
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera


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

        if self.__camera_follow_light == "SideView":
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

    def on_reset(self):
        """
        点击了重置按钮触发
        @return:
        """
        self.arrived_bodies.clear()  # 重置存放记录光体已到达天体列表
        self.arrived_info = "[00:00:00]\t从 [太阳] 出发\n\n"
        if self.text_panel is not None:
            self.text_panel.text = self.arrived_info

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

    def on_ready(self):
        """
        模拟器开始运行前触发
        @return:
        """
        self.text_panel = create_text_panel()
        self.text_panel.text = self.arrived_info

        if self.__camera_follow_light == "SideView":
            camera.parent = self.light_body.planet
            camera.rotation_y = -85
        elif self.__camera_follow_light == "ForwardView":
            # self.light_body.planet.enabled = False
            camera.parent = self.light_body.planet
            camera.rotation_y = -15

    def on_timer_changed(self, time_text, time_data):
        """
        计时器触发
        @param time_text: 计时器时间文本
        @param time_data: 计时器时间数据
        @return:
        """
        years, days, hours, minutes, seconds = time_data
        for body in self.bodies:
            if body is self.light_body or isinstance(body, Sun) \
                    or body in self.arrived_bodies or isinstance(body, Asteroids):
                # 对于光速天体、太阳、小行星群、“已到达天体列表”中的天体无需计算
                continue
            # 计算判断，如果光速天体距离到达了某个天体，就记录到“已到达天体列表”中
            if self.light_body.position[2] >= body.position[2]:
                self.arrived_bodies.append(body)
                if self.text_panel is not None:
                    self.arrived_info += f"[{time_text}]\t到达\t[{body.name}]\n\n"
                    self.text_panel.text = self.arrived_info
                    print(f"[{time_text}] 到达 [{body.name}]")
