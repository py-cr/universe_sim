# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟（月球始终一面朝向地球、月球对地球的扰动）
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================


from bodies import Sun, Earth, Moon
from objs import CoreValagaClas, SciFiBomber, WaterDrop
from common.consts import AU, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at, create_main_entity, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera

if __name__ == '__main__':
    """
    月球始终一面朝向地球
    月球对地球的扰动
    """
    OFFSETTING = 0
    WATER_SPEED = 400
    # TODO: 可以抵消月球带动地球的力，保持地球在原地
    # OFFSETTING = 0.01265
    sun = Sun(name="太阳", size_scale=6e1, init_position=[0, 0, -3 * AU]).set_ignore_gravity(True)
    earth_size_scale = 2.5e2
    resolution = 100
    earth = Earth(init_position=[0, -2500000, 0],
                  texture="earth-huge.jpg",
                  # rotate_angle=0,
                  rotation_speed=0,
                  init_velocity=[OFFSETTING, 0, 0],
                  size_scale=earth_size_scale).set_ignore_gravity(True).set_resolution(resolution)  # 地球放大 5 倍，距离保持不变
    # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
    clouds = Earth(name="地球云层", texture="transparent_clouds.png",
                   # rotate_angle=0,
                   rotation_speed=0,
                   init_position=[0, -2500000, 0],
                   size_scale=earth_size_scale * 1.01,
                   parent=earth).set_ignore_gravity(True).set_resolution(resolution)

    water_drop = WaterDrop(
        init_position=[0, 0, 0],
                           # texture="drops_bright.png",
                           # trail_color=[200, 200, 255],
                           init_velocity=[0, 0, 0],
                           # size_scale=4e4,
                           size_scale=3e3
                           ).set_ignore_gravity(True).set_light_disable(True)
    # moon = Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
    #             init_velocity=[-1.03, 0, 0], size_scale=2e1)  # 月球放大 10 倍，距离保持不变
    # moon.set_light_disable(True)
    d = 100000
    num_x = 10
    num_y = 10
    num_z = 10

    # d = 100000
    # num_x = 2
    # num_y = 2
    # num_z = 2

    x_offset = - (num_x) / 2 * d
    y_offset = - (num_y) / 2 * (d / 2)
    z_offset = - (num_z) / 2 * d
    ship_list = []
    for x in range(num_x):
        for y in range(num_y):
            for z in range(num_z):
                core_valaga_clas = CoreValagaClas(size_scale=15,
                                                  init_position=[x_offset + (x + 0.5) * d,
                                                                 y_offset + (2 * y - 0.5) * (d / 2),
                                                                 z_offset + (z + 0.8) * d - 20000]).set_ignore_gravity(
                    True)
                ship_list.append(core_valaga_clas)

    for x in range(num_x):
        for y in range(num_y):
            for z in range(num_z):
                sci_fi_bomber = SciFiBomber(size_scale=3.5,
                                            init_position=[x_offset + (x + 0.5) * d,
                                                           y_offset + (2 * y - 1.5) * (d / 2),
                                                           z_offset + (z + 0.8) * d - 20000]).set_ignore_gravity(True)
                ship_list.append(sci_fi_bomber)

    # earth.rotation_speed /= 6  # 地球的转速降低50倍

    bodies = [earth, clouds, water_drop] + ship_list

    WATER_RANGE = 2e6


    def on_ready():
        from ursina import camera, time, Vec3, application
        UrsinaConfig.trail_type = 'line'
        UrsinaConfig.trail_length = 10
        for body in bodies:
            if isinstance(body, CoreValagaClas):
                body.planet.rotation_x = 0  # -10
            elif isinstance(body, SciFiBomber):
                body.planet.rotation_x = -90

        water_drop.planet.main_entity.rotation_z = 90
        water_drop.planet.main_entity.rotation_x = 45
        # water_drop.planet.main_entity.rotation_x = 90

        water_drop.init_position = (0, 0, 2000)
        water_drop.init_velocity = [0, 0, 0]
        application.time_scale = 1



    # # 订阅事件后，上面2个函数功能才会起作用
    # # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)


    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies,
               SECONDS_PER_DAY / 24,
               # SECONDS_PER_WEEK * 4,
               # position=(0, 0, -220000),
               position=(0, 0, -20000),
               # position=(0, 0, 0),
               show_grid=False,
               # cosmic_bg="",
               # gravity_works=False,
               save_cube_map=True,
               # show_timer=True,
               timer_enabled=True,
               show_camera_info=False,
               show_control_info=False,
               view_closely=True,
               show_trail=True
               )
