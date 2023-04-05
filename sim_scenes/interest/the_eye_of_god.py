# -*- coding:utf-8 -*-
# title           :组成上帝之眼的星球群（自定义星球）
# description     :组成上帝之眼的星球群（自定义星球）
# author          :Python超人
# date            :2023-03-26
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon, FixedStar, Body
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK
from sim_scenes.func import mayavi_run, ursina_run
from sim_scenes.interest.utils.body_utils import gen_bodies_from_image
import random


def show_eye_of_god():
    """
    上帝之眼
    """
    D = 6000  # 基本距离单位:km（随意赋值）
    # 观看摄像机的位置
    # camera_pos = (左-右+, 上+下-, 前+后-)
    camera_pos = (D, D, -7000 * D)

    bodies: list = gen_bodies_from_image(pixel_image="./images/eye.png",
                                         texture="color_body.jpg",
                                         params={"camera_pos": camera_pos})
    # 放一个恒星作为背景
    bg = FixedStar(name="背景恒星", texture="fixed_star.png", mass=2e32, color=(0xff, 0xf8, 0xd4),
                   init_position=[-400 * D, 100 * D, 6000 * D],  # [ 左-右+, 上+下-, 远+近- ]
                   ignore_mass=True)
    bodies.append(bg)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = camera_pos = (左-右+, 上+下-, 前+后-)
    ursina_run(bodies, SECONDS_PER_WEEK * 2, position=camera_pos, view_closely=True)


if __name__ == '__main__':
    show_eye_of_god()
