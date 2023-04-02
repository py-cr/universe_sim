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

from simulators.ursina.ursina_config import UrsinaConfig
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
        #
        # verts_acc = [(0, 0, 0), tuple(acc_direction)]
        # verts_vel = [(0, 0, 0), tuple(vel_direction)]

        # acc_arrow = Arrow(parent=self,from_pos=Vec3((0, 0, 0)), to_pos=Vec3(tuple(acc_direction)),color=color.yellow, alpha=0.5)
        # acc_arrow.set_light_off()

        v_arrow, v_line, v_text = create_arrow_line((0, 0, 0), tuple(vel_direction), parent=self,
                                                    label=vel_info, color=color.red, alpha=0.8, arrow_scale=0.5)
        a_arrow, a_line, a_text = create_arrow_line((0, 0, 0), tuple(acc_direction), parent=self,
                                                    label=acc_info, color=color.yellow, alpha=0.8, arrow_scale=0.5)

        # acc_line = Entity(parent=self, model=Mesh(vertices=verts_acc, mode='line', thickness=3),
        #                   color=color.yellow, alpha=0.5)
        # acc_line.set_light_off()
        #
        # # vel_arrow = Arrow(parent=self,from_pos=Vec3((0, 0, 0)), to_pos=Vec3(tuple(vel_direction)),color=color.red, alpha=0.5)
        # # vel_arrow.set_light_off()
        #
        # vel_line = Entity(parent=self, model=Mesh(vertices=verts_vel, mode='line', thickness=3),
        #                   color=color.red, alpha=0.5)
        # vel_line.set_light_off()
        #
        # vel_text = Text(vel_info, scale=50, billboard=True, parent=self,
        #                 font=UrsinaConfig.CN_FONT, background=False, color=color.red,
        #                 position=vel_position, alpha=0.5)
        # vel_text.set_light_off()
        #
        # acc_text = Text(acc_info, scale=50, billboard=True, parent=self,
        #                 font=UrsinaConfig.CN_FONT, background=False, color=color.yellow,
        #                 position=acc_position, alpha=0.5)
        # acc_text.set_light_off()


class Arrow(Entity):
    def __init__(self, parent, from_pos=(0, 0, 0), to_pos=(1, 0, 0), **kwargs):
        from_pos = to_pos / 2
        super().__init__(parent=parent, model='arrow', position=from_pos, **kwargs)
        # self.x = -pos[1]
        # self.y = pos[2]
        # self.z = pos[0]
        to_pos = 1000 * to_pos
        # to_pos = -to_pos[2],-to_pos[1],to_pos[0]
        # to_pos = -to_pos[2],-to_pos[0],to_pos[1]
        # to_pos = to_pos[0],to_pos[2],to_pos[1]
        # to_pos = -to_pos[0],to_pos[1],to_pos[2]
        # to_pos = to_pos[1], -to_pos[0], -to_pos[2]
        # to_pos = to_pos[1], -to_pos[0], -to_pos[2]
        self.rotation = (0, 0, 0)
        self.look_at(to_pos)
        print(self.rotation)
        # self.model = Mesh(vertices=[
        #     from_pos,
        #     from_pos + (to_pos - from_pos) * 0.9,
        #     from_pos + (to_pos - from_pos) * 0.9 + Vec3(0, 0.1, 0),
        #     to_pos,
        #     from_pos + (to_pos - from_pos) * 0.9 - Vec3(0, 0.1, 0),
        #     from_pos + (to_pos - from_pos) * 0.9
        # ], mode='triangle', thickness=thickness)
        #
        # self.color = color
        # self.look_at(to_pos)
        # self.scale_z = (to_pos - from_pos).length()

# class Arrow(Entity):
#     def __init__(self,parent, from_pos, to_pos, **kwargs):
#         super().__init__(parent=parent, model='arrow', **kwargs)
#         self.position = from_pos
#         self.look_at(to_pos)


# import numpy as np
# def draw_arrow(parent, from_pos, to_pos, color, alpha):
#     # 计算方向向量和长度
#     p1 = np.array(from_pos)
#     p2 = np.array(to_pos)
#     direction = p2 - p1
#     length = np.linalg.norm(direction)
#
#     # 创建箭头实体
#     arrow = Entity(parent=parent, model="arrow", scale=(1, 1, length),color=color,alpha=alpha)
#
#     # 设置箭头位置和方向
#     arrow_position = p1 + direction/2
#     arrow.position = arrow_position
#     arrow.look_at(p2)
#
#     return arrow
