# -*- coding:utf-8 -*-
# title           :场景用功能库
# description     :场景用功能库
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import matplotlib.pyplot as plt
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_HALF_DAY
from common.system import System
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from common.consts import LIGHT_SPEED


def mayavi_run(bodies, dt=SECONDS_PER_WEEK,
               view_azimuth=0, view_distance='auto', view_focalpoint='auto',
               bgcolor=(1 / 255, 1 / 255, 30 / 255)):
    """
    用 mayavi 查看运行效果
    :param bodies: 天体
    :param dt: 单位：秒，按时间差进行演变，值越小越精确，但演变速度会慢。
    :param view_azimuth: 观测方位角，可选，float类型（以度为单位，0-360），用x轴投影到x-y平面上的球体上的位置矢量所对的角度。
    :param view_distance: 观测距离，可选，float类型 or 'auto',一个正浮点数，表示距放置相机的焦点的距离。
    :param view_focalpoint: 观测焦点，可选，类型为一个由3个浮点数组成的数组 or 'auto'，，代表观测相机的焦点
    :param bgcolor:
    :return:
    """
    from mayavi import mlab
    from simulators.mayavi_simulator import MayaviSimulator
    # 宇宙背景色
    mlab.figure(bgcolor=bgcolor, size=(1440, 810))
    body_sys = System(bodies)
    simulator = MayaviSimulator(body_sys)
    simulator.run(dt)
    # azimuth:
    #    观测方位角，可选，float类型（以度为单位，0-360），用x轴投影到x-y平面上的球体上的位置矢量所对的角度。
    # elevation:
    #    观测天顶角，可选，float类型（以度为单位，0-180）, 位置向量和z轴所对的角度。
    # distance:
    #    观测距离，可选，float类型 or 'auto',一个正浮点数，表示距放置相机的焦点的距离。
    #    Mayavi 3.4.0中的新功能：'auto' 使得距离为观察所有对象的最佳位置。
    # focalpoint:
    #    观测焦点，可选，类型为一个由3个浮点数组成的数组 or 'auto'，，代表观测相机的焦点
    #    Mayavi 3.4.0中的新功能：'auto'，则焦点位于场景中所有对象的中心。
    # roll:
    #    控制滚动，可选，float类型，即摄影机围绕其轴的旋转
    # reset_roll:
    #    布尔值，可选。如果为True，且未指定“滚动”，则重置相机的滚动方向。
    # figure:
    #    要操作的Mayavi图形。如果为 None，则使用当前图形。
    mlab.view(azimuth=view_azimuth, distance=view_distance, focalpoint=view_focalpoint)
    # mlab.view(azimuth=-45, elevation=45, distance=100e8 * 2 * 2 * 4 * 4, focalpoint=[5e10, 5e10, 5e9])
    mlab.show()


def ursina_run(bodies,
               dt=SECONDS_PER_HALF_DAY,
               position=(0, 0, 0),
               # view_azimuth=0, 摄像头观测方位角，可选，float类型（以度为单位，0-360）
               # ignore_mass: 忽略所有天体的引力
               cosmic_bg=None,
               bg_music=None,
               show_grid=True,
               show_trail=False,
               show_name=False,
               show_timer=False,
               save_as_json=None,
               view_closely=False):
    """
    ursina 模拟器运行天体
    @param bodies: 天体集合
    @param dt:  单位：秒，按时间差进行演变，值越小越精确，但演变速度会慢。
    @param position:  摄像头位置
    @param cosmic_bg: 宇宙背景图片
    @param bg_music: 背景音乐
    @param show_grid: 是否显示空间网格
    @param show_trail: 是否显示拖尾
    @param show_name: 是否显示天体名称
    @param show_timer: 是否显示计时器
    @param save_as_json: 将所有天体的信息保存为 json 文件
    @param view_closely: 是否近距离查看天体
    @return:
    """

    from simulators.ursina_simulator import UrsinaSimulator
    from simulators.ursina.entities.ursina_player import UrsinaPlayer
    body_sys = System(bodies)

    if show_name:
        for body in body_sys.bodies:
            body.show_name = True

    if save_as_json is not None:
        try:
            body_sys.save_to_json(save_as_json, {"dt": dt, "position": position,
                                                 "show_trail": show_trail, "show_name": show_name})
            print(f"{save_as_json} 文件生成成功！")
        except Exception as e:
            raise Exception(f"{save_as_json} 文件生成失败！" + str(e))
        return
    simulator = UrsinaSimulator(body_sys)
    view_azimuth = 0  # 暂时未用
    player = UrsinaPlayer(position, view_azimuth, simulator.ursina_views)

    def callback_update():
        UrsinaEvent.on_application_run()
        for ursina_view in simulator.ursina_views:
            simulator.check_and_evolve()
            if ursina_view.appeared:
                ursina_view.update()

    import sys
    sys.modules["__main__"].update = callback_update
    if show_trail:
        UrsinaConfig.show_trail = show_trail
    simulator.run(dt,
                  cosmic_bg=cosmic_bg,
                  show_grid=show_grid,
                  show_timer=show_timer,
                  bg_music=bg_music,
                  view_closely=view_closely)


