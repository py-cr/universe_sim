# -*- coding:utf-8 -*-
# title           :在太阳系中以光速运行
# description     :在太阳系中以光速运行
# author          :Python超人
# date            :2023-04-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Asteroids, Body
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import ursina_run, create_solar_system_bodies, create_text_panel, create_light
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera

# 已到达天体列表
arrived_bodies = []
text_panel = None
arrived_info = ""

CAMERA_FOLLOW_LIGHT = None  # 不跟随光
CAMERA_FOLLOW_LIGHT = 'ForwardView'  # 向前看
CAMERA_FOLLOW_LIGHT = 'SideView'  # 侧面看


def on_reset():
    global arrived_info
    arrived_bodies.clear()
    arrived_info = "[00:00:00] 从 [太阳] 出发\n\n"
    if text_panel is not None:
        text_panel.text = arrived_info


# 订阅重新开始事件
UrsinaEvent.on_reset_subscription(on_reset)


def on_ready():
    global text_panel
    text_panel = create_text_panel()
    text_panel.text = arrived_info

    if CAMERA_FOLLOW_LIGHT == "SideView":
        camera.parent = light_body.planet
        camera.rotation_y = -85
    elif CAMERA_FOLLOW_LIGHT == "ForwardView":
        light_body.planet.enabled = False
        camera.parent = light_body.planet
        camera.rotation_y = -15


UrsinaEvent.on_ready_subscription(on_ready)


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

if CAMERA_FOLLOW_LIGHT == "SideView":
    # 摄像机位置 = 前-后+、上+下-、左-右+、
    position = (AU, 0, 0)
    show_trail = True
    light_size_scale = 1e3
    light_init_position = [AU / 3, 0, 0]
elif CAMERA_FOLLOW_LIGHT == "ForwardView":
    # 摄像机位置 = 左-右+、上+下-、前+后-
    position = (0, AU / 10, -AU)
    show_trail = False
    light_size_scale = 1e2
    light_init_position = [AU / 12, 0, 0]
else:
    # 摄像机位置 = 左-右+、上+下-、前+后-
    position = (0, AU, -6 * AU)
    show_trail = True
    light_size_scale = 2e3
    light_init_position = [AU / 3, 0, 0]

# 创建太阳系天体（忽略质量，引力无效，初速度全部为0）
bodies = create_solar_system_bodies(ignore_mass=True, init_velocity=[0, 0, 0])
# 创建一个以光速前进的天体（模拟一个光子，质量为0才能达到光速）
light_body = create_light(light_size_scale, light_init_position)

bodies.append(light_body)

# 使用 ursina 查看的运行效果
# 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
# position = 左-右+、上+下-、前+后-
ursina_run(bodies, 60,
           position=position,
           show_trail=show_trail, show_timer=True,
           # view_closely=True,
           bg_music="sounds/interstellar.mp3")
