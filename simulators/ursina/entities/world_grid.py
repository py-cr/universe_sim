# -*- coding:utf-8 -*-
# title           :创建一个宇宙网格对象
# description     :创建一个宇宙网格对象
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import Entity, Grid, color
from simulators.ursina.ursina_mesh import create_arrow_line


class WorldGrid(Entity):
    """
    创建一个宇宙网格对象
    """

    def draw_axises(self):
        """
        画坐标轴
        @return:
        """

        arrow_x, line_x, text_x = create_arrow_line((0, 0, 0), (10, 0, 0), label="X", color=color.red)
        arrow_y, line_y, text_y = create_arrow_line((0, 0, 0), (0, 10, 0), label="Y", color=color.green)
        arrow_z, line_z, text_z = create_arrow_line((0, 0, 0), (0, 0, 10), label="Z", color=color.yellow)

    def __init__(self):
        super().__init__()
        s = 120
        grid = Entity(model=Grid(s, s), scale=s * 60, color=color.rgba(255, 255, 255, 20), rotation_x=90,
                      position=(0, -80, 0))
        grid.set_light_off()

        # self.draw_axises()
