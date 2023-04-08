# -*- coding:utf-8 -*-
# title           :创建一个宇宙网格对象
# description     :创建一个宇宙网格对象
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import Entity, camera


class SphereSky(Entity):
    def __init__(self, **kwargs):
        super().__init__(name='sky', model='sphere', texture='sky_default', scale=1000, double_sided=True)
        self.set_light_off()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.world_position = camera.world_position
