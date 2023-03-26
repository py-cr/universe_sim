# -*- coding:utf-8 -*-
# title           :上帝之眼
# description     :上帝之眼
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


def show_eye_of_god():
    """
    上帝之眼
    """
    D = 600
    mass = 0.9e25
    # camera_pos = 左-右+、上+下-、前+后-
    camera_pos = (-100 * D, 0, -5000 * D)

    def get_position(pos, scale):
        # [ 远+近-  , 左+右-  , 上+下-]
        return pos[0] + (scale - 1.0) * 300 * (random.randint(90, 110)) * D, pos[1], pos[2]
        # return pos[0], pos[1], pos[2]

    bodies: list = gen_eye_bodies(
        {"D": D, "Body": Body, "mass": mass, "get_position": get_position, "camera_pos": camera_pos})
    face = FixedStar(name="face", texture="fixed_star.png", mass=mass * 3000, color=(0xff, 0xf8, 0xd4),
                     init_position=[2000 * D, 200 * D, 100 * D],  # [ 远+近-  , 左+右-  , 上+下-]
                     ignore_mass=True)
    face.light_on = False
    bodies.append(face)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_WEEK * 2, position=camera_pos)


def gen_eye_bodies(params):
    """
    根据像素图片以及参数，自动生成星球，注意图片像素不能太多，否则会导致电脑运行太慢
    @param params:
    @return:
    """
    from PIL import Image

    img = Image.open("./images/eye.png").convert('RGBA')
    width, height = img.size
    interval_factor = 20  # 星球间距因子
    body_template = 'Body(name="%s", mass=mass, color=(%d, %d, %d), size_scale=%.4f, ' \
                    'init_position=get_position([0, %g * D, %g * D], %.4f), init_velocity=[0, 0, 0], ignore_mass=True)'
    bodies_str = "["

    # 以图片像素为坐标，对角线的距离
    distance_hw = pow(pow(width, 2) + pow(height, 2), 1 / 2)

    for h in range(0, height):
        # row = []
        for w in range(0, width):
            # 以图片像素为坐标，每个像素点到中心的距离
            distance_to_center = pow(pow(w - width / 2, 2) + pow(h - height / 2, 2), 1 / 2)
            # 让 body 从中心开始，离摄像机越远， body 的缩放值越大（scale 就越大，）
            scale = (distance_to_center / (distance_hw * 10) + 1)  # 中心最近 1.0 ~ 1.05
            # TODO: 队列反向排列（中心最远 1.05 ~ 1.0）
            # scale = 1.05 - scale + 1.0
            # print(scale)
            # 获取像素的颜色
            pixel = img.getpixel((w, h))
            # 对于纯白色的颜色，就忽略，不生成星球（这样像素中纯白色越多，对电脑的压力就越少）
            if pixel[0] >= 255 and pixel[1] >= 255 and pixel[1] >= 255:
                continue
            body_str = body_template % (f"星球{h}:{w}", pixel[0], pixel[1], pixel[2], scale,
                                        (width-w) * interval_factor, (height-h) * interval_factor, scale)
            bodies_str += body_str + ",\n"

    bodies_str += "]"
    return eval(bodies_str, params)


if __name__ == '__main__':
    show_eye_of_god()
