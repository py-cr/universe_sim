# -*- coding:utf-8 -*-
# title           :地球3D效果
# description     :地球3D效果
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, AU
from sim_scenes.func import ursina_run, camera_look_at, create_3d_card
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.camera3d import Camera3d
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera

if __name__ == '__main__':
    """
    地球3D效果
    # sim_video_3d_cap.bat earth earth_3d
    """
    # 创建带有云层的地球
    earth = Earth(
        # texture="earth_hd.jpg",
        texture="earth_hd_trans.png",
        rotate_angle=-23.44,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=1)
    # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
    clouds = Earth(name="地球云层", texture="transparent_clouds.png",
                   rotate_angle=-23.44,
                   size_scale=1.001, parent=earth)

    bodies = [earth, clouds]
    # camera.camera_pos = "right"
    # camera_l2r = 0.002 * AU * UrsinaConfig.SCALE_FACTOR
    #
    #
    # def switch_position():
    #     if camera.camera_pos == "right":  # 摄像机右眼
    #         camera.world_position[0] -= 2 * camera_l2r
    #         camera.camera_pos = "left"
    #     elif camera.camera_pos == "left":  # 摄像机左眼
    #         camera.world_position[0] += 2 * camera_l2r
    #         camera.camera_pos = "right"
    #
    #
    # camera.switch_position = switch_position


    def on_ready():
        earth.camera3d = Camera3d()
        earth.camera3d.position = (1.45 * earth.radius * UrsinaConfig.SCALE_FACTOR,
                                   0,
                                   -30000 * UrsinaConfig.SCALE_FACTOR)

        # camera_look_at(earth, rotation_z=0)
        # camera.fov = 40
        earth._3d_card = create_3d_card()

    def on_before_evolving(evolve_args):
        earth._3d_card.switch_color()
        earth.camera3d.switch_position()
        if earth._3d_card.switch_flag == 1:
            evolve_args["evolve_dt"] = 0.0

    # 订阅事件后，上面的函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    UrsinaEvent.on_before_evolving_subscription(on_before_evolving)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR,
               # position=(1.2 * earth.radius, 0, -30000),
               position=(0, 0, 0),
               show_grid=False,
               show_camera_info=False,
               show_control_info=False,
               cosmic_bg="none",
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001
