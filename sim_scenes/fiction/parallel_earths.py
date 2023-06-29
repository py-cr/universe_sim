# -*- coding:utf-8 -*-
# title           :平行宇宙的地球们
# description     :平行宇宙的地球们
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import random
import sys
from bodies import Earth, Moon
from common.consts import SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.sphere_sky import SphereSky
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


def sim_show():
    """
    使用模拟器（慢）
    @return:
    """
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
    """
    直接使用 ursina 模拟，无需考虑万有引力（性能高）
    @return:
    """
    from ursina import Ursina, Entity, color, EditorCamera, camera
    app = Ursina()
    # 黑色背景的宇宙背景
    SphereSky(texture='../../textures/bg_black.png')

    # 控制地球的数量，这里的 num 不代表数量
    # 地球数量 = num_x * num_y * num_z
    num = 5
    num_x = num * 2
    num_y = num
    num_z = num * 2
    # 控制运行的速度
    run_speed = 0.1
    # 控制地球之间的距离
    r = 10

    def create_earth(x, y, z):
        """
        在指定的三维坐标上创建地球
        @param x:
        @param y:
        @param z:
        @return:
        """
        earth = Entity(model="sphere", texture='../../textures/earth2.jpg',
                        x=x * r * 2, y=y * r,  z=z * r * 2, scale=3)
        earth.name = "%s:%s:%s" % (x, y, z)

        def update():
            def inner(s, b):
                if not hasattr(s, "initial_y"):
                    # 随机生成一个地球自转的初始量
                    s.initial_y = random.randint(20, 200) / 100 * run_speed
                # 地球进行自转
                s.rotation_y -= s.initial_y

            return inner(earth, y)

        earth.update = update

    for x in range(-num_x, num_x):
        for y in range(-num_y, num_y):
            for z in range(-num_z, num_z):
                create_earth(x, y, z)

    ed = EditorCamera()
    camera.fov = 80
    ed.position = [0, 0, r/2]

    # 控制摄像机三个维度的移动方向，值为 1 和 -1
    camera.x_d = 1
    camera.y_d = 1
    camera.z_d = 1

    def camera_update():
        # 更新摄像机位置和角度

        # 控制摄像机旋转（以y、z轴进行旋转）
        camera.world_rotation_y += 0.005
        camera.world_rotation_z += 0.001

        # 控制摄像机来回移动（x为左右移动，y为上下移动）
        camera.x += ((random.randint(100, 300) - 100) / 2500 * run_speed) * camera.x_d
        camera.y += ((random.randint(100, 300) - 100) / 5000 * run_speed) * camera.y_d
        # camera.z += ((random.randint(100, 300) - 100) / 3000 * run_speed) * camera.z_d
        range_val = 5
        if camera.x > range_val:
            camera.x_d = -1
        elif camera.x < -range_val:
            camera.x_d = 1
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
