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

from common.color_utils import get_inverse_color
from simulators.ursina.ursina_mesh import create_label
from simulators.ursina.ursina_mesh import create_arrow_line


class BodyTrail(Entity):
    def __init__(self, **kwargs):
        if "last_pos" in kwargs:
            from_pos = kwargs["last_pos"]
        else:
            from_pos = (0, 0, 0)

        if "to_pos" in kwargs:
            to_pos = kwargs["to_pos"]
        else:
            to_pos = (1, 1, 1)

        super().__init__(
            model='sphere',
            collider='sphere',
            ignore_paused=True,
            # highlight_color=color.red,  # Button 有效
            **kwargs
        )

        self.set_light_off()

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # print(key, self)
                self.show_infos()

    def show_infos(self):
        if not hasattr(self, "entity_infos"):
            return
        if not hasattr(self, "origin_alpha"):
            # self.origin_color = self.color
            self.origin_alpha = self.alpha

        if len(self.children) > 0:
            for c in self.children:
                destroy(c)
            # self.color = self.origin_color
            self.alpha = self.origin_alpha
            return
        self.alpha = 0.3
        # self.color = get_inverse_color(self.origin_color)

        vel_value, vel_direction, vel_position = self.entity_infos["velocity"]
        acc_value, acc_direction, acc_position = self.entity_infos["acceleration"]

        if vel_value >= 0.01:
            vel_info = "%.2fkm/s" % (vel_value)
        elif vel_value >= 0.00001:
            vel_info = "%.2fm/s" % (vel_value * 1000)
        elif vel_value >= 0.00000001:
            vel_info = "%.2fmm/s" % (vel_value * 1000 * 1000)
        else:
            vel_info = "0m/s"

        acc_m = acc_value * 1000

        if acc_m >= 0.01:
            acc_info = "%.2fm/s²" % (acc_m)
        elif acc_m >= 0.00001:
            acc_info = "%.2fmm/s²" % (acc_m * 1000)
        # elif acc_m >= 0.00000001:
        #     acc_info = "%.2fμm/s²" % (acc_m * 1000 * 1000)
        else:
            acc_info = "0m/s²"

        if vel_value < 0.00000001:
            create_label(parent=self, label=vel_info, pos=Vec3(-0.5, -0.5, -0.5), color=color.red).set_light_off()
            # v_text.parent = self
            # # v_arrow.enabled = False
            # # v_line.enabled = False
        else:
            v_arrow, v_line, v_text = create_arrow_line((0, 0, 0), tuple(vel_direction), parent=self,
                                                        label=vel_info, color=color.red, alpha=0.8, arrow_scale=0.5)

        if acc_m < 0.00001:
            create_label(parent=self, label=acc_info, pos=Vec3(0.5, 0.5, 0.5), color=color.green).set_light_off()
            # a_text.parent = self
            # a_arrow.enabled = False
            # a_line.enabled = False
        else:
            a_arrow, a_line, a_text = create_arrow_line((0, 0, 0), tuple(acc_direction), parent=self,
                                                        label=acc_info, color=color.green, alpha=0.8, arrow_scale=0.5)


class BodyTrailLine_OK(Entity):
    def __init__(self, **kwargs):
        if "last_pos" in kwargs:
            from_pos = kwargs["last_pos"]
        else:
            from_pos = (0, 0, 0)

        if "to_pos" in kwargs:
            to_pos = kwargs["to_pos"]
        else:
            to_pos = (1, 1, 1)
        super().__init__(
            # model='line',
            model=Mesh(vertices=(from_pos, to_pos), mode='line', thickness=3),
            ignore_paused=True,
            **kwargs
        )


class BodyTrailLine(Entity):
    def __init__(self, **kwargs):
        if "direction" in kwargs:
            direction = kwargs["direction"]
        else:
            direction = (0, 0, 0)

        super().__init__(
            # model='line',
            model=Mesh(vertices=((0, 0, 0), direction), mode='line', thickness=2),
            ignore_paused=True,
            **kwargs
        )
