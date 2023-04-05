# -*- coding:utf-8 -*-
# title           :Body工具类
# description     :Body工具类
# author          :Python超人
# date            :2023-03-26
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import ColorBody
import random
import math
from PIL import Image


def get_scaled_body_pos(camera_pos, body_pos, scale_factor):
    # 计算天体和摄像机的距离
    dist = math.sqrt((camera_pos[0] - body_pos[0]) ** 2 +
                     (camera_pos[1] - body_pos[1]) ** 2 +
                     (camera_pos[2] - body_pos[2]) ** 2)
    # 缩放天体的大小
    scaled_dist = dist * scale_factor
    # 计算摄像机和天体的连线向量
    vector = [body_pos[0] - camera_pos[0], body_pos[1] - camera_pos[1], body_pos[2] - camera_pos[2]]
    # 计算单位向量
    unit_vector = [vector[0] / dist, vector[1] / dist, vector[2] / dist]
    # 根据缩放后的距离和单位向量计算天体的新位置
    new_pos = [camera_pos[0] + unit_vector[0] * scaled_dist, camera_pos[1] + unit_vector[1] * scaled_dist,
               camera_pos[2] + unit_vector[2] * scaled_dist]
    return new_pos


def gen_bodies_from_image(pixel_image, params, texture="color_body.png"):
    """
    根据像素图片以及参数，自动生成星球，注意图片像素不能太多，否则会导致电脑运行太慢
    @param pixel_image:
    @param params:
    @return:
    """
    D = 6000
    mass = 0.9e25

    camera_pos = params["camera_pos"]

    def get_position(pos, scale):
        # return get_scaled_body_pos((camera_pos[2], camera_pos[0], camera_pos[1]), pos, scale)
        # return get_scaled_body_pos((camera_pos[2], camera_pos[1], camera_pos[0]), pos, scale)
        return get_scaled_body_pos((camera_pos[0], camera_pos[1], camera_pos[2]), pos, scale)

        # # body.init_position = [body.raduis * SIZE_SCALE, (distance_sum + d), AU]
        # body.init_position = [-(distance_sum + d), AU, body.raduis * SIZE_SCALE]

        # # [ 远+近-  , 左+右-  , 上+下-]
        # return pos[0] + (scale - 1.0) * 300 * (random.randint(90, 110)) * D, pos[1], pos[2]
        # return pos[0], pos[1], pos[2]

    params["ColorBody"] = ColorBody
    params["get_position"] = get_position
    params["mass"] = mass
    params["D"] = D

    img = Image.open(pixel_image).convert('RGBA')
    width, height = img.size
    interval_factor = 20  # 星球间距因子
    body_template = 'ColorBody(name="%s", mass=mass, color=(%d, %d, %d), size_scale=%.4f, ' \
                    'init_position=get_position([-%g * D, %g * D, 0], %.4f), ' \
                    f'init_velocity=[0, 0, 0], ignore_mass=True, texture="{texture}").set_light_disable(True)'
    bodies_str = "["

    # 以图片像素为坐标，对角线的距离
    distance_hw = pow(pow(width, 2) + pow(height, 2), 1 / 2)

    for h in range(0, height):
        # row = []
        for w in range(0, width):
            # 以图片像素为坐标，每个像素点到中心的距离
            distance_to_center = pow(pow(w - width / 2, 2) + pow(h - height / 2, 2), 1 / 2)
            # 让 body 从中心开始，离摄像机越远， body 的缩放值越大（scale 就越大，）
            scale = (distance_to_center / (distance_hw * 1.2) + 1)  # 中心最近 1.0 ~ 1.25
            # scale = scale + (random.randint(100, 200) / 1000)
            # TODO: 队列反向排列（中心最远 1.05 ~ 1.0）
            # scale = 1.25 - scale + 1.0
            # print(scale)
            # 获取像素的颜色
            pixel = img.getpixel((w, h))
            # 对于纯白色的颜色，就忽略，不生成星球（这样图片中，纯白色越多，对电脑的压力就越小）
            if pixel[0] >= 220 and pixel[1] >= 220 and pixel[1] >= 220:
                continue
            body_str = body_template % (f"星球{w}:{h}", pixel[0], pixel[1], pixel[2], scale * 10,
                                        (width - w) * interval_factor, (height - h) * interval_factor, scale)
            bodies_str += body_str + ",\n"

    bodies_str += "]"
    return eval(bodies_str, params)


def get_scaled_body_pos_test():
    camera_pos = [0, 0, 0]
    body_pos = [1, 2, 3]
    scale_factor = 2
    print(get_scaled_body_pos(camera_pos, body_pos, scale_factor))

if __name__ == '__main__':
    # get_scaled_body_pos_test()
    D = 600
    mass = 0.9e25
    # camera_pos = 左-右+、上+下-、前+后-
    camera_pos = (-100 * D, 0, -5000 * D)


    def get_position(pos, scale):
        # [ 远+近-  , 左+右-  , 上+下-]
        return pos[0] + (scale - 1.0) * 300 * (random.randint(90, 110)) * D, pos[1], pos[2]

    bodies: list = gen_bodies_from_image(pixel_image="../images/eye.png",
                                         params={"camera_pos": camera_pos})

    print(bodies)