def mpl_run(bodies, dt=SECONDS_PER_WEEK, gif_file_name=None, gif_max_frame=200):
    """

    :param bodies: 天体
    :param dt: 单位：秒，按时间差进行演变，值越小越精确，但演变速度会慢。
    :param gif_file_name: 导出的 gif 文件名，如果为空，则显示动画
    :return:
    """
    from simulators.mpl_simulator import MplSimulator
    body_sys = System(bodies)
    simulator = MplSimulator(body_sys)

    simulator.run(dt, gif_file_name=gif_file_name, gif_max_frame=gif_max_frame)


COSMIC_BG_COLOR = "#002563"
COSMIC_FORE_COLOR = "white"


def create_fig_ax(styles={}):
    bg_color = styles["bg_color"] if "bg_color" in styles else COSMIC_BG_COLOR
    fore_color = styles["fore_color"] if "fore_color" in styles else COSMIC_FORE_COLOR
    if bg_color is None:
        fig = plt.figure('天体模拟运行效果', figsize=(20, 12))
    else:
        fig = plt.figure('天体模拟运行效果', figsize=(20, 12), facecolor=bg_color)
    ax = fig.gca(projection="3d")

    return fig, ax


def create_solar_system_bodies(ignore_mass=False, init_velocity=None):
    """
    创建太阳系天体（忽略质量，引力无效，初速度全部为0）
    太阳、小行星环、
    八大行星：木星(♃)、土星(♄)、天王星(♅)、海王星(♆)、地球(⊕)、金星(♀)、火星(♂)、水星(☿)
    冥王星
    以下展示的效果为太阳系真实的距离
    @return:
    """
    from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
    sun = Sun(name="太阳", size_scale=0.5e2)  # 太阳放大 50 倍，距离保持不变
    bodies = [
        sun,
        Mercury(name="水星", size_scale=1e3),  # 水星放大 1000 倍，距离保持不变
        Venus(name="金星", size_scale=1e3),  # 金星放大 1000 倍，距离保持不变
        Earth(name="地球", size_scale=1e3),  # 地球放大 1000 倍，距离保持不变
        Mars(name="火星", size_scale=1e3),  # 火星放大 1000 倍，距离保持不变
        # Asteroids(name="小行星群", size_scale=3.2e2,
        #           parent=sun),  # 小行星群模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=0.3e3),  # 木星放大 300 倍，距离保持不变
        Saturn(name="土星", size_scale=0.3e3),  # 土星放大 300 倍，距离保持不变
        Uranus(name="天王星", size_scale=0.4e3),  # 天王星放大 400 倍，距离保持不变
        Neptune(name="海王星", size_scale=1e3),  # 海王星放大 1000 倍，距离保持不变
        Pluto(name="冥王星", size_scale=10e3),  # 冥王星放大 10000 倍，距离保持不变(从太阳系的行星中排除)
    ]

    # 遍历所有天体，
    for idx, body in enumerate(bodies):
        body.set_ignore_mass(ignore_mass)  # 忽略质量（引力无效）
        if init_velocity is not None:
            body.init_velocity = init_velocity
    return bodies


def create_light_body(size_scale, init_position, speed=LIGHT_SPEED):
    """
    用天体模拟一个光子
    @param size_scale: 光体的大小
    @param init_position: 光体的初始位置
    @param speed: 光体的速度->1光速=299792.458 千米/秒(km/秒)
    @return:
    """
    from bodies import Body
    return Body(name='光速', mass=0, texture='metal.jpg', size_scale=size_scale, color=(255, 255, 0),
                init_position=init_position,
                init_velocity=[0, 0, speed]).set_light_disable(True)


def create_text_panel(width=0.35, height=.5):
    # 创建一个 Panel 组件
    from ursina import Text, Panel, color, camera, Vec3
    panel = Panel(
        parent=None,
        model='quad',
        # texture='white_cube',
        color=color.black,
        origin=(-.48, .48, -.48),
        scale=(width, height),
        position=(-.88, 0.3, 0),
        alpha=0.5
    )

    # 创建一个 Text 组件用于显示消息
    text = Text(
        parent=panel,
        text='',
        origin=(-.5, .5, -.5),
        scale=(height * 5, width * 5),
        font=UrsinaConfig.CN_FONT,
        # background=True,
        # background_color=color.clear
    )
    return text


if __name__ == '__main__':
    from bodies import Sun, Earth

    """
    太阳、地球
    """
    bodies = [
        Sun(size_scale=1.2e2),  # 太阳放大 120 倍
        Earth(size_scale=4e3, distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    ]
    # mpl_run(bodies, SECONDS_PER_WEEK)
    ursina_run(bodies, SECONDS_PER_WEEK)
