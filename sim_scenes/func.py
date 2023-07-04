# -*- coding:utf-8 -*-
# title           :场景用功能库
# description     :场景用功能库
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import matplotlib.pyplot as plt
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_MINUTE, SECONDS_PER_HALF_DAY, AU
from common.func import calculate_distance
from common.system import System
from bodies import Body
from common.consts import LIGHT_SPEED
import math
import numpy as np


def calc_run(bodies, dt=SECONDS_PER_WEEK, on_init=None, **kwargs):
    from simulators.calc_simulator import CalcSimulator
    import copy
    if on_init is not None:
        _bodies = copy.deepcopy(bodies)
        _bodies = on_init(_bodies)
        if _bodies is None:
            _bodies = bodies
    else:
        _bodies = bodies

    body_sys = System(_bodies)
    simulator = CalcSimulator(body_sys)
    simulator.run(dt, **kwargs)


def mayavi_run(bodies, dt=SECONDS_PER_WEEK,
               view_azimuth=0, view_distance='auto', view_focalpoint='auto',
               bgcolor=(1 / 255, 1 / 255, 30 / 255)):
    """
    用 mayavi 查看运行效果
    @param bodies: 天体
    @param dt: 单位：秒，按时间差进行演变，值越小越精确，但演变速度会慢。
    @param view_azimuth: 观测方位角，可选，float类型（以度为单位，0-360），用x轴投影到x-y平面上的球体上的位置矢量所对的角度。
    @param view_distance: 观测距离，可选，float类型 or 'auto',一个正浮点数，表示距放置相机的焦点的距离。
    @param view_focalpoint: 观测焦点，可选，类型为一个由3个浮点数组成的数组 or 'auto'，，代表观测相机的焦点
    @param bgcolor:
    @return:
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


def set_camera_parent(target):
    from ursina import camera
    if hasattr(target, "planet"):
        camera.parent = target.planet.main_entity
    else:
        camera.parent = target


def camera_look_at(target, rotation_x=None, rotation_y=None, rotation_z=None):
    """
    让摄像机看向指定天体
    @param target: 天体
    @param rotation_x: x轴旋转角度（None表示不旋转）
    @param rotation_y: y轴旋转角度（None表示不旋转）
    @param rotation_z: z轴旋转角度（None表示不旋转）
    @return:
    """
    from ursina import camera
    if hasattr(target, "planet"):
        camera.look_at(target.planet.main_entity)
    else:
        camera.look_at(target)

    if rotation_x is not None:
        camera.rotation_x = rotation_x
    if rotation_y is not None:
        camera.rotation_y = rotation_y
    if rotation_z is not None:
        camera.rotation_z = rotation_z


def ursina_run(bodies,
               dt=SECONDS_PER_HALF_DAY,
               position=(0, 0, 0),
               # view_azimuth=0, 摄像头观测方位角，可选，float类型（以度为单位，0-360）
               # ignore_mass: 忽略所有天体的引力
               cosmic_bg=None,
               bg_music=None,
               show_grid=True,
               grid_position=None,
               grid_scale=None,
               show_trail=False,
               show_name=False,
               show_timer=False,
               timer_enabled=False,
               save_as_json=None,
               save_as_video=False,
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
    @param timer_enabled: 计时器是否有效
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

    if save_as_video:
        from common.video_recorder import VideoRecorder
        vr = VideoRecorder()

    def callback_update():
        UrsinaEvent.on_application_run()
        for ursina_view in simulator.ursina_views:
            simulator.check_and_evolve()
            if ursina_view.appeared:
                ursina_view.update()

        if save_as_video:
            vr.screenshot()

    import sys
    from simulators.ursina.ursina_config import UrsinaConfig
    from simulators.ursina.ursina_event import UrsinaEvent
    sys.modules["__main__"].update = callback_update
    if show_trail:
        UrsinaConfig.show_trail = show_trail
    simulator.run(dt,
                  cosmic_bg=cosmic_bg,
                  show_grid=show_grid,
                  grid_position=grid_position,
                  grid_scale=grid_scale,
                  show_timer=show_timer,
                  timer_enabled=timer_enabled,
                  bg_music=bg_music,
                  view_closely=view_closely)


def mpl_run(bodies, dt=SECONDS_PER_WEEK, gif_file_name=None, gif_max_frame=200):
    """

    @param bodies: 天体
    @param dt: 单位：秒，按时间差进行演变，值越小越精确，但演变速度会慢。
    @param gif_file_name: 导出的 gif 文件名，如果为空，则显示动画
    @return:
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
    from bodies import Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

    sun = Sun(name="太阳", size_scale=0.5e2)  # 太阳放大 50 倍，距离保持不变
    bodies = [
        sun,
        Mercury(name="水星", size_scale=0.3e3),  # 水星放大 300 倍，距离保持不变
        Venus(name="金星", size_scale=0.3e3),  # 金星放大 300 倍，距离保持不变
        Earth(name="地球", size_scale=0.3e3),  # 地球放大 300 倍，距离保持不变
        Moon(name="月球", init_position=[0, 0, 363104 + AU],
             size_scale=0.3e3),  # 月球放大 300 倍，距离保持不变
        Mars(name="火星", size_scale=0.3e3),  # 火星放大 300 倍，距离保持不变
        # Asteroids(name="小行星群", size_scale=3.2e2,
        #           parent=sun),  # 小行星群模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=0.3e3),  # 木星放大 300 倍，距离保持不变
        Saturn(name="土星", size_scale=0.3e3),  # 土星放大 300 倍，距离保持不变
        Uranus(name="天王星", size_scale=0.3e3),  # 天王星放大 300 倍，距离保持不变
        Neptune(name="海王星", size_scale=0.3e3),  # 海王星放大 300 倍，距离保持不变
        Pluto(name="冥王星", size_scale=0.3e3),  # 冥王星放大 300 倍，距离保持不变(从太阳系的行星中排除)
    ]

    # 遍历所有天体，
    for idx, body in enumerate(bodies):
        body.set_ignore_gravity(ignore_mass)  # 忽略质量（引力无效）
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


