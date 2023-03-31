# -*- coding:utf-8 -*-
# title           :UrsinaPlayer
# description     :UrsinaPlayer
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import camera, color, mouse, Vec2, Vec3, Vec4, Text
from ursina.prefabs.first_person_controller import FirstPersonController
from simulators.ursina.ursina_config import UrsinaConfig
import numpy as np


class UrsinaPlayer(FirstPersonController):
    """

    """

    # body_rotation_speed_control = 1.0

    def __init__(self, position, view_azimuth=0, targets=None):
        super().__init__()
        # camera.fov = 2000 # 100
        # camera.rotation_y = 90
        self.planets = None
        if targets is not None:
            self.planets = []
            # targets = [view.planet.parent for view in targets]
            # targets_parent = Entity()
            for view in targets:
                # view.planet.parent = targets_parent
                self.planets.append(view.planet)
            # self.camera_adj(planets)
            #     # planets.append(view.planet)
            #
            # camera.add_script(SmoothFollow(targets_parent, offset=(0, 8, -20)))
        pos = np.array(position) * UrsinaConfig.SCALE_FACTOR
        self.position = Vec3(pos[0], pos[1], pos[2])
        # 将摄像机位置设置为 x=0、y=1、z=0 的位置
        camera.position = Vec3(pos[0], pos[1], pos[2])
        # self.x = 90
        # self.position = Vec3(pos[0], pos[1], pos[2])
        # 将摄像机的观察角度绕 x 轴旋转 45 度，绕 y 轴旋转 0 度，绕 z 轴旋转 0 度
        # self.rotation = Vec3(45, 90, 0)
        # camera.look_at(Vec3(0, 0, 0))
        # camera.world_rotation = Vec3(0, 190, 190)
        # camera.enabled = True
        # self.gravity = 0
        # self.vspeed = 400
        # self.speed = 1000
        # self.mouse_sensitivity = Vec2(160, 160)
        # self.on_enable()
        # self.rotation_speed = 80

        self.on_disable()  # 防止鼠标被窗口锁定

    # def input(self, key):
    #     if key == "escape":
    #         if mouse.locked:
    #             self.on_disable()
    #         else:
    #             sys.exit()
    #     return super().input(key)
