# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Body, Sun, Earth, Moon
from objs import Obj, Satellite, Satellite2
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from bodies.body import AU


def get_lagrangian_points(m1, m2, r):
    """
    https://baike.baidu.com/item/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E7%82%B9/731078

    @param m1: 大质量
    @param m2: 小质量
    @param r: 半径
    @return:
    """
    a = m2 / (m1 + m2)
    l1 = (0, 0, r * (1 - pow(a / 3, 1 / 3)))
    l2 = (0, 0, r * (1 + pow(a / 3, 1 / 3)))
    l3 = (0, 0, -r * (1 + (5 * a) / 12))
    l4 = (pow(3, 1 / 2) / 2 * r, 0, (r / 2) * ((m1 - m2) / (m1 + m2)))
    l5 = (-pow(3, 1 / 2) / 2 * r, 0, (r / 2) * ((m1 - m2) / (m1 + m2)))

    return l1, l2, l3, l4, l5


def create_satellite(name, init_position, init_velocity):
    satellite = Satellite(name=name, mass=1.4e10, size_scale=3e3, color=(255, 200, 0),
                          init_position=init_position,
                          init_velocity=init_velocity, gravity_only_for=[earth, moon])
    return satellite


bodies = [
    Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
          init_velocity=[0, 0, 0], size_scale=0.5e1),  # 地球放大 5 倍，距离保持不变
    Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
         init_velocity=[-1.054152222, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
]
import math

earth = bodies[0]
moon = bodies[1]
# L1_p, L2_p, L3_p, L4_p, L5_p = get_lagrangian_points(earth.mass, moon.mass, 363104)
# point_z = L4_p[2] + 0  # 越大，离月球越近
# L4_vel = 1.048
# init_velocity = [-math.sin(math.pi * 30 / 180)*L4_vel, 0, math.cos(math.pi * 30 / 180)*L4_vel]

# point_z = L1_p[2] + 3301.48891  # 越大，离月球越近  3301.48891
# init_velocity = [-0.890136271716, 0, 0]  # -0.890136271716 画图比较好
# L1：point=[0,0,308536.70059015526]  velocity=[-0.890136271716, 0, 0]
satelliteL1 = create_satellite(name=f'卫星L1', init_position=[0, 0, 308536.672],
                               init_velocity=[-0.890136271716, 0, 0])
bodies.append(satelliteL1)

# point_z = L2_p[2] + 2365.72  # 越大，离月球越近
# init_velocity = [-1.24, 0, 0]
# L2：point=[0,0, 423338.5083198447]  velocity=[-1.24, 0, 0]
satelliteL2 = create_satellite(name=f'卫星L2', init_position=[0, 0, 423338.5083198447],
                               init_velocity=[-1.24, 0, 0])
bodies.append(satelliteL2)

# L3：point=[0,0, -364941.3043941873]  velocity=[1.039 , 0, 0]
satelliteL3 = create_satellite(name=f'卫星L3', init_position=[0, 0, -364941.3043941873],
                               init_velocity=[1.048, 0, 0])
bodies.append(satelliteL3)

L4_vel = 1.048
L4_init_velocity = [-math.sin(math.pi * 30 / 180) * L4_vel, 0, math.cos(math.pi * 30 / 180) * L4_vel]
# L4：point=[0,0, 177142.46945395062]  velocity=[1.039 , 0, 0]
satelliteL4 = create_satellite(name=f'卫星L4', init_position=[314457.2882157448, 0, 177142.46945395062],
                               init_velocity=L4_init_velocity)
bodies.append(satelliteL4)

L5_vel = 1.048
L5_init_velocity = [-math.sin(math.pi * 30 / 180) * L5_vel, 0, -math.cos(math.pi * 30 / 180) * L5_vel]
# L4：point=[0,0, 177142.46945395062]  velocity=[1.039 , 0, 0]
satelliteL5 = create_satellite(name=f'卫星L5', init_position=[-314457.2882157448, 0, 177142.46945395062],
                               init_velocity=L5_init_velocity)
