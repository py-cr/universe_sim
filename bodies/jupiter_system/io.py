# -*- coding:utf-8 -*-
# title           :木卫一Io
# description     :木卫一Io
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body, AU
from bodies import Jupiter


class Io(Body):
    """
    木卫一Io:即伊奥，是木星的四颗伽利略卫星中最靠近木星的一颗卫星
    ------------------------
中文名木卫一外文名Io
别    名伊奥分    类卫星发现者伽利略、马里乌斯发现时间1610年1月7日
质    量8.9319×10²² kg (0.015木星)
平均密度3.528 g/cm³
直    径3637.4 km
表面温度平均 130K ；最大 2000 K逃逸速度2.558 km/s反照率0.63 ± 0.02视星等5.02 (冲)表面积41,910,000 km² (0.082木星)
体    积2.53×10¹⁰ km³ (0.023木星)赤道旋转速率271 km/h

物理特征
大小： 3,660.0 × 3,637.4 × 3,630.6 km
赤道表面引力： 1.796 m/s²(0.183 g)
宇宙速度： 2.558 km/s
自转周期： 同步的
赤道旋转速率： 271 km/h
反照率： 0.63 ± 0.02
表面温度：平均 130K ；最大 2000 K
星等： 5.02 (冲)
轨道资料
近拱点： 420,000 km (0.002 807 AU)
远拱点： 423,400 km (0.002 830 AU)
平均轨道半径： 421,700 km (0.002 819 AU)
轨道离心率： 0.0041
轨道周期： 1.769 137 786 d (152 853.504 7 s, 42 h)
平均公转速度： 17.334 km/s
轨道倾角： 2.21° （对黄道）
0.05°（对木星的赤道）
卫星所属星球： 木星


    　逃逸速度: 2.558 km/s
    　天体质量: 8.9319×10²² kg
    　平均密度: 3.528 g/cm³ -> 3.528✕10³ kg/m³
    """

    def __init__(self, name="木卫一", mass=8.9319e22,
                 init_position=[0, 0, 420000],
                 init_velocity=[17.334, 0, 0],
                 texture="jupiter_io.jpg", size_scale=1.0, distance_scale=1.0,
                 rotation_speed=0.25, ignore_mass=False,
                 trail_color=None, show_name=False,
                 gravity_only_for_jupiter=False):
        """
        @param name: 木卫名称
        @param mass: 木卫质量 (kg)
        @param init_position: 初始位置 (km)
        @param init_velocity: 初始速度 (km/s)
        @param texture: 纹理图片
        @param size_scale: 尺寸缩放
        @param distance_scale: 距离缩放
        @param rotation_speed: 自旋速度（度/小时）
        @param ignore_mass: 是否忽略质量（如果为True，则不计算引力）
                            TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
        @param trail_color:木卫拖尾颜色（默认天体颜色）
        @param show_name: 是否显示木卫名称
        @param gravity_only_for_earth: 如果为True，则仅适用于木星的重力，与其他天体之间的重力不会受到影响
        """
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": 3.528e3,
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
        self.gravity_only_for_jupiter = gravity_only_for_jupiter

    def ignore_gravity_with(self, body):
        """
        是否忽略指定天体的引力
        @param body:
        @return:
        """
        if self.ignore_mass:
            return True

        if self.gravity_only_for_jupiter:
            # 只对木星有引力，忽略其他的引力
            if isinstance(body, Jupiter):
                return False
        else:
            return False

        return True


if __name__ == '__main__':
    io = Io()
    print(io)
