# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Body, Sun, Earth, Moon
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from bodies.body import AU
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    地球、月球
    """
    OFFSETTING = 0
    # TODO: 可以抵消月球带动地球的力，保持地球在原地
    # OFFSETTING = 0.01265
    bodies = [
        Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
              init_velocity=[OFFSETTING, 0, 0], size_scale=0.5e1),  # 地球放大 5 倍，距离保持不变
        Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
             init_velocity=[-1.03, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
    ]

    from ursina.shaders import lit_with_shadows_shader
    from ursina import Vec2, Vec4, Entity

    shader = lit_with_shadows_shader
    shader.default_input = {
        'texture_scale': Vec2(1, 1),
        'texture_offset': Vec2(0, 0),
        'shadow_color': Vec4(0.1, 0.1, 0.1, .5),
    }
    Entity.default_shader = shader

    def on_ready():

        Entity.body = Entity(model="sphere", texture='../textures/transparent.png', y=0, x=0, z=0,scale=10)
        # 运行前触发
        # 运行开始前，将摄像机指向地球
        earth = bodies[0]
        moon = bodies[1]
        # 摄像机看向地球
        camera_look_at(earth)
        e_pos = earth.planet.position
        from ursina.lights import DirectionalLight
        sun = DirectionalLight(shadow_map_resolution=(1024, 1024), position=earth.planet.position)
        sun.look_at(moon.planet.position)
        sun.rotation_x = 0
        Entity.sun = sun
        # sun._light.show_frustum()
        # 创建太阳光
        shadows_shader = create_directional_light(position=(200, 0, -300), target=earth, shadows=True)
        earth.planet.shadows = shadows_shader
        moon.planet.shadows = shadows_shader


    def on_timer_changed(time_data):
        Entity.sun.update_bounds()
        # Entity.sun.update_bounds(bodies[1].planet)
        pass


    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY,
               position=(-300000, 1500000, -1000),
               show_timer=True,
               show_trail=True)
