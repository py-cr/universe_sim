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


class Ganymede(Body):
    """
    木卫三（盖尼米得，Ganymede，Γανυμήδης）是围绕木星运转的一颗卫星，公转周期约为7天。
    按距离木星从近到远排序，在木星的所有卫星中排第七，在伽利略卫星中排第三。它与木卫二及木卫一保持着1:2:4的轨道共振关系。
    ------------------------

中文名木卫三外文名Ganymede，Γανυμήδης别    名盖尼米得分    类卫星发现时间1610年

平均密度1.936 g/cm³
直    径5262 km表
面温度-160 ℃
逃逸速度4 km/s反照率0.43视星等4.6 等自转周期7天离心率0.003
公转周期7天轨道倾角0.20 度表面积87000000km²
体    积7.6×10¹⁰ km³
表面引力1.428 m/s²
平均半径2632.1km大气成分氧气，原子氧，臭氧

轨道参数：
所属行星：木星
平均半径：1,070,400km（0.007155 AU）
离心率：0.003
近拱点：1,069,200km（0.007147 AU）
远拱点：1,071,600km（0.007163 AU）
公转周期：约7天
公转速度：平均10.880km/s
轨道倾角：2.21（黄道夹角）0.20（木星赤道夹角）
物理性质：
平均半径：2,631.2km（地球的0.413倍）
表面积：87.000,000平方千米（地球的0.12倍）
体积：7.6×10¹⁰（地球的0.0705倍）
质量：1.4819×10²³（地球的0.025倍）
平均密度：1.936g/cm
表面引力：1.428m/s
逃逸速度：3km/s
自转周期：7天
转轴倾角：0-0.33
反照率：0.43±0.02
表面温度：最高122K 平均99K 最低：22k
视星等∶5（oppositition）
大气压：极小
大气成份：氧气，原子氧，臭氧

    　逃逸速度: 3 km/s
    　天体质量: 1.4819×10²³ kg
    　平均密度: 1.936 g/cm³ -> 1.936✕10³ kg/m³
    """

    def __init__(self, name="木卫三", mass=1.4819e23,
                 init_position=[0, 0, 1069200],
                 init_velocity=[10.880, 0, 0],
                 texture="jupiter_ganymede.jpg", size_scale=1.0, distance_scale=1.0,
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
        @param gravity_only_for_jupiter: 如果为True，则仅适用于木星的重力，与其他天体之间的重力不会受到影响
        """
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": 1.936e3,
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
    ganymede = Ganymede()
    print(ganymede)
