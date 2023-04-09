# -*- coding:utf-8 -*-
# title           :抛物线模拟
# description     :抛物线模拟
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_MINUTE
from sim_scenes.func import ursina_run, get_vector2d_velocity


def create_ejected_object(velocity, raduis, trail_color, angle=10):
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
    moon = Moon(name=f'物体速度:{velocity}', mass=500, size_scale=2e6, trail_color=trail_color,
                init_position=[0, raduis, 0],
                init_velocity=[vx, vy, 0], gravity_only_for_earth=True)  # 仅适用于地球的重力，物体之间重力不要受到影响
    return moon


if __name__ == '__main__':
    """
    抛物线模拟
    """
    # 地球在中心位置
    e = Earth(init_position=[0, 0, 0], size_scale=1, texture="earth_hd.jpg", init_velocity=[0, 0, 0])
    raduis = e.raduis + 300
    # 红色：velocity = 8  # 物体飞不出地球太远，就落地
    obj1 = create_ejected_object(velocity=8, raduis=raduis, trail_color=(255, 0, 0))
    # 绿色：velocity = 10  # 物体能飞出地球很远，但还是无法摆脱地球引力
    obj2 = create_ejected_object(velocity=10, raduis=raduis, trail_color=(0, 255, 0))
    # 蓝色：velocity = 11.2  # 脱离地球引力直接飞出。速度11.2千米/秒为脱离地球引力的速度叫第二宇宙速度
    obj3 = create_ejected_object(velocity=11.2, raduis=raduis, trail_color=(0, 0, 255))

    bodies = [e, obj1, obj2, obj3]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,  # 一秒相当于半个小时
               position=(0, 0, -45000),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
