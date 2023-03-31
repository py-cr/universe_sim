# -*- coding:utf-8 -*-
# title           :ursina天体Planet
# description     :ursina天体Planet
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import Entity, Mesh, Text, color, destroy

from simulators.ursina.ursina_config import UrsinaConfig


class BodyTrail(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='sphere',
            collider='sphere',
            ignore_paused=True,
            **kwargs
        )

    def input(self, key):
        # if self.hovered:
        #     if key == 'left mouse down':
        #         print(f"{self} was clicked!")
        #         self.text.enabled = True
        #     elif key == 'left mouse up':
        #         self.text.enabled = False
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
        # entity_infos = {"velocity": [vel_info, vel_direction, vel_position],
        #                       "acceleration": [acc_info, acc_direction, acc_position]}
        vel_info, vel_direction, vel_position = self.entity_infos["velocity"]
        acc_info, acc_direction, acc_position = self.entity_infos["acceleration"]

        verts_acc = [(0, 0, 0), tuple(acc_direction)]
        verts_vel = [(0, 0, 0), tuple(vel_direction)]

        acc_line = Entity(parent=self, model=Mesh(vertices=verts_acc, mode='line', thickness=3),
                          color=color.yellow, alpha=0.5)
        acc_line.set_light_off()

        vel_line = Entity(parent=self, model=Mesh(vertices=verts_vel, mode='line', thickness=3),
                          color=color.red, alpha=0.5)
        vel_line.set_light_off()

        vel_text = Text(vel_info, scale=50, billboard=True, parent=self,
                        font=UrsinaConfig.CN_FONT, background=False, color=color.red,
                        position=vel_position, alpha=0.5)
        vel_text.set_light_off()

        acc_text = Text(acc_info, scale=50, billboard=True, parent=self,
                        font=UrsinaConfig.CN_FONT, background=False, color=color.yellow,
                        position=acc_position, alpha=0.5)
        acc_text.set_light_off()
