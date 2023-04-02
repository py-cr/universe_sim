# -*- coding:utf-8 -*-
# title           :ursina天体Planet
# description     :ursina天体Planet
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import Entity, Mesh, Text, color, destroy, Vec3

from simulators.ursina.ursina_mesh import create_arrow_line


class BodyTrail(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='sphere',
            collider='sphere',
            ignore_paused=True,
            **kwargs
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # print(key, self)
                if hasattr(self, "entity_infos"):
                    self.show_infos()

    def show_infos(self):

        if len(self.children) > 0:
            for c in self.children:
                destroy(c)
            return

        vel_info, vel_direction, vel_position = self.entity_infos["velocity"]
        acc_info, acc_direction, acc_position = self.entity_infos["acceleration"]

        v_arrow, v_line, v_text = create_arrow_line((0, 0, 0), tuple(vel_direction), parent=self,
                                                    label=vel_info, color=color.red, alpha=0.8, arrow_scale=0.5)
        a_arrow, a_line, a_text = create_arrow_line((0, 0, 0), tuple(acc_direction), parent=self,
                                                    label=acc_info, color=color.yellow, alpha=0.8, arrow_scale=0.5)
