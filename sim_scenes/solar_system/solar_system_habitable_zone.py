# -*- coding:utf-8 -*-
# title           :太阳系宜居带模拟场景
# description     :太阳系宜居带模拟场景（展示的效果为太阳系真实的距离）
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, HabitableZone, Asteroids
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY, SECONDS_PER_YEAR, AU
from sim_scenes.func import mayavi_run, ursina_run

if __name__ == '__main__':
    # 目前认为 太阳系 的宜居带范围是从距离太阳0.95个天文单位 (约1.42亿千米)到 2.4个天文单位（约3.59亿千米）的范围为宜居带，
    # 其宽度约为2.17亿千米， 按照这个标准，太阳系的宜居带中只有三个大型天体，分别是地球、 月球 以及火星（1.52天文单位）。
    sun = Sun(name="太阳", size_scale=0.5e2)       # 太阳放大 80 倍，距离保持不变
    bodies = [
        sun,
        Venus(name="金星", size_scale=1.5e3),        # 金星放大 4000 倍，距离保持不变
        Earth(name="地球", size_scale=1.5e3),        # 地球放大 4000 倍，距离保持不变
        Moon(name="月球", size_scale=2e3),        # 地球放大 4000 倍，距离保持不变
        Mars(name="火星", size_scale=2e3),         # 火星放大 4000 倍，距离保持不变
        Asteroids(name="小行星群", size_scale=3.2e2,
                  parent=sun),                     # 小行星群模拟(仅 ursina 模拟器支持)
        HabitableZone(name="宜居带", size_scale=1e2,
                  parent=sun),                     # 小行星群模拟(仅 ursina 模拟器支持)
        Jupiter(name="木星", size_scale=2e2),    # 木星放大 800 倍，距离保持不变
    ]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, 1, position=(0, 2 * AU, -11 * AU),
               bg_music="sounds/interstellar.mp3")
