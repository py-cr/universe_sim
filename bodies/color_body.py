# -*- coding:utf-8 -*-
# title           :颜色天体
# description     :颜色天体
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body
from common.consts import MO
from common.image_utils import gen_color_body_texture, find_texture_root_path
import os
import random


class ColorBody(Body):
    """
    颜色天体基类
    """

    def __init__(self, name="颜色天体", mass=1 * MO,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 color=(0xFF, 0xFF, 0xFF),
                 texture=None, size_scale=1.0, distance_scale=1.0,
                 rotation_speed=None, ignore_mass=False, density=5e3, trail_color=None,
                 texture_bright=None, texture_contrast=None, show_name=False):

        self.color = color
        texture = self.gen_texture(texture, texture_bright, texture_contrast)
        if rotation_speed is None:
            rotation_speed = random.randint(10, 100) / 50
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": density,
            "color": color,
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "rotation_speed": rotation_speed,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name
        }
        super().__init__(**params)

    def gen_texture(self, texture, texture_bright, texture_contrast):
        if texture is None:
            return None
        texture_path = find_texture_root_path()
        if texture_path is None:
            err_msg = "未找到纹理图片目录"
            raise Exception(err_msg)

        temp_dir = os.path.join(texture_path, "temp")
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        texture_name = os.path.basename(texture). \
            replace(".", "_").replace("/", "_"). \
            replace("\\", "_").replace("__", "_")

        save_file = os.path.join(temp_dir, "%s_%s.png" % (texture_name, "_".join([str(i) for i in list(self.color)])))

        if os.path.exists(save_file):
            return save_file

        body_img = os.path.join(texture_path, texture)
        gen_color_body_texture(self.color,
                               bright=texture_bright,
                               contrast=texture_contrast,
                               save_file=save_file,
                               color_body_img=body_img)
        return save_file


if __name__ == '__main__':
    print(ColorBody())
