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

    water_drop = WaterDrop(init_position=[AU / 300, 0, AU / 100],
                           texture="drops_bright.png",
                           # trail_color=[200, 200, 255],
                           init_velocity=[-WATER_SPEED, 0, 0],
                           # size_scale=4e4,
                           size_scale=1e3
                           ).set_ignore_gravity(True).set_light_disable(True)
    # moon = Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
    #             init_velocity=[-1.03, 0, 0], size_scale=2e1)  # 月球放大 10 倍，距离保持不变
    # moon.set_light_disable(True)
    d = 100000
    num_x = 10
    num_y = 10
    num_z = 10

    d = 100000
    num_x = 2
    num_y = 2
    num_z = 2

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

    bodies = [sun, earth, clouds, water_drop] + ship_list

    WATER_RANGE = 2e6

    # def calc_velocity(current_pos, to_pos, velocity_fact):
    #     """
    #     计算一个物体，从物体当前位置（三维坐标系）到达指定位置（三维坐标系）的矢量速度 x,y,z 分量的速度( * 速度因子 velocity_fact）
    #     @param current_pos: 物体当前位置（三维坐标系）
    #     @param to_pos: 指定位置（三维坐标系）
    #     @param velocity_fact: 速度因子
    #     @return: 矢量速度 x,y,z 分量的速度
    #     """
    #     velocity = [0, 0, 0]
    #     # TODO:在这里实现代码
    #
    #     return velocity
    import math


    def calc_acceleration(current_pos, to_pos, desired_velocity):
        """
        Calculate the acceleration vector components (x, y, z) for an object to move from its current position to a specified position,
        considering the desired velocity.
        @param current_pos: Current position of the object (in a three-dimensional coordinate system)
        @param to_pos: Specified position (in a three-dimensional coordinate system)
        @param desired_velocity: Desired velocity of the object
        @return: Acceleration vector components (x, y, z)
        """
        acceleration = [0, 0, 0]
        # Calculate the differences in each dimension
        diff_x = to_pos[0] - current_pos[0]
        diff_y = to_pos[1] - current_pos[1]
        diff_z = to_pos[2] - current_pos[2]
        # Calculate the total distance
        total_distance = math.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)
        # Calculate the time required to reach the specified position
        time = total_distance / desired_velocity
        # Calculate the acceleration required to reach the desired velocity in the calculated time
        acceleration_magnitude = desired_velocity / time
        # Calculate the acceleration in each dimension
        acceleration[0] = diff_x / time
        acceleration[1] = diff_y / time
        acceleration[2] = diff_z / time
        # Adjust the acceleration using the acceleration magnitude
        acceleration[0] *= acceleration_magnitude
        acceleration[1] *= acceleration_magnitude
        acceleration[2] *= acceleration_magnitude
        return acceleration


    def calc_velocity(current_pos, to_pos, velocity_fact):
        """
        Calculate the velocity vector components (x, y, z) for an object to move from its current position to a specified position,
        considering the velocity factor.
        @param current_pos: Current position of the object (in a three-dimensional coordinate system)
        @param to_pos: Specified position (in a three-dimensional coordinate system)
        @param velocity_fact: Velocity factor
        @return: Velocity vector components (x, y, z)
        """
        velocity = [0, 0, 0]
        # Calculate the differences in each dimension
        diff_x = to_pos[0] - current_pos[0]
        diff_y = to_pos[1] - current_pos[1]
        diff_z = to_pos[2] - current_pos[2]
        # Calculate the total distance
        total_distance = math.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)
        # Calculate the proportions of velocity in each dimension
        velocity[0] = diff_x / total_distance
        velocity[1] = diff_y / total_distance
        velocity[2] = diff_z / total_distance
        # Adjust the velocity using the velocity factor
        velocity[0] *= velocity_fact
        velocity[1] *= velocity_fact
        velocity[2] *= velocity_fact
        return velocity


    def on_timer_changed(time_data: TimeData):
        if time_data.total_days > 0.2:
            if water_drop.position[0] < -WATER_RANGE:
                water_drop.planet.rotation_z = -90
                water_drop.velocity = [WATER_SPEED, 0, 0]
            elif water_drop.position[0] > WATER_RANGE:
                water_drop.planet.rotation_z = 90
                water_drop.velocity = [-WATER_SPEED, 0, 0]
            else:
                velocity = calc_velocity(water_drop.position, ship_list[0].position, 5)
                water_drop.velocity = velocity

                # acceleration = calc_acceleration(water_drop.position, ship_list[0].position, 1e-4)
                # water_drop.acceleration = acceleration  # [-9.8e-4, 0, 0]

                water_drop.look_at(ship_list[0], rotation_x=None, rotation_y=None, rotation_z=None)

        camera_look_at(water_drop, rotation_z=0)
        # camera.y += UrsinaConfig.SCALE_FACTOR * 100

        for ship in ship_list:
            # 循环判断每个石头与木星是否相碰撞，如果相碰撞就爆炸
            if two_bodies_colliding(water_drop, ship):
                # velocity = water_drop.velocity
                # acceleration = water_drop.acceleration

                # 将石头隐藏、设置引力无效后，展示爆炸效果
                water_drop.explode(ship, scale=1e1, fps=0.5)
                # water_drop.planet.enabled = True
                # water_drop.set_ignore_gravity(False)
                #
                # water_drop.velocity = velocity
                # water_drop.acceleration = acceleration


    def on_ready():
        UrsinaConfig.trail_type = 'line'
        UrsinaConfig.trail_length = 10
        for body in bodies:
            if isinstance(body, CoreValagaClas):
                body.planet.rotation_x = 0  # -10
            elif isinstance(body, SciFiBomber):
                body.planet.rotation_x = -90

        water_drop.planet.main_entity.rotation_z = 90

        water_drop.init_position = (0, 0, 2000)
        water_drop.init_velocity = [0, 0, 0]

        create_main_entity(water_drop, rotation_y=90)


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

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
               # save_cube_map=True,
               show_timer=True,
               timer_enabled=True,
               show_camera_info=False,
               show_control_info=False,
               view_closely=True,
               show_trail=True
               )
