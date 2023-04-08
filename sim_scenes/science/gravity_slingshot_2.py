# -*- coding:utf-8 -*-
# title           :模拟流浪地球通过木星、土星加速
# description     :模拟流浪地球通过木星、土星加速
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Jupiter, Saturn
from common.consts import SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import  ursina_run
from bodies.body import AU

if __name__ == '__main__':
    """
    模拟流浪地球通过木星、土星加速
    """
    # params 为不同参数量的加速效果，j_pos为木星位置；s_pos为土星位置；e_vel为地球初始速度
    # 地球初始速度≈36km/s，通过木星加速到 42.43km/s(加速度为0时的速度)，再通过土星加速到 108.64km/s(加速度为0时的速度)
    params = {"j_pos": [-AU / 4, 0, 0], "s_pos": [-0.9 * AU + 7.5e6, 0, AU / 1.5], "e_vel": [-36, 0, -0.2]}

    # 地球初始速度≈38km/s，通过木星加速到 51.96km/s(加速度为0时的速度)，再通过土星加速到 71.27km/s(加速度为0时的速度)
    params = {"j_pos": [-AU / 4, 0, 0], "s_pos": [-1.3 * AU + 1.09e7, 0, AU / 1.5], "e_vel": [-38, 0, -0.2]}

    bodies = [
        Jupiter(size_scale=1e2, init_position=params["j_pos"], init_velocity=[0, 0, 0]),  # 木星放大 100 倍
        Saturn(size_scale=1e2, init_position=params["s_pos"], init_velocity=[0, 0, 0]),  # 土星放大 100 倍
        Earth(size_scale=3e2, init_position=[0, 0, 0], init_velocity=params["e_vel"]),  # 地球放大 300 倍
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK, position=(-8e7, AU / 5, -1.5 * AU), show_trail=True, view_closely=True)
