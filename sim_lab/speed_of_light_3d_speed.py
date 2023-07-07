# -*- coding:utf-8 -*-
# title           :在太阳系中以光速运行（裸眼3D）
# description     :在太阳系中以光速运行（裸眼3D）
# author          :Python超人
# date            :2023-07-02
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import sys
import time
from common.func import wait_for, calculate_acceleration
from common.consts import AU
from sim_scenes.func import ursina_run, create_solar_system_bodies, create_light_ship, create_3d_card
from common.consts import LIGHT_SPEED
from sim_scenes.science.speed_of_light_init import SpeedOfLightInit

# TODO: 三种不同的摄像机视角
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import get_value_direction_vectors
from simulators.ursina.ursina_event import UrsinaEvent

camera_follow_light = None
camera_follow_light = 'ForwardView'  # 摄像机跟随光，方向是向前看

# 实例化一个初始化对象（订阅事件，记录到达每个行星所需要的时间）
init = SpeedOfLightInit(camera_follow_light)

# TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
# 创建太阳系天体（忽略质量，引力无效，初速度全部为0）
bodies = create_solar_system_bodies(ignore_mass=True, init_velocity=[0, 0, 0])

earth = bodies[3]
earth.rotate_angle = -23.44
jupiter, saturn, uranus, neptune = bodies[6:10]

for big_body in [jupiter, saturn, uranus, neptune]:
    big_body.init_position[0] = big_body.radius * big_body.size_scale

distance_scales = [1, 2.0, 1.5, 1.48, 1.65, 1.5, 0.82, 0.75, 0.50, 0.40, 0.33]

for idx, body in enumerate(bodies):
    body.distance_scale = distance_scales[idx]
    # if idx > 0:
    #     body.init_position[0] = body.diameter * body.size_scale
    #     body.init_position[1] = -body.radius * body.size_scale / 10
    body.rotation_speed *= 150

# if len(sys.argv) > 1:
#     camera_pos = sys.argv[1].replace("_", "")
# else:
#     camera_pos = "left"
camera_pos = "right"

print("camera_pos:", camera_pos)
camera_l2r = 0.002 * AU

if camera_pos == "right":  # 摄像机右眼
    init.light_init_position[0] += camera_l2r
elif camera_pos == "left":  # 摄像机左眼
    init.light_init_position[0] -= camera_l2r

init.light_init_position[0] = 5000000
init.light_init_position[1] = 150000
# init.auto_control_speed = True
init.camera_position = (0, -AU / 100, -AU / 50)

# 从 init 对象中获取 光体的大小（light_size_scale），光体的位置（light_init_position）
# 创建一个以光速前进的天体（模拟一个光子） speed=1光速=299792.458千米/秒，注意：质量为0才能达到光速，虽然如此，但也可以试试超光速
light_ship = create_light_ship(init.light_size_scale, init.light_init_position, speed=LIGHT_SPEED * 1)
light_ship.camera_pos = camera_pos
# 增加光速天体到天体集合
bodies.append(light_ship)


def switch_position():
    if light_ship.camera_pos == "right":  # 摄像机右眼
        light_ship.position[0] -= 2 * camera_l2r
        light_ship.camera_pos = "left"
    elif light_ship.camera_pos == "left":  # 摄像机左眼
        light_ship.position[0] += 2 * camera_l2r
        light_ship.camera_pos = "right"


light_ship.switch_position = switch_position

# 运行前指定bodies、light_body并订阅事件
init.light_ship = light_ship
init.bodies = bodies
init.event_subscription()

UrsinaEvent.on_reset_unsubscription(init.on_reset)


def on_reset():
    init.on_reset()
    init.arrived_info = "距离[太阳中心]：${distance}\n\n"
    init.arrived_info = "距离[太阳中心]：${distance}\n\n光速飞船速度：${speed}\n\n"


def get_acc_control_info():
    acc_control_info = [(0, 0.42, 10000),
                        (0.42, 0.70, -21000),  # 水星 0.76
                        (0.70, 0.85, 10000),
                        (0.85, 1.05, -21000),  # 金星 1.08
                        (1.05, 1.18, 10000),
                        (1.18, 1.6, -18000),  # 地球 1.48 # 月球 1.65
                        (1.6, 2.0, 10000),
                        (2.0, 2.25, -25000),  # 火星 2.28
                        (2.25, 3.3, 19000),
                        (3.3, 4.1, -35000),  # 木星 4.2
                        (4.1, 5.8, 15000),
                        (5.8, 6.9, -35000),  # 土星 7.14
                        (6.9, 8.2, 20000),
                        (8.3, 9.2, -35000),  # 天王星 9.6
                        (9.3, 10.8, 20000),
                        (10.8, 12, -35000),  # 海王星 12.3
                        (12, 12.5, 10000),
                        (12.5, 16, -35000),  # 冥王星 13
                        ]

    # [00:06:31] 到达 [水星] 0.7736 AU
    # [00:10:35] 到达 [金星] 1.0845 AU
    # [00:16:23] 到达 [地球] 1.4816 AU
    # [00:19:15] 到达 [月球] 1.6587 AU
    # [00:24:19] 到达 [火星] 2.2803 AU
    # [00:36:23] 到达 [木星] 4.2629 AU
    # [00:56:11] 到达 [土星] 7.1386 AU
    # [01:11:11] 到达 [天王星] 9.6171 AU
    # [01:31:11] 到达 [海王星] 12.2898 AU
    # [01:40:23] 到达 [冥王星] 13.0516 AU
    distance_list = [0.7736, 1.0845, 1.4816, 1.6587, 2.2803, 4.2629, 7.1386, 9.6171, 12.2898, 13.0516]
    distance_list = [0.7036, 1.0045, 1.4016, 1.6087, 2.2403, 4.0029,  # 木星
                     6.9086, 9.4171, 12.2098, 12.9516]
    acc_list = [(30000, -66000),  # 水星
                (28000, -65000),  # 金星
                (28000, -65000),  # 地球
                (0, 0),  # 月球
                (45000, -160000),  # 火星
                (32000, -60000),  # 木星
                (80000, -50000),  # 土星
                (50000, -50000),  # 天王星
                (50000, -40000),  # 海王星
                (100000, -206000)  # 冥王星
                ]
    acc_control_info.clear()
    last_d = 0
    for i, d in enumerate(distance_list):
        d2 = (d - last_d) * (2 / 3) + last_d
        acc_control_info.append((last_d, d2, acc_list[i][0]))
        acc_control_info.append((d2, d, acc_list[i][1]))
        last_d = d
    # calculate_acceleration(velocity , d, 5)
    return acc_control_info


