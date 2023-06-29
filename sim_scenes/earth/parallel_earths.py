# -*- coding:utf-8 -*-
# title           :平行宇宙的地球们
# description     :平行宇宙的地球们
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import random

from bodies import Earth, Moon
from common.consts import SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.sphere_sky import SphereSky
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


def sim_show():
    bodies = []
    num = 2
    r = 30000
    for x in range(-num, num):
        for y in range(-num, num):
            for z in range(-num, num):
                earth = Earth(init_position=[r * x, r * y, r * z],
                              rotation_speed=0,
                              rotate_angle=0,
                              init_velocity=[0, 0, 0], size_scale=1, ignore_mass=True)
                # earth.rotation_speed /= 50  # 地球的转速降低50倍
                bodies.append(earth)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY,
               position=(0, 0, -r * num * 6), show_grid=False
               )


def ursina_show():
    from ursina import Ursina, Entity, color, EditorCamera, camera
    app = Ursina()
    SphereSky(texture='../../textures/bg_black.png')
    num = 5
    num_x = num * 2
    num_y = num
    num_z = num * 2
    r = 10

    def create_sphere(x, y, z):
        sphere = Entity(model="sphere", texture='../../textures/earth2.jpg',
                        x=x * r * 2, y=y * r,  z=z * r * 2, scale=3)
        sphere.name = "%s:%s:%s" % (x, y, z)

        def update():
            def inner(s, b):
                if not hasattr(s, "initial_y"):
                    s.rotation_y -= 1
                # print(s.name, s.rotation_y)

            return inner(sphere, y)

        sphere.update = update

    for x in range(-num_x, num_x):
        for y in range(-num_y, num_y):
            for z in range(-num_z, num_z):
                create_sphere(x, y, z)

    ed = EditorCamera()
    camera.fov = 80
    ed.position = [0, 0, r/2]
    import sys
    camera.x_d = 1
    camera.y_d = 1
    camera.z_d = 1

    def camera_update():
        camera.world_rotation_y += 0.05
        camera.world_rotation_z += 0.01
        # camera.x += ((random.randint(100, 300) - 100) / 3000) * camera.x_d
        camera.y += ((random.randint(100, 300) - 100) / 5000) * camera.y_d
        # camera.z += ((random.randint(100, 300) - 100) / 3000) * camera.z_d
        range_val = 5
        # if camera.x > range_val:
        #     camera.x_d = -1
        # elif camera.x < -range_val:
        #     camera.x_d = 1
        if camera.y > range_val:
            camera.y_d = -1
        elif camera.y < -range_val:
            camera.y_d = 1
        # if camera.z > range_val:
        #     camera.z_d = -1
        # elif camera.z < -range_val:
        #     camera.z_d = 1

    sys.modules["__main__"].update = camera_update
    app.run()


if __name__ == '__main__':
    """
    平行宇宙的地球们
    """
    # sim_show()
    ursina_show()
