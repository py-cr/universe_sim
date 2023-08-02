# -*- coding:utf-8 -*-
# title           :水滴
# description     :水滴
# author          :Python超人
# date            :2023-08-02
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class WaterDrop(Obj):
    """
    水滴
    来源：https://www.cgmodel.com/model/500318.html
    """

    def __init__(self, name="水滴", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="drops.png", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=None, show_name=False,
                 model="drops.obj", rotation=(0, 0, 0),
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
    water_drop = WaterDrop(
        # texture="drops_normal.png"
        # texture="drops_uvw.png"
        texture="drops.png"
    )
    water_drop.init_velocity = [0, 0, -10]
    print(water_drop)


    def on_ready():
        water_drop.planet.rotation_x = 90


    water_drop.show_demo(size_scale=1000000, on_ready_fun=on_ready)
