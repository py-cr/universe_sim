# -*- coding:utf-8 -*-
# title           :抛物线模拟
# description     :抛物线模拟
# author          :Python超人
# date            :2023-04-09
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from objs import Football
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_MINUTE
from sim_scenes.func import ursina_run, get_vector2d_velocity, camera_look_at, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent


def create_ejected_object(velocity, raduis, trail_color, gravity_only_for, angle=10):
    """
    创建一个被抛的物体
    @param velocity: 抛出去的速度
    @param raduis: 物体地球中心的半径
    @param trail_color: 轨迹颜色
    @param angle: 抛出去的角度（地平线夹角，默认为10）
    @return:
    """
    # 根据速度、角度获取矢量速度（vx、vy） -> vx² + vy² = velocity²
    vx, vy = get_vector2d_velocity(velocity, angle=angle)
    football = Football(name=f'物体速度:{velocity}', mass=500, size_scale=1e3, trail_color=trail_color,
                        init_position=[0, raduis, 0],
                        init_velocity=[vx, vy, 0], gravity_only_for=[gravity_only_for])  # 仅适用于地球的重力，物体之间重力不要受到影响
    return football


if __name__ == '__main__':
    """
    抛物线模拟
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                  size_scale=1, rotation_speed=0, texture="earth_hd.jpg")
    raduis = earth.raduis + 300
    # TODO: 4个不同的抛出速度  7.5km/s、8.5km/s、10km/s、11.2km/s（第二宇宙速度）
    # 粉色：velocity = 7.5，飞不出地球太远，就落地
    obj0 = create_ejected_object(velocity=7.5, raduis=raduis, trail_color=(255, 0, 255), gravity_only_for=earth)
    # 红色：velocity = 8.5，飞不出地球太远，就落地
    obj1 = create_ejected_object(velocity=8.5, raduis=raduis, trail_color=(255, 0, 0), gravity_only_for=earth)
    # 绿色：velocity = 10，能飞出地球很远，但还是无法摆脱地球引力
    obj2 = create_ejected_object(velocity=10, raduis=raduis, trail_color=(0, 255, 0), gravity_only_for=earth)
    # 蓝色：velocity = 11.2，脱离地球引力直接飞出。速度11.2千米/秒为脱离地球引力的速度叫第二宇宙速度
    obj3 = create_ejected_object(velocity=11.2, raduis=raduis, trail_color=(0, 0, 255), gravity_only_for=earth)

    bodies = [earth, obj0, obj1, obj2, obj3]


    def on_timer_changed(time_data: TimeData):
        """
        定时触发，在10分钟后，进行碰撞判断，如果抛出物与地球相碰撞了，则抛出物体静止不动
        @param time_data:
        @return:
        """
        if time_data.total_minutes > 10:
            # 抛出物体10分钟后，再进行碰撞判断
            for obj in [obj0, obj1, obj2, obj3]:
                # 循环判断每个抛出物与地球是否相碰撞
                if two_bodies_colliding(obj, earth):
                    # 如果抛出物与地球相碰撞了，则静止不动（抛出物停止并忽略引力）
                    obj.stop_and_ignore_gravity()


    def on_reset():
        for obj in [obj0, obj1, obj2, obj3]:
            obj.ignore_mass = False


    # 订阅计时器事件（定时触发）
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    UrsinaEvent.on_reset_subscription(on_reset)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,  # 一秒相当于半个小时
               position=(0, 0, -45000),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
