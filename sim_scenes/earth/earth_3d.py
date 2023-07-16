# -*- coding:utf-8 -*-
# title           :地球3D效果
# description     :地球3D效果
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    地球3D效果
    """
    # 创建带有云层的地球
    earth = Earth(texture="earth_hd_trans.png",
                  rotate_angle=-23.44,
                  init_position=[0, 0, 0],
                  init_velocity=[0, 0, 0],
                  size_scale=1)
    # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
    clouds = Earth(name="地球云层", texture="transparent_clouds.png",
                   rotate_angle=-23.44,
                   size_scale=1.001, parent=earth)

    bodies = [earth, clouds]


    def on_ready():
        from ursina import camera
        # camera_look_at(earth, rotation_z=0)
        # camera.fov = 40


    def on_timer_changed(time_data: TimeData):
        pass


    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 订阅事件后，上面的函数功能才会起作用
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(1.2 * earth.radius, 0, -30000),
               show_grid=False,
               cosmic_bg="none",
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001
