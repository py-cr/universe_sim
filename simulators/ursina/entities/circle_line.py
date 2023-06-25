# -*- coding:utf-8 -*-
# title           :创建一个圆圈
# description     :创建一个圆圈
# author          :Python超人
# date            :2023-06-24
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import *
import math


class CircleLine(Entity):
    def __init__(self, radius, position=None, segments=100, thickness=0.1, color=color.white, alpha=1):
        super().__init__()
        self.radius = radius
        self.segments = segments
        self.thickness = thickness
        self.color = color
        self.alpha = alpha
        if position is None:
            position = (0, 0, 0)
        self.position = position
        # self.collider = 'sphere'
        self.create_circle_line()

    def create_circle_line(self):
        angle_step = 360 / self.segments
        r = self.radius * 1.4363
        for i in range(self.segments):
            angle = math.radians(i * angle_step)
            next_angle = math.radians((i + 1) * angle_step)

            # print(i/self.segments)
            #
            # if i/self.segments < 0.5:
            #     continue

            x = r * math.cos(angle)
            y = r * math.sin(angle)
            next_x = r * math.cos(next_angle)
            next_y = r * math.sin(next_angle)
            pos_x, pos_y, pos_z = self.position
            line = Entity(parent=self,
                          model=Mesh(vertices=((pos_x + x, pos_y + y, pos_z), (pos_x + next_x, pos_y + next_y, pos_z)),
                                     mode='line',
                                     thickness=self.thickness),
                          color=self.color, alpha=self.alpha)


if __name__ == '__main__':
    app = Ursina()

    window.borderless = False
    window.fullscreen = False
    window.title = "Circle Line"
    window.color = color.black
    circle_line = CircleLine(radius=2, segments=100, thickness=0.1, color=color.yellow, alpha=0.4)
    EditorCamera()
    app.run()
