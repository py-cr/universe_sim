# -*- coding:utf-8 -*-
# title           :ursina天体视图
# description     :ursina天体视图（天体效果展示用，需要安装 ursina）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import Ursina, window, Entity, Mesh, EditorCamera, color, mouse, Vec2, Vec3, load_texture, Texture, Text
from math import pi, sin, cos
import numpy as np
import math

from simulators.ursina.ursina_config import UrsinaConfig


def create_sphere(radius, subdivisions):
    """
    创建一个球体
    :param radius:
    :param subdivisions:
    :return:
    """
    # 生成球体的顶点、UV坐标uvs、法线tris和三角面
    verts = []
    tris = []
    normals = []
    uvs = []

    for y in range(subdivisions + 1):
        for x in range(subdivisions + 1):
            x_segment = x / subdivisions
            y_segment = -y / subdivisions
            x_pos = cos(x_segment * 2 * pi) * sin(y_segment * pi)
            y_pos = cos(y_segment * pi)
            z_pos = sin(x_segment * 2 * pi) * sin(y_segment * pi)

            verts.append(Vec3(x_pos, y_pos, z_pos) * radius)
            uvs.append(Vec2(x_segment, y_segment))
            normals.append(Vec3(x_pos, y_pos, z_pos))

    for y in range(subdivisions):
        for x in range(subdivisions):
            first = (y * (subdivisions + 1)) + x
            second = first + subdivisions + 1
            # tris.append((first, second + 1, second))
            # tris.append((first, first + 1, second + 1))

            tris.append((second, second + 1, first))
            tris.append((second + 1, first + 1, first))

    # 反转面法线
    # for i in range(len(tris)):
    #     a, b, c = tris[i]
    #     tris[i] = (c, b, a)
    #     normals[a], normals[b], normals[c] = -Vec3(*normals[c]), -Vec3(*normals[b]), -Vec3(*normals[a])
    # normals[a], normals[b], normals[c] = -Vec3(*normals[a]), -Vec3(*normals[b]), -Vec3(*normals[c])
    # 翻转球体
    # for i in range(len(normals)):
    #     normals[i] = -normals[i]

    return Mesh(vertices=verts, triangles=tris, normals=normals, uvs=uvs, mode='triangle')


def create_arrow(height=0.5, width=0.1):
    # 创建金字塔的顶点
    r = width / 2
    verts = [
        (0, height, 0),  # 顶点
        (-r, 0, -r),  # 左后底点
        (r, 0, -r),  # 右后底点
        (r, 0, r),  # 右前底点
        (-r, 0, r),  # 左前底点
    ]
    # 修改指向
    verts = [(z, x, y) for x, y, z in verts]

    # 定义金字塔的面
    faces = [
        (0, 1, 2),  # 底面1
        (0, 2, 3),  # 底面2
        (0, 3, 4),  # 底面3
        (0, 4, 1),  # 底面4
        (4, 2, 1),  # 侧面1
        (4, 3, 2),  # 侧面1
    ]

    # 创建一个金字塔的Mesh对象
    arrow_mesh = Mesh(vertices=verts, triangles=faces, mode='triangle')
    return arrow_mesh


def create_label(parent, label, pos, color, scale=50, alpha=1.0):
    text = Text(label, parent=parent, scale=scale, billboard=True, color=color,
                position=Vec3(pos) + Vec3(1, 1, 1), alpha=alpha,
                font=UrsinaConfig.CN_FONT, background=False)
    return text


def create_arrow_line(from_pos, to_pos, parent=None, label=None,
                      set_light_off=True, alpha=1.0, len_scale=0.5,
                      color=color.white, thickness=2,
                      arrow_scale=1, text_scale=50):
    """
    创建箭头和箭头线段
    @param from_pos: 箭头线段开始位置
    @param to_pos: 箭头线段结束位置
    @param parent:
    @param label: 箭头显示的文字
    @param set_light_off: 是否设置为灯光关闭状态
    @param alpha: 透明度
    @param len_scale: 长度缩放
    @param color: 箭头线颜色
    @param thickness: 线段粗细
    @param arrow_scale: 箭头缩放
    @return:
    """
    height = 0.5 * thickness
    width = 0.1 * thickness
    arrow_mesh = create_arrow(height, width)
    from_pos, to_pos = (Vec3(from_pos), Vec3(to_pos))
    line = Entity(parent=parent,
                  model=Mesh(vertices=(from_pos * len_scale, to_pos * len_scale), mode='line', thickness=thickness),
                  color=color, alpha=alpha)
    arrow = Entity(parent=line, model=arrow_mesh, position=to_pos * len_scale,
                   scale=thickness * arrow_scale, color=color, alpha=alpha)
    arrow.look_at(to_pos * 100)

    if set_light_off:
        line.set_light_off()
        arrow.set_light_off()

    if label is not None:
        text = create_label(parent=line, label=label, pos=Vec3(to_pos) * len_scale * 1.2,
                            color=color, scale=text_scale, alpha=alpha)
        if set_light_off:
            text.set_light_off()
    else:
        text = None

    return arrow, line, text


def create_pyramid():
    # 创建金字塔的顶点
    verts = [
        (0, 2, 0),  # 顶点
        (-1, 0, -1),  # 左后底点
        (1, 0, -1),  # 右后底点
        (1, 0, 1),  # 右前底点
        (-1, 0, 1),  # 左前底点
    ]

    # 定义金字塔的面
    faces = [
        (0, 1, 2),  # 底面1
        (0, 2, 3),  # 底面2
        (0, 3, 4),  # 底面3
        (0, 4, 1),  # 底面4
        (4, 2, 1),  # 侧面1
        (4, 3, 2),  # 侧面1
    ]

    # 创建一个金字塔的Mesh对象
    # verts = [(0, 1, 0), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1)]
    # faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 3, 2)]
    pyramid_mesh = Mesh(vertices=verts, triangles=faces, mode='triangle')

    return pyramid_mesh