def create_light_ship(size_scale, init_position, speed=LIGHT_SPEED):
    """
    用天体模拟一个光速飞船
    @param size_scale: 光速飞船的大小
    @param init_position: 光速飞船的初始位置
    @param speed: 光速飞船的速度->1光速=299792.458 千米/秒(km/秒)
    @return:
    """
    from objs.space_ship import SpaceShip
    return SpaceShip(name='光速飞船', mass=0, size_scale=size_scale, color=(255, 110, 0),
                     init_position=init_position,
                     init_velocity=[0, 0, speed]).set_light_disable(True)


def create_3d_card(left=-.885, top=0.495, width=0.02, height=0.02):
    # 创建一个 Panel 组件
    from ursina import Text, Panel, color, camera, Vec3
    from simulators.ursina.ursina_config import UrsinaConfig
    panel = Panel(
        parent=None,
        model='quad',
        # texture='white_cube',
        color=color.black,
        origin=(-.48, .48, -.48),
        scale=(width, height),
        position=(left, top, 0)
    )

    def switch_color():
        if panel.color == color.black:
            panel.color = color.white
        else:
            panel.color = color.black

    panel.switch_color = switch_color

    return panel


def create_text_panel(width=0.35, height=.5):
    # 创建一个 Panel 组件
    from ursina import Text, Panel, color, camera, Vec3
    from simulators.ursina.ursina_config import UrsinaConfig
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


def get_vector2d_velocity(velocity, angle=15):
    """
    根据速度、角度获取矢量速度（vx、vy）
    @param velocity:
    @param angle:
    @return:
    """
    vy = math.sin(math.pi * angle / 180) * velocity
    vx = math.cos(math.pi * angle / 180) * velocity
    # vx² + vy² = velocity²
    return vx, vy


def two_bodies_colliding(body1: Body, body2: Body):
    """
    判断两个天体是否相撞
    @param body1:
    @param body2:
    @return:
    """
    if hasattr(body1, "planet") and hasattr(body2, "planet"):
        # 使用 Ursina 的算法
        if hasattr(body1.planet, "intersects"):
            return body1.planet.intersects(body2.planet).hit

    # 自行实现的算法，两物体的距离小于两物体半径的和，就视为碰撞了
    d = calculate_distance(np.array(body1.position) * body1.distance_scale,
                           np.array(body2.position) * body2.distance_scale)

    if d <= body1.radius * body1.size_scale + body2.radius * body2.size_scale:
        return True
    return False

    # raise Exception("two_bodies_colliding 不支持类型[body1 body2]")


