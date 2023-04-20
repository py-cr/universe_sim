# -*- coding:utf-8 -*-
# title           :钻石
# description     :钻石
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class Diamond(Obj):
    """
    钻石
    密度：3.51g/cm³
    """

    def __init__(self, name="钻石", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture=None, size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=3.51e3, color=(7, 0, 162),
                 trail_color=None, show_name=False,
                 parent=None, gravity_only_for=[]):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": density,
            "color": color,
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name,
            "parent": parent,
            "gravity_only_for": gravity_only_for,
            "model": "diamond"
        }
        super().__init__(**params)


if __name__ == '__main__':
    diamond = Diamond()
    print(diamond)
