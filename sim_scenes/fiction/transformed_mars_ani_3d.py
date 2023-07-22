# -*- coding:utf-8 -*-
# title           :改造后火星的3D效果
# description     :改造后火星的3D效果
# author          :Python超人
# date            :2023-07-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import os

import numpy as np

from bodies import Earth
from common.consts import SECONDS_PER_HOUR
from sim_scenes.func import ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.camera3d import Camera3d
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


def transformed_mars_ani(transformed_texture=None, texture=None, camera3d=False):
    trans_texture = transformed_texture.replace(".jpg", "_trans.png")
    # texture = transformed_texture
    # texture = os.path.join("transformed", texture)

    # 创建带有云层的地球
    mars = Earth(
        texture=texture,
        rotate_angle=0,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=1)

    transformed_mars = Earth(
        texture=os.path.join("transformed", transformed_texture),
        rotate_angle=0,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=0.999)

    trans_mars = Earth(
        texture=os.path.join("transformed", trans_texture),
        rotate_angle=0,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=0.995)

    bodies = [mars, transformed_mars, trans_mars]

    # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
    clouds = Earth(name="云层", texture="transparent_clouds.png",
                   rotate_angle=0,
                   size_scale=1.001, parent=mars)

    bodies.append(clouds)

    init_pos = (1.45 * mars.radius,
                0,
                -30000)
    if camera3d:
        init_pos = np.array(init_pos) * UrsinaConfig.SCALE_FACTOR
        Camera3d.init(init_pos)
        init_pos = (0, 0, 0)

    def on_ready():
        pass

    def on_timer_changed(time_data: TimeData):
        # mars.planet.opacity = 0.01
        opacity = round((time_data.total_hours - 1) / 10, 2)
        clouds_opacity = round(opacity - 0.5, 2)
        if opacity > 1.0:
            opacity = 1.0
        elif opacity < 0.0:
            opacity = 0.0
        # clouds.planet.enabled = False
        if opacity >= 1.0:
            mars.planet.enabled = False  # 原火星完全消失

        if clouds_opacity > 1.0:
            clouds_opacity = 1.0
        elif clouds_opacity < 0.0:
            clouds_opacity = 0.0

        clouds.planet.alpha = clouds_opacity  # 火星云层渐渐显示
        mars.planet.alpha = 1 - opacity  # 原火星渐渐消失

        # if time_data.total_hours > 10:
        #     trans_mars.planet.enabled = True
        # else:
        #     trans_mars.planet.enabled = False
        # if mars.planet.enabled == False:
        #     opacity = round((time_data.total_hours*5 - 11) / 10, 2)
        #     if opacity > 1.0:
        #         opacity = 1.0
        #     elif opacity < 0.0:
        #         opacity = 0.0
        #     transformed_mars.planet.alpha = 0.9
        #     trans_mars.planet.enabled = False

    # 订阅事件后，上面2个函数功能才会起作用
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=init_pos,
               show_grid=False,
               show_camera_info=False,
               show_control_info=False,
               # cosmic_bg="none",
               timer_enabled=True,
               show_timer=True,
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001


if __name__ == '__main__':
    transformed_mars_ani(
        transformed_texture="mars.jpg",
        texture="mars.png",
        camera3d=False
    )
