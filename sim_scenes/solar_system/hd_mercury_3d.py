# -*- coding:utf-8 -*-
# title           :高清水星3D效果
# description     :高清水星3D效果
# author          :Python超人
# date            :2023-07-26
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Mercury
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY
from sim_scenes.func import ursina_run

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

    # TODO: 开启3D摄像机
    from simulators.ursina.entities.camera3d import Camera3d
    # 3D摄像机初始化(眼睛的距离为1000公里效果)
    Camera3d.init(eye_distance=1000)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY,
               position=(2.0 * mercury.radius, 0, -14000),
               # cosmic_bg="",  # 无背景（黑色）
               show_grid=False,  # 不显示网格
               show_camera_info=False,  # 不显示摄像机信息
               show_control_info=False,  # 不显示控制提示信息
               view_closely=0.001)
