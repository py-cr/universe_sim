# -*- coding:utf-8 -*-
# title           :组成文本的星球群（自定义星球）
# description     :组成文本的星球群（自定义星球）
# author          :Python超人
# date            :2023-03-26
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon, FixedStar, ColorBody
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK
from sim_scenes.func import mayavi_run, ursina_run
from bodies.body import AU
import random
from sim_scenes.interest.utils.body_utils import gen_bodies_from_image


def show_text_bodies():
    """
    显示文本的星球群
    """
    D = 6000
    # camera_pos = 左-右+、上+下-、前+后-
    camera_pos = (-130 * D, 0, -6000 * D)

    bodies: list = gen_bodies_from_image(pixel_image="./images/python.png", texture="color_body.jpg",
                                         params={"camera_pos": camera_pos})
    bg = FixedStar(name="bg", texture="fixed_star.png", mass=5e31, color=(0xff, 0xf8, 0xd4),
                   init_position=[3000 * D, 260 * D, 100 * D],  # [ 远+近-  , 左+右-  , 上+下-]
                   ignore_mass=True)
    bg.light_on = True
    bodies.append(bg)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK * 2, position=camera_pos, view_closely=True)


if __name__ == '__main__':
    show_text_bodies()
