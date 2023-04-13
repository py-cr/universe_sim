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


class Europa(Body):
    """
    木卫二（Europa，[juəˈrəupə]，欧罗巴），在1610年被伽利略发现，是木星的第六颗已知卫星，是木星的第四大卫星，在伽利略发现的卫星中离木星第二近。
    ------------------------
中文名木卫二外文名Europa
IPA发现时间1610年1月
质    量4.80×10²² kg
平均密度3.014 g/cm³
直    径3138 km
逃逸速度2020m/s
公转周期3天半
表面积3.1×10⁷ km²
体    积1.593×10¹⁰ km³
重力加速度1.3 m/s²公转轨道
距离木星670,900 千米
轨道偏心率0.009赤道地区温度110K(-163 ℃)两极温度50K(-223 ℃)母行星木星

相关数据
发现者
伽利略
马里乌斯
轨道平均半径
671,034 km
离心率
0.0094
近地点
664,700 km (0.00444 AU)
远地点
677,300 km (0.00453 AU)
公转周期
3.551181041 d
轨道周长
4,216,100 km (0.028 AU)
最大公转速度
13.871 km/s
平均公转速度
13.741 km/s
最小公转速度
13.613 km/s
所属行星
天然卫星之一
平均直径
3,121.6 km
表面积
3.1×107 km²
体积
1.593×1010 km³
质量
4.80×1022 kg
平均密度
3.014g
表面重力
1.314 m/s2 (0.134 g)
逃逸速度
2.025 km/s
自转周期
与公转同步
赤道转速
zero
自转轴倾角
0.67
反照率
5.3


    　逃逸速度: 2.02 km/s
    　天体质量: 4.80×10²² kg
    　平均密度: 3.014 g/cm³ -> 3.014✕10³ kg/m³
    """

    def __init__(self, name="木卫二", mass=4.80e22,
                 init_position=[0, 0, 670900],
                 init_velocity=[-13.741, 0, 0],
                 texture="jupiter_europa.jpg", size_scale=1.0, distance_scale=1.0,
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
    europa = Europa()
    print(europa)