def smooth_speed_transition2(run_speed_maps, transition_secs=1):
    """
    通过逐步调整速度在给定的过渡时间内实现运行速度地图中速度的圆滑过渡。
    参数：
        run_speed_maps: 运行速度分段的列表，每一个速度分段是一个字典，包含两个键值对{"au": au, "secs": seconds}，
                        其中au是以天文单位（AU）表示的距离，seconds则是以秒为单位的时间。
        transition_secs: 运行速度过渡的时间（秒数），默认为1秒。
    """
    # assuming 60 steps per second
    transition_steps = transition_secs * 60

    # 初始化速度分段序列
    speed_maps = []

    # 循环每一个分段
    for i, speed_map in enumerate(run_speed_maps):
        if i == 0:
            # 对于第一个分段，直接添加到速度分段序列中
            speed_maps.append(speed_map)
            continue
        if speed_map["secs"] <= 1:
            # 如果当前分段所用时间小于等于1秒，直接添加到速度分段序列中
            speed_maps.append(speed_map)
            continue
        # 否则，保存前一个速度分段
        prev_speed_map = run_speed_maps[i - 1]

        # 计算距离和时间差
        distance_diff = speed_map["au"] - prev_speed_map["au"]
        time_diff = speed_map["secs"] - prev_speed_map["secs"]

        # 计算每一步速度的变化值
        speed_per_step = distance_diff / time_diff / transition_steps

        # 添加过渡步数个过渡速度分段
        for j in range(transition_steps):
            tran_speed_map = {}
            # 计算过渡速度分段的距离和时间
            tran_speed_map["au"] = prev_speed_map["au"] + distance_diff * ((j + 1) / transition_steps)
            tran_speed_map["secs"] = prev_speed_map["secs"] + time_diff * ((j + 1) / transition_steps)
            # 计算过渡速度分段的速度
            tran_speed = prev_speed_map["au"] + speed_per_step * (j + 1)
            tran_speed_map["speed"] = tran_speed
            # 将过渡速度分段添加到速度分段序列中
            speed_maps.append(tran_speed_map)

        # 添加当前分段到速度分段序列中
        speed_maps.append(speed_map)

    # 返回计算出来的速度分段序列
    return speed_maps


def check_calc_run_speed_maps(run_speed_maps):
    # 循环每一个分段
    for i, speed_map in enumerate(run_speed_maps):
        if i == 0:
            continue
        if i + 1 >= len(run_speed_maps):
            continue
        prev_speed_map = run_speed_maps[i - 1]
        next_speed_map = run_speed_maps[i + 1]

        if isinstance(speed_map["au"], str):
            speed_map["au"] = (next_speed_map["au"] + prev_speed_map["au"]) / 2
    return run_speed_maps


def smooth_speed_transition(run_speed_maps, transition_secs=1):
    """
    通过逐步调整速度在给定的过渡时间内实现运行速度地图中速度的圆滑过渡。
    参数：
        run_speed_maps: 运行速度分段的列表，每一个速度分段是一个字典，包含两个键值对{"au": au, "secs": seconds}，
                        其中au是以天文单位（AU）表示的距离，seconds则是以秒为单位的时间。
        transition_secs: 运行速度过渡的时间（秒数），默认为1秒。
    """
    from scipy.interpolate import InterpolatedUnivariateSpline

    # 初始化速度分段序列
    speed_maps = []

    xs = np.array([p["au"] for p in run_speed_maps])
    ys = np.array([p["secs"] for p in run_speed_maps])
    # x = 2
    # y = spl(x)

    # 计算 dydx（即导数）
    # dydx = np.diff(ys) / np.diff(xs)
    # spl = CubicSpline(xs, ys)
    spl = InterpolatedUnivariateSpline(xs, ys, k=1)  # k=5)

    # 循环每一个分段
    for i, speed_map in enumerate(run_speed_maps):
        if i == 0:
            # 对于第一个分段，直接添加到速度分段序列中
            speed_maps.append(speed_map)
            continue
        if speed_map["secs"] <= 1:
            # 如果当前分段所用时间小于等于1秒，直接添加到速度分段序列中
            speed_maps.append(speed_map)
            continue
        if i + 1 >= len(run_speed_maps):
            speed_maps.append(speed_map)
            continue
        # 否则，保存前一个速度分段
        prev_speed_map = run_speed_maps[i - 1]
        next_speed_map = run_speed_maps[i + 1]
        current_speed_map = speed_map

        diff_au = current_speed_map["au"] - prev_speed_map["au"]

        distance_step = 0.01

        for j in range(int(diff_au / distance_step)):
            d = prev_speed_map["au"] + (distance_step * (j + 1))
            s = spl(d)
            s = np.clip(s, 1, 1800)
            speed_maps.append({"au": d, "secs": float(s)})

        speed_maps.append(speed_map)
        diff_au = next_speed_map["au"] - current_speed_map["au"]
        # distance_step = diff_au / 10

        for j in range(int(diff_au / distance_step)):
            d = current_speed_map["au"] + (distance_step * (j + 1))
            s = spl(d)
            s = np.clip(s, 1, 1800)
            speed_maps.append({"au": d, "secs": float(s)})

    # 返回计算出来的速度分段序列
    return speed_maps


