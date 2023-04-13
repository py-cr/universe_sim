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


class Callisto(Body):
    """
    木卫四又称为卡里斯托（Callisto、英语发音：/kəˈlɪstoʊ/、希腊文：Καλλιστώ）是围绕木星运转的一颗卫星，由伽利略·伽利莱在1610年首次发现。木卫四是太阳系第三大卫星，也是木星第二大卫星，仅次于木卫三。
    ------------------------
中文名木卫四外文名Callisto分    类卫星
质    量1.08 x 10²³ 千克
直    径4800 km
自转周期16.7个地球日
公转周期16.7个地球日
公转轨道距木星1,883,000 千米

木卫四（左下角）、木星和木卫二（位于木星大红斑的左下方）。木卫四是距离木星最远的伽利略卫星，
其轨道距离木星约188万公里(是木星半径——7万1398公里——的26.3倍)，比之距离木星次近的木卫三的轨道半径——107万公里——远得多。由于轨道半径较大，故其并不处于轨道共振状态，可能永远也不会处于这种状态。

    　逃逸速度:
    　天体质量: 1.08 x 10²³ kg
    　平均密度:  g/cm³ -> ✕10³ kg/m³
    """

    def __init__(self, name="木卫四", mass=1.08e23,
                 init_position=[0, 0, 1880000],
                 init_velocity=[8.15, 0, 0],
                 texture="jupiter_callisto.jpg", size_scale=1.0, distance_scale=1.0,
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
            "density": 3.014e3,
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
    callisto = Callisto()
    print(callisto)