bodies.append(satelliteL5)


def calc_simulator(target):
    from sim_scenes.func import calc_run
    from simulators.calc_simulator import CalcSimulator, CalcContext

    CalcSimulator.init(True)

    def on_ready(context: CalcContext):
        for body in bodies:
            body.reset()

    def evolve_next(context: CalcContext):
        return context.evolve_count < 1000

    def after_evolve(dt, context: CalcContext):
        # target: Body = context.bodies[1]  # 月球
        # target: Obj = context.bodies[2]  # 卫星
        context.init_param("init_vel", target.init_velocity[0])
        context.init_param("acc_values", []).append(target.acceleration_value())
        context.init_param("vel_values", []).append(target.velocity_value())
        print(target.name, target.acceleration_value(), target.velocity_value())

    def on_finished(context: CalcContext):
        import matplotlib.pyplot as plt
        # 解决中文显示问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        acc_values = context.params["acc_values"]
        vel_values = context.params["vel_values"]
        max_value = max(acc_values)
        min_value = min(acc_values)
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(111)
        ax1.plot(acc_values, 'blue', label='加速度')
        ax1.set_ylabel('加速度', fontdict={'weight': 'normal', 'size': 15, 'color': 'blue'})
        # ax1.set_title("加速度/速度", fontdict={'weight': 'normal', 'size': 15})
        plt.title("%s(%.4f) max:%.4f min:%.4f diff:%.4f" % (target.name,
                                                            context.get_param("init_vel"), max_value * 1e6,
                                                            min_value * 1e6, (max_value - min_value) * 1e6))
        l1 = ax1.legend(loc='lower left', labels=['加速度'])

        ax2 = ax1.twinx()  # this is the important function
        ax2.plot(vel_values, 'red', label='速度')
        ax2.set_ylabel('速度', fontdict={'weight': 'normal', 'size': 15, 'color': 'red'})
        ax2.set_xlabel('Same')

        l2 = ax2.legend(loc='upper right', labels=['速度'])
        plt.show()

    CalcSimulator.on_ready_subscription(on_ready)
    CalcSimulator.on_after_evolve_subscription(after_evolve)
    CalcSimulator.on_finished_subscription(on_finished)

    calc_run(bodies, SECONDS_PER_HOUR, evolve_next=evolve_next)


def ursina_simulator():
    from sim_scenes.func import ursina_run, camera_look_at
    from simulators.ursina.entities.body_timer import TimeData
    from simulators.ursina.entities.entity_utils import create_directional_light
    from simulators.ursina.ursina_event import UrsinaEvent
    from simulators.ursina.ursina_mesh import create_line

    def on_ready():
        # 运行前触发
        # 运行开始前，将摄像机指向地球

        # 摄像机看向地球
        camera_look_at(moon)

    def create_connecting_lines(satellites_list):
        lines = []
        for satellites in satellites_list:
            line = create_line(from_pos=satellites[0].planet.position, to_pos=satellites[1].planet.position, alpha=0.3)
            lines.append(line)
        return lines

    def on_timer_changed(time_data: TimeData):
        from ursina import destroy
        if hasattr(earth, "lines"):
            for line in earth.lines:
                destroy(line)

        earth.lines = create_connecting_lines([[satelliteL2, satelliteL3],
                                    [satelliteL4, satelliteL1], [satelliteL5, satelliteL1],
                                    [satelliteL4, satelliteL2], [satelliteL5, satelliteL2],
                                    [satelliteL4, satelliteL3], [satelliteL5, satelliteL3],
                                    ])

    # 订阅事件后，上面的函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR * 10,
               position=(-300000, 1500000, -100),
               show_timer=True,
               # show_trail=True
               )


if __name__ == '__main__':
    # calc_simulator(earth)
    # calc_simulator(moon)
    # calc_simulator(satellite)
    ursina_simulator()