def smooth_speed_transition3(run_speed_maps):
    # 初始化速度分段序列
    speed_maps = []

    # 循环每一个分段
    for i, speed_map in enumerate(run_speed_maps):
        if i == 0:
            # 对于第一个分段，直接添加到速度分段序列中
            speed_maps.append(speed_map)
            continue
        if speed_map["secs"] <= 1:
            # 如果当前分段所用时间小于等于1秒，直接添加到速度分段序列中
            speed_maps.append(speed_map)
            continue
        if i + 1 >= len(run_speed_maps):
            speed_maps.append(speed_map)
            continue

        # 否则，保存前一个速度分段
        prev_speed_map = run_speed_maps[i - 1]
        next_speed_map = run_speed_maps[i + 1]
        current_speed_map = speed_map

        speed_maps.append(speed_map)

    return speed_maps


def speed_smooth_adjust_test():
    # 运行速度配置
    run_speed_maps = [
        {"au": 0., "secs": 1},
        {"au": 0.008, "secs": 1},
        {"au": "?", "secs": SECONDS_PER_MINUTE * 10},
        {"au": 0.3855, "secs": 1},
        {"au": 0.386, "secs": 1},  # [00:03:12] 到达 [水星] 0.384 AU
        {"au": "?", "secs": SECONDS_PER_MINUTE * 10},
        {"au": 0.719, "secs": 1},
        # {"au": 0.723, "secs": 1},  # [00:06:00] 到达 [金星] 0.721 AU
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 10},
        # {"au": 0.99, "secs": 1},
        # {"au": 1.002, "secs": 1},  # [00:08:19] 到达 [地球] 1.0 AU
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 10},
        # {"au": 1.51, "secs": 1},
        # {"au": 1.522, "secs": 1},  # [00:12:39] 到达 [火星] 1.52 AU
        # # {"au": 5.1, "secs": SECONDS_PER_HOUR},
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 20},
        # {"au": 5.189, "secs": 1},
        # {"au": 5.192, "secs": 1},  # [00:43:10] 到达 [木星] 5.19 AU
        # # {"au": 9.44, "secs": SECONDS_PER_HOUR},
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 20},
        # {"au": 9.492, "secs": 1},
        # {"au": 9.502, "secs": 1},  # [01:19:01] 到达 [土星] 9.5 AU
        # # {"au": 19.15, "secs": SECONDS_PER_HOUR},
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 30},
        # {"au": 19.192, "secs": 1},
        # {"au": 19.202, "secs": 1},  # [02:39:41] 到达 [天王星] 19.2 AU
        # # {"au": 30.67, "secs": SECONDS_PER_HOUR},
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 30},
        # {"au": 30.692, "secs": 1},
        # {"au": 30.702, "secs": 1},  # [04:15:19] 到达 [海王星] 30.7 AU
        # # {"au": 39.52, "secs": SECONDS_PER_HOUR * 1.2},
        # {"au": "?", "secs": SECONDS_PER_MINUTE * 30},
        # {"au": 39.54, "secs": 1},
        # {"au": 40, "secs": 1}  # [05:28:55] 到达 [冥王星] 39.55 AU
    ]

    run_speed_maps = check_calc_run_speed_maps(run_speed_maps)

    data1 = [(m["au"], m["secs"]) for m in run_speed_maps]
    x1, y1 = zip(*data1)
    import copy
    run_speed_maps2 = smooth_speed_transition(run_speed_maps)

    data2 = [(m["au"], m["secs"]) for m in run_speed_maps2]
    x2, y2 = zip(*data2)

    # print(run_speed_maps2)
    # 导入包
    import matplotlib.pyplot as plt
    # 生成一个Figure画布和一个Axes坐标系
    fig, ax = plt.subplots()
    # 在生成的坐标系下画折线图
    ax.plot(x1, y1, 'o', linewidth=1)
    ax.plot(x2, y2, 'r', linewidth=1)
    # 显示图形
    plt.show()


if __name__ == '__main__':
    # from bodies import Sun, Earth
    #
    # """
    # 太阳、地球
    # """
    # bodies = [
    #     Sun(size_scale=1.2e2),  # 太阳放大 120 倍
    #     Earth(size_scale=4e3, distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    # ]
    # # mpl_run(bodies, SECONDS_PER_WEEK)
    # ursina_run(bodies, SECONDS_PER_WEEK)
    speed_smooth_adjust_test()
