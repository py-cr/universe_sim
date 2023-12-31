# -*- coding:utf-8 -*-
# title           :卫星
# description     :卫星
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class Satellite(Obj):
    """
    卫星
    """

    def __init__(self, name="卫星", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="satellite.png", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=(255, 255, 255), show_name=False,
                 trail_scale_factor=1.0, model="satellite.obj",
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
            "trail_scale_factor": trail_scale_factor,
            "show_name": show_name,
            "parent": parent,
            "gravity_only_for": gravity_only_for,
            "model": model
        }
        super().__init__(**params)


class Satellite2(Obj):
    """
    卫星
    """

    def __init__(self, name="卫星", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="satellite2.jpg", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=(255, 255, 255), show_name=False,
                 model="satellite2.obj",
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
            "model": model
        }
        super().__init__(**params)


if __name__ == '__main__':
    satellite = Satellite2()
    print(satellite)
