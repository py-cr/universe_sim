# -*- coding:utf-8 -*-
# title           :ursina天体Planet
# description     :ursina天体Planet
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import Entity, camera, color, Vec3, Text, load_texture, destroy, PointLight

from simulators.ursina.entities.entity_utils import create_name_text, create_trails, clear_trails, create_rings, \
    trail_init, create_fixed_star_lights
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from common.color_utils import adjust_brightness, conv_to_vec4_color, get_inverse_color
from common.func import find_file
from simulators.views.body_view import BodyView
from simulators.ursina.ursina_mesh import create_sphere, create_torus, create_arrow_line
import math


class Planet(Entity):

    @property
    def body(self):
        return self.body_view.body

    def on_reset(self):
        # 删除拖尾
        clear_trails(self)
        self.body.reset()

    def __init__(self, body_view: BodyView):
        self.body_view = body_view
        self.rotation_speed = self.body.rotation_speed
        self.rotMode = 'x'  # random.choice(["x", "y", "z"])
        self.name = body_view.name

        pos = body_view.position * body_view.body.distance_scale * UrsinaConfig.SCALE_FACTOR
        scale = body_view.body.diameter * body_view.body.size_scale * UrsinaConfig.SCALE_FACTOR
        self.init_scale = scale
        if hasattr(body_view, "texture"):
            texture = load_texture(body_view.texture)
            # color.white
            self.plant_color = color.white
        else:
            texture = None
            b_color = self.body_view.color
            if len(b_color) == 3:
                b_color = (b_color[0], b_color[1], b_color[2], 1.0)
            self.plant_color = color.rgba(*b_color)

        if hasattr(self.body, "torus_stars"):
            # 创建一个星环小天体群（主要模拟小行星群，非一个天体）
            model = create_torus(0.83, 1.05, 64, 1)
            rotation = (90, 0, 0)
        else:
            # 创建一个天体
            subdivisions = 32
            if self.body.resolution is not None:
                subdivisions = self.body.resolution

            model = create_sphere(0.5, subdivisions)
            rotation = (0, 0, 0)

        UrsinaEvent.on_reset_subscription(self.on_reset)

        super().__init__(
            # model="sphere",
            model=model,
            scale=scale,
            texture=texture,
            color=self.plant_color,
            position=pos,
            rotation=rotation,
            double_sided=True
        )

        if hasattr(self.body, "torus_stars"):
            # 星环小天体群（主要模拟小行星群，非一个天体）
            self.set_light_off()
            self.double_sided = True
        else:
            # 一个天体
            # 拖尾球体的初始化
            trail_init(self)

        if self.body.is_fixed_star:
            # 如果是恒星，开启恒星的发光的效果、并作为灯光源
            create_fixed_star_lights(self)
        elif self.body.light_disable:
            # 如果是非恒星，并且禁用灯光
            self.set_light_off()

        if self.body.show_name:
            create_name_text(self)

        if self.body.has_rings:
            # 创建行星环（目前只有土星环）
            create_rings(self)

    def turn(self):
        if hasattr(self.body, "torus_stars"):
            # 星环小天体群（主要模拟小行星群，非一个天体）不受 body_size_factor 影响
            self.scale = self.init_scale
        else:
            self.scale = self.init_scale * UrsinaConfig.body_size_factor

        pos = self.body_view.position * UrsinaConfig.SCALE_FACTOR
        if self.body.parent is None:
            # TODO: ????????
            self.x = -pos[1]
            self.y = pos[2]
            self.z = pos[0]
        else:
            self.follow_parent()

        dt = 0
        if hasattr(self.body, "dt"):
            dt = self.body.dt
        if self.rotation_speed is None or dt == 0:
            self.rotspeed = 0
            # 旋转速度和大小成反比（未使用真实数据）
            # self.rotspeed = 30000 / self.body_view.raduis  # random.uniform(1.0, 2.0)
        else:
            # 是通过月球保持一面面对地球，调整得到
            self.rotspeed = self.rotation_speed * (dt / 3600) / 2.4 * \
                            UrsinaConfig.ROTATION_SPEED_FACTOR * UrsinaConfig.body_spin_factor
            # rotation_speed 度/小时  dt 秒 = (dt / 3600)小时

        # if self.rotation_y < 0:
        #     self.rotation_y += 360
        try:
            # 天体旋转
            self.rotation_y -= self.rotspeed
        except Exception as e:
            print(self.body)
            self.destroy_all()
            return

        # 如果有行星环
        if hasattr(self, "ring"):
            # 如果有行星环，则不让行星环跟随行星转动
            self.ring.rotation = -Vec3(self.rotation_x - self.ring_rotation_x,
                                       self.rotation_y,
                                       self.rotation_z)

        if UrsinaConfig.show_trail:
            # 有时候第一个位置不正确，所以判断一下有历史记录后在创建
            if len(self.body.his_position()) > 1:
                create_trails(self)
        else:
            clear_trails(self)

        if hasattr(self, "name_text"):
            d = (camera.world_position - self.name_text.world_position).length()

            if d < pow(self.scale_x, 1.02) * 1.2:
                self.name_text.visible = False
            else:
                self.name_text.visible = True
            # print(d, self.name_text.text, self.scale_x ,self.scale_x*1.23)
            # # 计算相机和实体之间的距离
            # distance = (camera.world_position - self.world_position).length()
            # # 根据距离设置文本缩放比例
            # self.name_text.scale = distance / 10

    def follow_parent(self):
        if not hasattr(self, "f_parent"):
            if not hasattr(self.body_view, "bodies_system"):
                return
            sys = self.body_view.bodies_system
            for b in sys.bodies:
                if self.body.parent == b:
                    self.f_parent = b
                    break
        pos = self.f_parent.position * UrsinaConfig.SCALE_FACTOR
        # TODO: ????????
        self.x = -pos[1]
        self.y = pos[2]
        self.z = pos[0]

    def destroy_all(self):
        # 从天体系统中移除自己（TODO:暂时还不能移除）
        # self.body_view.bodies_system.bodies.remove(self.body)
        # 删除拖尾
        clear_trails(self)
        # 如果有行星环，则删除行星环
        if hasattr(self, "ring"):
            destroy(self.ring)
        self.body.appeared = False
        self.body_view.appeared = False
        # 最后删除自己
        destroy(self)
