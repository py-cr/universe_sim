# -*- coding:utf-8 -*-
# title           :改造后金星的3D效果
# description     :改造后金星的3D效果
# author          :Python超人
# date            :2023-07-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from sim_scenes.fiction.transformed_planet import run_transformed_planet

if __name__ == '__main__':
    run_transformed_planet(
        # transformed_texture="venus.jpg",
        texture="venus.jpg",
        camera3d=True,
        transparent=True
    )
