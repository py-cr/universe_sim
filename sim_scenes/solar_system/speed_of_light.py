# -*- coding:utf-8 -*-
# title           :太阳系场景模拟1
# description     :太阳系场景模拟（展示的效果为太阳系真实的距离）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Asteroids, Body
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import Text, Panel, color, camera, Vec3


def create_bodies():
    """
    创建太阳系天体（忽略质量，引力无效，初速度全部为0）
    太阳、小行星环、
    八大行星：木星(♃)、土星(♄)、天王星(♅)、海王星(♆)、地球(⊕)、金星(♀)、火星(♂)、水星(☿)
    冥王星
    以下展示的效果为太阳系真实的距离
    @return:
    """
    sun = Sun(name="太阳", size_scale=0.6e2)  # 太阳放大 60 倍，距离保持不变
    bodies = [
        sun,
        Mercury(name="水星", size_scale=2e3),  # 水星放大 2000 倍，距离保持不变
        Venus(name="金星", size_scale=2e3),  # 金星放大 2000 倍，距离保持不变
        Earth(name="地球", size_scale=2e3),  # 地球放大 2000 倍，距离保持不变
        Mars(name="火星", size_scale=2e3),  # 火星放大 2000 倍，距离保持不变
        # Asteroids(name="小行星群", size_scale=3.2e2,
        #           parent=sun),  # 小行星群模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=0.6e3),  # 木星放大 600 倍，距离保持不变
        Saturn(name="土星", size_scale=0.6e3),  # 土星放大 600 倍，距离保持不变
        Uranus(name="天王星", size_scale=0.7e3),  # 天王星放大 700 倍，距离保持不变
        Neptune(name="海王星", size_scale=1e3),  # 海王星放大 1000 倍，距离保持不变
        Pluto(name="冥王星", size_scale=10e3),  # 冥王星放大 10000 倍，距离保持不变(从太阳系的行星中排除)
    ]

    # 遍历所有天体，
    for idx, body in enumerate(bodies):
        body.set_ignore_mass(True)  # 忽略质量（引力无效）
        body.init_velocity = [0, 0, 0]  # 初速度为0
    return bodies


def create_light(size_scale=1e4):
    """
    用天体模拟一个光子
    @return:
    """
    return Body(name='光速', mass=0, size_scale=size_scale, color=(255, 255, 0),
                # init_position=[AU / 3, 0, 0],
                init_position=[AU / 12, 0, 0],
                init_velocity=[0, 0, 299792.458]).set_light_disable(True)  # 1光速=299792.458 千米/秒(km/秒)


def create_text_panel(width=0.35, height=.5):
    # 创建一个 Panel 组件
    panel = Panel(
        parent=None,
        model='quad',
        # texture='white_cube',
        color=color.gray,
        origin=(-.48, .48),
        scale=(width, height),
        position=(-.88, 0.3, 0),
        alpha=0.2
    )

    # 创建一个 Text 组件用于显示消息
    text = Text(
        parent=panel,
        text='',
        origin=(-.5, .5),
        scale=(height * 5, width * 5),
        font=UrsinaConfig.CN_FONT,
        # background=True,
        # background_color=color.clear
    )
    return text


# 已到达天体列表
arrived_bodies = []
text_panel = None
arrived_info = ""

CAMERA_FOLLOW_LIGHT = None  # 不跟随光
CAMERA_FOLLOW_LIGHT = 'ForwardView'  # 向前看
# CAMERA_FOLLOW_LIGHT = 'SideView'  # 侧面看


def on_reset():
    global arrived_info
    arrived_bodies.clear()
    arrived_info = ""
    if text_panel is not None:
        text_panel.text = ""


def on_ready():
    global text_panel
    text_panel = create_text_panel()

    if CAMERA_FOLLOW_LIGHT == "SideView":
        camera.parent = light_body.planet
        camera.rotation_y = -85
    elif CAMERA_FOLLOW_LIGHT == "ForwardView":
        camera.parent = light_body.planet
        light_body.planet.enabled = False
        camera.rotation_y = -15


def on_timer_changed(time_text, time_data):
    global arrived_info
    years, days, hours, minutes, seconds = time_data
    for body in bodies:
        if body is light_body or isinstance(body, Sun) \
                or body in arrived_bodies or isinstance(body, Asteroids):
            # 对于光速天体、太阳、小行星群、“已到达天体列表”中的天体无需计算
            continue
        # 计算判断，如果光速天体距离到达了某个天体，就记录到“已到达天体列表”中
        if light_body.position[2] >= body.position[2]:
            arrived_bodies.append(body)
            if text_panel is not None:
                arrived_info += f"[{time_text}]\t到达\t[{body.name}]\n\n"
                text_panel.text = arrived_info
                print(f"[{time_text}] 到达 [{body.name}]")


# 订阅计时器事件（记录已到达天体列表）
UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
# 订阅重新开始事件
UrsinaEvent.on_reset_subscription(on_reset)

UrsinaEvent.on_ready_subscription(on_ready)

if CAMERA_FOLLOW_LIGHT == "SideView":
    position = (2 * AU, 0, -AU / 8)
    show_trail = True
    light_size_scale = 1e3
elif CAMERA_FOLLOW_LIGHT == "ForwardView":
    position = (0, AU / 10, -AU)
    show_trail = False
    light_size_scale = 1e2
else:
    position = (0, 2 * AU, -11 * AU)
    show_trail = True
    light_size_scale = 5e3

# 创建太阳系天体（忽略质量，引力无效，初速度全部为0）
bodies = create_bodies()
# 创建一个以光速前进的天体（模拟一个光子，质量为0才能达到光速）
light_body = create_light(size_scale=light_size_scale)

bodies.append(light_body)

# 使用 ursina 查看的运行效果
# 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
# position = 左-右+、上+下-、前+后-
ursina_run(bodies, 60,
           position=position,
           show_trail=show_trail, show_timer=True,
           # view_closely=True,
           bg_music="sounds/interstellar.mp3")
