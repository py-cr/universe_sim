# -*- coding:utf-8 -*-
# title           :组成文本的星球群（自定义星球）
# description     :组成文本的星球群（自定义星球）
# author          :Python超人
# date            :2023-03-26
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Moon, FixedStar, Body
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_HALF_DAY, SECONDS_PER_DAY, SECONDS_PER_WEEK
from sim_scenes.func import mayavi_run, ursina_run
from bodies.body import AU
import random
from sim_scenes.interest.utils.body_utils import gen_eye_bodies


def show_text_bodies():
    """
    显示文本的星球群
    """
    D = 600
    mass = 0.5e25
    # camera_pos = 左-右+、上+下-、前+后-
    camera_pos = (-100 * D, 0, -5000 * D)

    def get_position(pos, scale):
        # [ 远+近-  , 左+右-  , 上+下-]
        return pos[0] + (scale - 1.0) * 200 * (random.randint(90, 110)) * D, pos[1], pos[2]
        # return pos[0], pos[1], pos[2]

    bodies: list = gen_eye_bodies(pixel_image="./images/python.png",
                                  params={"D": D, "Body": Body, "mass": mass,
                                          "get_position": get_position,
                                          "camera_pos": camera_pos})
    face = FixedStar(name="bg", texture="fixed_star.png", mass=mass * 9000, color=(0xff, 0xf8, 0xd4),
                     init_position=[2000 * D, 260 * D, 100 * D],  # [ 远+近-  , 左+右-  , 上+下-]
                     ignore_mass=True)
    face.light_on = False
    bodies.append(face)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK * 2, position=camera_pos)


if __name__ == '__main__':
    show_text_bodies()
