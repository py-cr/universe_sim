# -*- coding:utf-8 -*-
# title           :月球
# description     :月球
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body, AU
from bodies import Earth


class Moon(Body):
    """
    月球
    ------------------------
    　自转周期: 27.32 地球日，自转角速度约为 0.5487 度/小时 = 360/(27.32*24)
    距地距离约: 363104 至 405696 km
    　逃逸速度: 2.4 km/s
    　公转速度: 1.023 km/s + (地球)29.79 km/s
    　天体质量: 7.342✕10²² kg
    　平均密度: 3.344 g/cm³ -> 3.344✕10³ kg/m³
    """

    def __init__(self, name="月球", mass=7.342e22,
                 init_position=[0, 0, 363104 + 1.12 * AU],
                 init_velocity=[-(29.79 + 1.03), 0, 0],
                 texture="moon.jpg", size_scale=1.0, distance_scale=1.0,
                 rotation_speed=0.25, ignore_mass=False,
                 trail_color=None, show_name=False,
                 gravity_only_for_earth=False):
        """
        @param name: 月球名称
        @param mass: 月球质量 (kg)
        @param init_position: 初始位置 (km)
        @param init_velocity: 初始速度 (km/s)
        @param texture: 纹理图片
        @param size_scale: 尺寸缩放
        @param distance_scale: 距离缩放
        @param rotation_speed: 自旋速度（度/小时）
        @param ignore_mass: 是否忽略质量（如果为True，则不计算引力）
                            TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
        @param trail_color:月球拖尾颜色（默认天体颜色）
        @param show_name: 是否显示月球名称
        @param gravity_only_for_earth: 如果为True，则仅适用于地球的重力，与其他天体之间的重力不会受到影响
        """
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": 3.344e3,
            "color": (162, 162, 162),
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "rotation_speed": rotation_speed,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name
        }
        super().__init__(**params)
        self.gravity_only_for_earth = gravity_only_for_earth

    def ignore_gravity_with(self, body):
        """
        是否忽略指定天体的引力
        @param body:
        @return:
        """
        if self.ignore_mass:
            return True

        if self.gravity_only_for_earth:
            # 月球只对地球有引力，忽略其他的引力
            if isinstance(body, Earth):
                return False
        else:
            return False

        return True


if __name__ == '__main__':
    moon = Moon()
    print(moon)
