# -*- coding:utf-8 -*-
# title           :高清水星3D效果
# description     :高清水星3D效果
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Mercury
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY
from sim_scenes.func import ursina_run
from simulators.ursina.entities.camera3d import Camera3d
from simulators.ursina.ursina_config import UrsinaConfig

if __name__ == '__main__':
    """
    高清水星3D效果
    """
    bodies = [
        Mercury(texture="mercury_hd.jpg",
                init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                size_scale=1, show_name=False)
    ]
    mercury = bodies[0]
    init_pos = (2.0 * mercury.radius * UrsinaConfig.SCALE_FACTOR,
                0,
                -14000 * UrsinaConfig.SCALE_FACTOR)
    Camera3d.init(init_pos)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY, position=(0, 0, 0),
               # cosmic_bg="textures/cosmic1.jpg",
               view_closely=0.001)
