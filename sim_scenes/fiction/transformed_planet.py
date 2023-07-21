# -*- coding:utf-8 -*-
# title           :改造后地球的3D效果
# description     :改造后地球的3D效果
# author          :Python超人
# date            :2023-07-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import numpy as np

from bodies import Earth
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run, camera_look_at, create_3d_card
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.camera3d import Camera3d
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera
import os


def run_transformed_planet(texture, with_clouds=True, camera3d=False, transparent=True):
    if transparent:
        texture = texture.replace(".jpg", "_trans.png")

    # 创建带有云层的地球
    earth = Earth(
        texture=os.path.join("transformed", texture),
        rotate_angle=-23.44,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=1)
    bodies = [earth]
    if with_clouds:
        # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
        clouds = Earth(name="云层", texture="transparent_clouds.png",
                       rotate_angle=-23.44,
                       size_scale=1.001, parent=earth)

        bodies.append(clouds)

    init_pos = (1.45 * earth.radius,
                0,
                -30000)
    if camera3d:
        init_pos = np.array(init_pos) * UrsinaConfig.SCALE_FACTOR
        Camera3d.init(init_pos)
        init_pos = (0, 0, 0)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=init_pos,
               show_grid=False,
               show_camera_info=False,
               show_control_info=False,
               cosmic_bg="none",
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001


if __name__ == '__main__':
    """
    改造后地球的3D效果
    """
    run_transformed_planet(
        "earth.jpg",
        camera3d=True,
        transparent=False
    )
