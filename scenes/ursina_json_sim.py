# -*- coding:utf-8 -*-
# title           :ursina模拟器（支持天体json文件的读取）
# description     :ursina模拟器（支持天体json文件的读取）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Body

from common.consts import SECONDS_PER_WEEK, SECONDS_PER_MONTH, SECONDS_PER_YEAR, AU
from scenes.func import ursina_run

if __name__ == '__main__':
    # TODO: 去掉注释，太阳演示
    # bodies, params = Body.build_bodies_from_json('../data/sun.json')
    # TODO: 去掉注释，太阳和地球演示
    # bodies, params = Body.build_bodies_from_json('../data/sun_earth.json')
    # TODO: 去掉注释，在地球上看月相演示变化过程演示
    # bodies, params = Body.build_bodies_from_json('../data/sun_earth_moon.json')
    # TODO: 去掉注释，完美数据的三体模型的演示01（等边三角形）
    bodies, params = Body.build_bodies_from_json('../data/tri_bodies_sim_perfect_01.json')
    # TODO: 去掉注释，完美数据的三体模型的演示02（等边三角形）
    # bodies, params = Body.build_bodies_from_json('../data/tri_bodies_sim_perfect_02.json')
    # TODO: 去掉注释，完美数据的三体模型的演示03（等边三角形）
    # bodies, params = Body.build_bodies_from_json('../data/tri_bodies_sim_perfect_03.json')
    # TODO: 去掉注释，引力弹弓的演示
    # bodies, params = Body.build_bodies_from_json('../data/gravity_slingshot.json')

    dt = params["dt"] if "dt" in params else SECONDS_PER_YEAR
    position = params["position"] if "position" in params else (0, 0, 0)
    show_trail = params["show_trail"] if "show_trail" in params else True

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    json_file = None  # 指定 json_file 保存路径，则会将模拟环境天体数据保存到该json文件中
    ursina_run(bodies, dt, position=position, save_as_json=json_file, show_trail=show_trail)