def create_body_torus(inner_radius, outer_radius, subdivisions):
    vertices = []
    uvs = []
    normals = []
    triangles = []

    # 计算圆环顶点、法向量和纹理坐标
    for i in range(subdivisions):
        for j in range(subdivisions):
            # 计算纹理坐标
            u = i / subdivisions
            v = j / subdivisions
            # 计算球面坐标系下的角度
            theta = u * math.pi * 2
            phi = v * math.pi * 2

            # 计算圆环顶点位置
            x = (outer_radius + inner_radius * math.cos(phi)) * math.cos(theta)
            y = inner_radius * math.sin(phi) * (inner_radius) / 2
            z = (outer_radius + inner_radius * math.cos(phi)) * math.sin(theta)

            # 计算圆环顶点法向量
            nx = math.cos(theta) * math.cos(phi)
            ny = math.sin(phi)
            nz = math.sin(theta) * math.cos(phi)

            vertices.append((x, y, z))
            normals.append((nx, ny, nz))
            uvs.append((u, v))

    # 计算圆环三角形面片
    for i in range(subdivisions):
        for j in range(subdivisions):
            i1 = i
            j1 = j
            i2 = (i + 1) % subdivisions
            j2 = (j + 1) % subdivisions

            p1 = i1 * subdivisions + j1
            p2 = i2 * subdivisions + j1
            p3 = i2 * subdivisions + j2
            p4 = i1 * subdivisions + j2

            triangles.append((p1, p2, p3))
            triangles.append((p1, p3, p4))
    # uvs = [[u * 2, v] for u, v in uvs]
    # 创建 mesh 对象
    mesh = Mesh(vertices=vertices, uvs=uvs, normals=normals, triangles=triangles, mode='triangle')

    return mesh


def create_torus(inner_radius, outer_radius, subdivisions, repeat=1):
    verts = []
    tris = []
    uvs = []

    for i in range(subdivisions):
        angle = i * (360 / subdivisions)
        x = np.cos(angle * np.pi / 180)
        y = np.sin(angle * np.pi / 180)

        # create vertices for inner radius
        inner_x = x * inner_radius
        inner_y = y * inner_radius
        # create vertices for outer radius
        outer_x = x * outer_radius
        outer_y = y * outer_radius

        if i % int(subdivisions / repeat) == 0:
            verts.append((inner_x, inner_y, 0))
            verts.append((outer_x, outer_y, 0))
            uvs.append((0.999, 0.0))
            uvs.append((0.999, 0.999))
            verts.append((inner_x, inner_y, 0))
            verts.append((outer_x, outer_y, 0))
            uvs.append((0.001, 0.0))
            uvs.append((0.001, 0.999))
        else:
            verts.append((inner_x, inner_y, 0))
            verts.append((outer_x, outer_y, 0))
            # create uvs
            u = angle * repeat / 360 % 1
            uvs.append((u, 0.0))
            uvs.append((u, 0.999))

        # create triangles
        first_index = i * 2
        second_index = (i * 2 + 2) % (subdivisions * 2)
        third_index = (i * 2 + 1) % (subdivisions * 2)
        fourth_index = (i * 2 + 3) % (subdivisions * 2)

        tris.append((first_index, second_index, third_index))
        tris.append((third_index, second_index, fourth_index))

    # create normals
    normals = []
    for i in range(len(verts)):
        angle = i * (360 / subdivisions)
        x = np.cos(angle * np.pi / 180)
        y = np.sin(angle * np.pi / 180)
        normals.append((x, y, 0))

    # create mesh
    mesh = Mesh(vertices=verts, triangles=tris, uvs=uvs, normals=normals, mode='triangle')

    # add color attribute
    # mesh.colorize()

    return mesh


if __name__ == '__main__':
    app = Ursina()
    # # 使用 Mesh 类创建球体
    texture = "../../textures/saturn.jpg"
    textureRings = '../../textures/saturnRings.jpg'
    textureAsteroids = '../../textures/asteroids.png'

    # 创建球体
    # sphere = create_sphere(1, 32)
    # entity = Entity(model=sphere, texture=texture, color=color.white)
    # 创建光晕
    # glow_entity = Entity(parent=entity, model='sphere', color=color.rgb(1,1,1,0.1),
    #                      scale=2.1, alpha=0.1)
    #

    # torus = create_body_torus(0.8, 2, 64)
    # textureRings = load_texture(textureRings)
    # entity = Entity(model=torus, texture=textureRings, rotation=(0, 0, 0), double_sided=True)

    # torus = create_torus(1.5, 3, 64)
    # entity = Entity(model=torus, texture=textureRings, rotation=(85, 0, 0), double_sided=True)

    # body_torus = create_torus(9, 10, 64)
    # entities = Entity(model=body_torus, texture=textureAsteroids, rotation=(85, 0, 0), double_sided=True)
    # entities.set_light_off()

    # 创建金字塔的实体对象
    # pyramid = Entity(model=create_pyramid(), texture='brick', color=color.yellow)
    # pyramid.set_light_off()

    # arrow = Entity(model=create_arrow(), color=color.yellow)
    # arrow.set_light_off()

    arrow, line, text = create_arrow_line((0, 0, 0), (10, 0, 0))

    EditorCamera()
    app.run()
