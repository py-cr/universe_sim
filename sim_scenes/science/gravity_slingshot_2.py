# -*- coding:utf-8 -*-
# title           :引力弹弓模拟演示
# description     :引力弹弓模拟演示
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Jupiter, Saturn
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import mayavi_run, ursina_run
from bodies.body import AU

if __name__ == '__main__':
    """
    模拟流浪地球经过木星、土星加速
    """
    bodies = [
        Jupiter(size_scale=1e2, init_position=[-AU / 4, 0, 0], init_velocity=[0, 0, 0]),  # 木星放大 100 倍
        Saturn(size_scale=1e2, init_position=[-1.5 * AU, 0, AU / 1.5], init_velocity=[0, 0, 0]),  # 土星放大 100 倍
        Earth(size_scale=3e2,  # 地球放大 300 倍
              init_position=[0, 0, 0],  #
              # init_velocity=[0, 33, -1],
              # init_velocity=[-1, 10, 0],  # 朝向木星的速度为 38km/s，-1 km/s 是为了防止地球正面对着木星冲去
              init_velocity=[-10, 0, -1],  # 朝向木星的速度为 38km/s，-1 km/s 是为了防止地球正面对着木星冲去
              # init_velocity=[0, 50, -1],
              ),
    ]

    # 使用 mayavi 查看的运行效果
    # mayavi_run(bodies, SECONDS_PER_WEEK, view_azimuth=-45)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_MONTH, position=(0, AU / 2, -2 * AU), show_trail=True, view_closely=True)
