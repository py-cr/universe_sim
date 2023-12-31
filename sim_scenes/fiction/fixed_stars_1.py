# -*- coding:utf-8 -*-
# title           :恒星演示
# description     :恒星演示
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Earth, Sirius, Rigel, Bellatrix, Alcyone, Antares, Arcturus, Aldebaran, Betelgeuse
from bodies import EtaCarinae, YCanumVenaticorum, VYCanisMajoris, UYScuti, CarinaeV382, Stephenson_2_18
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_MONTH, SECONDS_PER_YEAR, SECONDS_PER_DAY
from sim_scenes.func import ursina_run
from bodies.body import Body, AU

if __name__ == '__main__':
    """
    恒星演示
    """
    # 构建恒星天体对象
    D = 5e5  # 基本距离单位:km（随意赋值）
    SIZE_SCALE = 0.5  # 所有天体尺寸缩放保持一致
    # TODO: ignore_mass=True
    #  注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
    bodies = [
        Earth(size_scale=SIZE_SCALE, ignore_mass=True),
        Sun(size_scale=SIZE_SCALE, ignore_mass=True),                   # 太阳
        Sirius(size_scale=SIZE_SCALE, ignore_mass=True),                # 天狼星A      质量倍数 2.02   半径倍数 1.71
        # Bellatrix(size_scale=SIZE_SCALE, ignore_mass=True),          # 参宿五       质量倍数 8.6    半径倍数 5.75
        Alcyone(size_scale=SIZE_SCALE, ignore_mass=True),               # 昴宿六       质量倍数 6      半径倍数 9.5
        Arcturus(size_scale=SIZE_SCALE, ignore_mass=True),              # 大角星       质量倍数 1.1    半径倍数 25.7
        Aldebaran(size_scale=SIZE_SCALE, ignore_mass=True),             # 毕宿五       质量倍数 1.16   半径倍数 44.13
        Rigel(size_scale=SIZE_SCALE, ignore_mass=True),                 # 参宿七       质量倍数 18     半径倍数 78
        # YCanumVenaticorum(size_scale=SIZE_SCALE, ignore_mass=True),  # 猎犬座Y      质量倍数 3.0    半径倍数 215
        EtaCarinae(size_scale=SIZE_SCALE, ignore_mass=True),            # 海山二       质量倍数 125    半径倍数 278
        # Antares(size_scale=SIZE_SCALE, ignore_mass=True),            # 心宿二       质量倍数 15     半径倍数 680
        CarinaeV382(size_scale=SIZE_SCALE, ignore_mass=True),           # 船底座V382   质量倍数 39     半径倍数 747
        # Betelgeuse(size_scale=SIZE_SCALE, ignore_mass=True),        # 参宿四       质量倍数 19     半径倍数 1180
        VYCanisMajoris(size_scale=SIZE_SCALE, ignore_mass=True),        # 大犬座VY     质量倍数 30     半径倍数 1400
        # UYScuti(size_scale=SIZE_SCALE, ignore_mass=True),            # 盾牌座 UY    质量倍数 10     半径倍数 1708
        Stephenson_2_18(size_scale=SIZE_SCALE, ignore_mass=True)        # 史蒂文森2-18 质量倍数 40.0   半径倍数 2150
    ]
    distance_sum = 0
    # 循环为每个恒星的初始位置进行赋值，方便演示
    for idx, body in enumerate(bodies):
        body.rotation_speed /= 10  # 恒星的旋转速度减小10倍
        if body.is_fixed_star:
            body.light_on = False  # 关闭灯光效果
        if idx == 0:  # 这是地球
            d = 0
        else:
            d = pow((body.radius + bodies[idx - 1].radius) * SIZE_SCALE, 1.0) * 1.1
        # 所有天体的初始速度为 0
        body.init_velocity = [0, 0, 0]
        # 所有天体的初始位置进行赋值
        body.init_position = [-(distance_sum + d), AU, body.radius * SIZE_SCALE]
        distance_sum += d

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    #             M：摄像机移动加速  N:摄像机移动减速
    # position = (左-右+、上+下-、前+后-)
    ursina_run(bodies, SECONDS_PER_WEEK,
               show_grid=False,
               position=(0, AU, -AU / 500),
               show_name=True, bg_music="sounds/universe_03.mp3")
