# -*- coding:utf-8 -*-
# title           :太空飞船
# description     :太空飞船
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class StarWarsSpeeder(Obj):
    """
    太空战机
    来源：https://www.3dcool.net/model/12/65699.html
    """

    def __init__(self, name="太空战机", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="star_wars_speeder.jpg", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=None, show_name=False,
                 model="star_wars_speeder.obj", rotation=(0, 0, 0),
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
            "rotation": rotation,
            "gravity_only_for": gravity_only_for,
            "model": model
        }
        super().__init__(**params)


if __name__ == '__main__':
    star_wars_speeder = StarWarsSpeeder(size_scale=10000)
    print(star_wars_speeder)
    star_wars_speeder.show_demo()

