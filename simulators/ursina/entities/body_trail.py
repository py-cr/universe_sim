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
            **kwargs
        )

        self.set_light_off()

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                # print(key, self)
                if hasattr(self, "entity_infos"):
                    self.show_infos()

    def show_infos(self):
        if not hasattr(self, "origin_alpha"):
            self.origin_color = self.color
            self.origin_alpha = self.alpha

        if len(self.children) > 0:
            for c in self.children:
                destroy(c)
            # self.color = self.origin_color
            self.alpha = self.origin_alpha
            return
        self.alpha = 0.2
        # self.color = get_inverse_color(self.origin_color)

        vel_info, vel_direction, vel_position = self.entity_infos["velocity"]
        acc_info, acc_direction, acc_position = self.entity_infos["acceleration"]

        v_arrow, v_line, v_text = create_arrow_line((0, 0, 0), tuple(vel_direction), parent=self,
                                                    label=vel_info, color=color.red, alpha=0.8, arrow_scale=0.5)
        if str(vel_info).startswith("0.00"):
            v_text.parent = self
            v_arrow.enabled = False
            v_line.enabled = False

        a_arrow, a_line, a_text = create_arrow_line((0, 0, 0), tuple(acc_direction), parent=self,
                                                    label=acc_info, color=color.yellow, alpha=0.8, arrow_scale=0.5)
        if str(acc_info).startswith("0.00"):
            a_text.parent = self
            a_arrow.enabled = False
            a_line.enabled = False


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
