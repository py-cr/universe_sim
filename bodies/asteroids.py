# -*- coding:utf-8 -*-
# title           :小行星
# description     :小行星
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body, AU
from bodies.torus_zone import TorusZone


class Asteroids(TorusZone):
    """
    小行星群
    质量 (kg):~4.1×1010 kg
    密度 :2.3±0.3 g/cm&sup3;
    ------------------------
    小行星带距离太阳约2.17-3.64天文单位的空间区域内，聚集了大约50万颗以上的小行星。
    这么多小行星能够被凝聚在小行星带中，除了太阳的引力作用以外，木星的引力也起着作用。
    [小行星25143的数据如下]:
     远日点距离: 253.520Gm (1.695AU)
     近日点距离: 142.568Gm (0.953AU)
       逃逸速度: 0.0002 km/s
     　公转速度: 25.37 km/s
     　天体质量: 4.1✕10¹⁰ kg
     　平均密度: 2.3✕10³ kg/m³
    """

    def __init__(self, name="小行星群", mass=1.9891e30,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="asteroids.png",
                 inner_radius=2.17,
                 outer_radius=3.64,
                 subdivisions=64,
                 size_scale=1.0,
                 distance_scale=1.0,
                 rotate_angle=0,
                 rotation_speed=0.002,  # 小行星绕太阳转一圈的时间在数年到几十年之间不等。
                 parent=None):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "inner_radius": inner_radius,
            "outer_radius": outer_radius,
            "subdivisions": subdivisions,
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "rotation_speed": rotation_speed,
            "rotate_angle": rotate_angle,
            "parent": parent
        }
        super().__init__(**params)
        # 环状星群
        # self.torus_stars = True
        # 环状星群带（inner_radius, outer_radius, subdivisions）
        # inner_radius:内圆半径 outer_radius:外圆半径，subdivisions:细分数，控制圆环的细节和精度
        # self.torus_zone = 2.17, 3.64, 64

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
    asteroids = Asteroids()
    print(asteroids)
