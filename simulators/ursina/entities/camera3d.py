# -*- coding:utf-8 -*-
# title           :创建一个宇宙网格对象
# description     :创建一个宇宙网格对象
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import Entity, camera

from common.consts import AU
from simulators.ursina.ursina_config import UrsinaConfig


class Camera3d(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

        camera.parent = self
        self.camera_pos = "right"
        # self.camera_l2r = 0.002 * AU * UrsinaConfig.SCALE_FACTOR
        self.camera_l2r = 0.0005

    def switch_position(self):
        if self.camera_pos == "right":  # 摄像机右眼
            self.x -= 2 * self.camera_l2r
            self.camera_pos = "left"
        elif self.camera_pos == "left":  # 摄像机左眼
            self.x += 2 * self.camera_l2r
            self.camera_pos = "right"

    def update(self):
        pass
