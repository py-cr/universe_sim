# -*- coding:utf-8 -*-
# title           :小行星
# description     :小行星
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body, AU


class TorusZone(Body):
    """
    模拟环形区域:
    """

    def __init__(self, name="宜居带", mass=1.9891e30,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="green_alpha_1.png",
                 inner_radius=0.95,
                 outer_radius=1.67,
                 subdivisions=64,
                 size_scale=1.0,
                 distance_scale=1.0,
                 rotation_speed=0,
                 parent=None):
        """

        @param name: 天体名称
        @param mass: 天体质量 (kg)
        @param init_position: 初始位置 (km)
        @param init_velocity: 初始速度 (km/s)
        @param texture: 纹理图片
        @param inner_radius: 内圆半径
        @param outer_radius: 外圆半径
        @param subdivisions: 细分数，控制圆环的细节和精度
        @param size_scale: 尺寸缩放
        @param distance_scale: 距离缩放
        @param rotation_speed: 自旋速度（度/小时）
        @param parent: 天体的父对象
        """
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": 1.408e3,
            "color": (179, 231, 255),
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "rotation_speed": rotation_speed,
            "parent": parent
        }
        super().__init__(**params)
        # 环状带（inner_radius, outer_radius, subdivisions）
        self.torus_zone = inner_radius, outer_radius, subdivisions

    def ignore_gravity_with(self, body):
        """
        是否忽略指定天体的引力
        @param body:
        @return:
        """
        # 小行星只对恒星有引力，忽略其他行星的引力
        # if body.is_fixed_star:
        return True

        # return True


if __name__ == '__main__':
    habitable_zone = HabitableZone()
    print(habitable_zone)