def on_ready():
    init._3d_card = create_3d_card()
    init.light_ship.acc_control_info = get_acc_control_info()


def on_timer_changed(time_data: TimeData):
    init.text_panel.parent.enabled = True
    velocity, _ = get_value_direction_vectors(light_ship.velocity)
    distance = round(init.light_ship.position[2] / AU, 4)
    text = init.arrived_info.replace("${distance}", "%.4f AU" % distance)
    init.text_panel.text = text.replace("${speed}", str(round(velocity / LIGHT_SPEED, 1)) + "倍光速")

    if distance > 13.2:
        exit(0)

    MAX_SPEED = LIGHT_SPEED * 10
    MIN_SPEED = LIGHT_SPEED
    acc_val = 0
    for acc_vals in init.light_ship.acc_control_info:
        if acc_vals[0] < distance < acc_vals[1]:
            acc_val = acc_vals[2]
            break

    if acc_val > 0:
        if velocity > MAX_SPEED:
            acc_val = 0
    elif acc_val < 0:
        if velocity < MIN_SPEED:
            acc_val = 0

    light_ship.acceleration[2] = acc_val

    # if time_data.total_minutes < 2:
    #     light_ship.acceleration[2] = 5000
    # elif 2 < time_data.total_minutes < 100:
    #     light_ship.acceleration[2] = -5000
    # else:
    #     light_ship.acceleration[2] = 0
    # if time_data.total_seconds > 20:
    #     wait_for(0.03)


def on_before_evolving(evolve_args):
    init._3d_card.switch_color()
    light_ship.switch_position()
    if init._3d_card.switch_flag == 1:
        evolve_args["evolve_dt"] = 0.0


# 订阅重新开始事件
# 按键盘的 “O” 重置键会触发 on_reset
UrsinaEvent.on_reset_subscription(on_reset)

UrsinaEvent.on_ready_subscription(on_ready)
# 订阅计时器事件（记录已到达天体列表）
# 运行中，每时每刻都会触发 on_timer_changed
UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

UrsinaEvent.on_before_evolving_subscription(on_before_evolving)


def body_arrived(body):
    # # 到达每个行星都会触发，对光速飞船进行加速，超光速前进（使用未来曲率引擎技术）
    if body.name == "金星":  # 到达金星，木星开始调整位置
        jupiter.acceleration[0] = -500
        jupiter.acceleration[1] = -205
    elif body.name == "火星":  # 到达火星，土星开始调整位置
        saturn.acceleration[0] = -500
        saturn.acceleration[1] = -205
    elif body.name == "木星":  # 到达木星，天王星开始调整位置
        uranus.acceleration[0] = -150
        uranus.acceleration[1] = -105
    elif body.name == "土星":  # 到达土星，海王星开始调整位置
        neptune.acceleration[0] = -150
        neptune.acceleration[1] = -105
        # saturn, uranus, neptune
    # elif body.name == "土星":  # 到达土星，加速前进，并进行攀升
    #     light_ship.acceleration = [-150, 100, 0]
    # elif body.name == "天王星":  # 到达天王星，加速前进，并进行下降
    #     light_ship.acceleration = [0, 200, 0]
    # elif body.name == "海王星":  # 到达海王星，加速前进，并进行攀升
    #     light_ship.acceleration = [150, -550, -2500]

    elif body.name == "冥王星":
        # time.sleep(2)
        # exit(0)
        pass
    # print(body)


# def body_arrived(body):
#     # 到达每个行星都会触发，对光速飞船进行加速，超光速前进（使用未来曲率引擎技术）
#     if body.name == "火星":  # 到达火星，加速前进，并进行攀升
#         light_ship.acceleration = [0, 35000, 300000]
#     elif body.name == "木星":  # 到达木星，加速前进，并进行下降
#         light_ship.acceleration = [0, -100000, 200000]
#     elif body.name == "土星":  # 到达土星，加速前进，并进行攀升
#         light_ship.acceleration = [0, 55000, 200000]
#     elif body.name == "天王星":  # 到达天王星，加速前进，并进行下降
#         light_ship.acceleration = [0, -50000, 200000]
#     elif body.name == "海王星":  # 到达海王星，加速前进，并进行攀升
#         light_ship.acceleration = [-3, 48000, 300000]


init.body_arrived = body_arrived

# 使用 ursina 查看的运行效果
# 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
# position = 左-右+、上+下-、前+后-
ursina_run(bodies, 30,
           position=init.camera_position,
           # show_trail=init.show_trail,
           show_timer=True,
           show_camera_info=False,
           show_control_info=False,
           timer_enabled=True,
           view_closely=init.view_closely,
           # bg_music="sounds/interstellar.mp3"
           )
