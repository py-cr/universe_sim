# -*- coding:utf-8 -*-
# title           :太阳系场景模拟（展示用）
# description     :太阳系场景模拟（为了更好的展示效果，对距离进行的调整，不是太阳系的真实距离）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Asteroids
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run
import math
from common.consts import G


def get_velocity(mass, distance, velocity, target_distance):
    """
    根据天体的质量和天体原始距离、速度，计算出能稳定围绕太阳转的速度。
    @param mass: 天体质量，单位 kg
    @param distance: 天体原始距离，单位 km
    @param velocity: 天体原始速度，单位 km/s
    @param target_distance: 目标距离，即新轨道的距离，单位 km
    @return: 稳定围绕太阳转的速度，单位 km/s
    """
    v = velocity * pow(distance / target_distance, 0.5)
    # # 计算原始速率
    # v0 = math.sqrt(G * mass / distance * 1000)
    # # 计算目标速率
    # v_target = math.sqrt(G * mass / target_distance * 1000)
    # # 计算需要调整的速率量
    # dv = v_target - v0
    # # 新速度等于原始速度加上调整速率量
    # v = (velocity*1000 + dv)/1000
    return [v, 0, 0]


if __name__ == '__main__':
    # 八大行星：木星(♃)、土星(♄)、天王星(♅)、海王星(♆)、地球(⊕)、金星(♀)、火星(♂)、水星(☿)
    # 排列顺序
    # 1、体积：(以地球为1)木星 ：土星 ：天王星 ：海王星 ：地球 ：金星 ：火星 ：水星 = 1330：745：65：60：1：0.86：0.15：0.056
    # 2、质量：(以地球为1)木星 ：土星 ：天王星 ：海王星 ：地球 ：金星 ：火星 ：水星 = 318：95：14.53：17.15：1：0.8：0.11：0.0553
    # 3、离太阳从近到远的顺序：水星、金星、地球、火星、木星、土星、天王星、海王星
    #  =====================================================================
    #  以下展示的效果为太阳系真实的距离
    #  由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
    sun = Sun(name="太阳", size_scale=1.4e2)  # 太阳放大 80 倍，距离保持不变
    sun.init_velocity = [0, 2, 0]  # 太阳以2km/s的速度带着其他行星一起跑
    bodies = [
        sun,
        Mercury(name="水星", size_scale=4e3),  # 水星放大 4000 倍，距离保持不变
        Venus(name="金星", size_scale=4e3),  # 金星放大 4000 倍，距离保持不变
        Earth(name="地球", size_scale=4e3),  # 地球放大 4000 倍，距离保持不变
        Mars(name="火星", size_scale=4e3),  # 火星放大 4000 倍，距离保持不变
        Asteroids(name="小行星群", size_scale=3.2e2,
                  parent=sun),  # 小行星群模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=0.6e3),  # 木星放大 800 倍，距离保持不变
        Saturn(name="土星", size_scale=0.6e3),  # 土星放大 800 倍，距离保持不变
        Uranus(name="天王星", size_scale=0.8e3),  # 天王星放大 800 倍，距离保持不变
        Neptune(name="海王星", size_scale=1e3),  # 海王星放大 1000 倍，距离保持不变
        Pluto(name="冥王星", size_scale=10e3),  # 冥王星放大 10000 倍，距离保持不变(从太阳系的行星中排除)
    ]

    # 真实距离
    # body_real_distances = [0.4 * AU, 0.72 * AU, AU, 1.5 * AU,
    #                        5.2 * AU, 10 * AU, 19 * AU, 30 * AU, 40 * AU]

    # 调整距离方便演示
    body_distances = [1 * AU, 1.5 * AU, 1.8 * AU, 2.3 * AU, 3.6 * AU,
                      4.2 * AU, 5.3 * AU, 6 * AU, 7 * AU]
    body_index = 0
    # 设置为行星距离
    for idx, body in enumerate(bodies):
        # 对于太阳和小行星群保持原来的距离
        if body.is_fixed_star or hasattr(body, "torus_stars"):
            continue
        body_real_distance = body.init_position[2]  # 格式：body.init_position=[0, 0, 1.12 * AU]
        body_real_velocity = body.init_velocity[0]  # 格式：body.init_velocity=body.[-29.79, 0, 0]
        body.init_position = [0, 0, body_distances[body_index]]
        # 距离变化，将要重新设置速度
        init_velocity = get_velocity(body.mass, body_real_distance, body_real_velocity, body_distances[body_index])
        body.init_velocity = init_velocity
        body_index += 1

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_YEAR, position=(0, 2 * AU, -11 * AU),
               show_trail=True,  # 运行轨迹拖尾效果（通过快捷键 I 控制开关）
               bg_music="sounds/interstellar.mp3")
