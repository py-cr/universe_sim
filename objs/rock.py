# -*- coding:utf-8 -*-
# title           :岩石
# description     :岩石
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class Rock(Obj):
    """
    岩石
    """

    def __init__(self, name="岩石", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="rock1.png", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=None, show_name=False,
                 model="rock1.obj", rotation=(0, 0, 0),
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


# 对岩石进行缩放，保证 create_rock 保证创建的岩石大小差异不会过大
ROCK_SIZE_SCALE_FACTOR = {
    6: 1e-2,
    7: 1e-2
}


def create_rock(no: int = None, **kwargs):
    if no is not None:
        kwargs["model"] = f"rock{no}.obj"
        kwargs["texture"] = f"rock{no}.png"
    if "size_scale" in kwargs:
        kwargs["size_scale"] = kwargs["size_scale"] * ROCK_SIZE_SCALE_FACTOR.get(no, 1.0)
    else:
        kwargs["size_scale"] = ROCK_SIZE_SCALE_FACTOR.get(no, 1.0)

    rock = Rock(**kwargs)
    # print(rock)
    return rock


if __name__ == '__main__':
    for i in range(10):
        rock = create_rock(no=i % 8 + 1, name=f'岩石{i + 1}')
        print(rock)
