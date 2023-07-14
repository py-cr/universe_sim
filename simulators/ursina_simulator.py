# -*- coding:utf-8 -*-
# title           :ursina天体运行模拟器
# description     :ursina天体运行模拟器
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from ursina import Ursina, window, Entity, Grid, camera, application, color, distance, Audio, Animation
import itertools

from common.image_utils import find_texture
from simulators.ursina.ursina_event import UrsinaEvent
# from simulators.ursina.ursina_ui import UrsinaUI
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ui.control_handler import ControlHandler
from simulators.ursina.ursina_mesh import create_arrow_line
from simulators.ursina.entities.body_timer import BodyTimer
from simulators.views.ursina_view import UrsinaView
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.simulator import Simulator
from common.system import System
from simulators.ursina.entities.world_grid import WorldGrid
from simulators.ursina.entities.sphere_sky import SphereSky
from common.func import find_file, find_intersection
import datetime
import os
from ursina import EditorCamera
from sim_scenes.func import ursina_run


class UrsinaSimulator(Simulator):
    """
    Ursina官网： https://www.ursinaengine.org/
    """

    def __init__(self, bodies_sys: System):
        # window.borderless = False
        window.title = '宇宙模拟器(universe sim)'  # 'universe_sim'  # '宇宙模拟器'
        icon = find_file("images/icon.ico")
        window.icon = icon
        self.app = Ursina()
        # import os
        # os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # 选择第二个GPU
        # self.app = Ursina(window_title='GPU模拟',
        #              window_kwargs={'vsync': True, 'fullscreen': False, 'borderless': False, 'show_ursina_splash': True,
        #                             'high_resolution': True})
        self.ursina_views = []
        window.color = color.black

        super().__init__(bodies_sys, UrsinaView)

        # ps = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
        # cp = [200, 15, 35, 42, 20, 160, 145, 90, 80]
        # x, y, z = 0, 0, 0
        for i, view in enumerate(self.body_views):
            # pos = tuple(body.position)
            # ursina_view = UrsinaView(body)
            self.bind_event(view.body)
            view.update()
            self.ursina_views.append(view)
            # planets.append(newPlanet)
            # x += cp[i] * 10
        self.adjust_system_motion_params()
        UrsinaEvent.on_searching_bodies_subscription(type(self).__name__, self.on_searching_bodies)

    def bind_event(self, body):

        def body_look_at(target, rotation_x=None, rotation_y=None, rotation_z=None):
            """
            让 body 看向 target 目标天体
            @param target: 目标天体
            @param rotation_x: x轴旋转角度（None表示不旋转）
            @param rotation_y: y轴旋转角度（None表示不旋转）
            @param rotation_z: z轴旋转角度（None表示不旋转）
            @return:
            """
            if hasattr(target, "planet") and hasattr(body, "planet"):
                body.planet.main_entity.look_at(target.planet.main_entity)
                if rotation_x is not None:
                    body.planet.rotation_x = rotation_x
                if rotation_y is not None:
                    body.planet.rotation_y = rotation_y
                if rotation_z is not None:
                    body.planet.rotation_z = rotation_z

        def body_visible(visible):
            body.planet.enabled = visible

        @property
        def body_visibled():
            return body.planet.enabled

        # Explosion animation
        def body_explode(target=None):
            # from panda3d.core import GeomUtils
            if body.planet.enabled:
                # TODO:下面代码保留，由于运行太快导致两个天体不是在表面碰撞，这样就要进行计算，希望在表面爆炸，但是需要耗费CPU资源，暂时注释
                # line_start_pos = body.his_position()[0] * UrsinaConfig.SCALE_FACTOR
                # line_end_pos = body.planet.position
                # sphere_center = target.position * UrsinaConfig.SCALE_FACTOR
                # # sphere_radius = target.planet.scale_x/2
                # sphere_radius = target.radius * target.size_scale * UrsinaConfig.SCALE_FACTOR
                # explode_pos = find_intersection(sphere_center, sphere_radius, line_start_pos, line_end_pos)
                # if explode_pos is None:
                #     explode_pos = body.planet.position
                # else:
                #     print("explode_pos", explode_pos)

                explode_pos = body.planet.position
                # 如果爆炸，则静止不动（停止并忽略引力）
                body.stop_and_ignore_gravity()
                body.planet.enabled = False
                explosion_file = find_file("images/explosion")
                explosion_file = os.path.join(explosion_file, "explosion")
                # 获取体积数据（开三次方）
                volume_scale = pow(body.planet.model.get_bounds().volume, 1 / 3)
                # 根据体积、大小缩放判断爆炸的量
                scale = 3 * volume_scale * body.size_scale * UrsinaConfig.SCALE_FACTOR
                print(scale, body)
                explode_ani = Animation(explosion_file,
                                        position=explode_pos,
                                        scale=scale, fps=6,
                                        loop=False, autoplay=True)
                explode_ani.set_light_off()

                if target is not None:
                    if hasattr(target, "planet"):
                        if hasattr(target.planet, "main_entity"):
                            explode_ani.world_parent = target.planet.main_entity
                            explode_ani.look_at(target.planet.main_entity)
                        else:
                            explode_ani.world_parent = target.planet
                            explode_ani.look_at(target.planet)
                    else:
                        explode_ani.world_parent = target
                        explode_ani.look_at(target)
                return explode_ani

        body.look_at = body_look_at
        body.set_visible = body_visible
        body.explode = body_explode
        body.visibled = body_visibled

    # def get_bodies_max_distance(self, body_views):
    #     max_distance = 0
    #     for b1 in body_views:
    #         if b1.body.ignore_mass:
    #             continue
    #         for b2 in body_views:
    #             if (b1 is b2) or b2.body.ignore_mass:
    #                 continue
    #         d = distance(b1.planet, b2.planet)
    #         if d > max_distance:
    #             max_distance = d
    #     return max_distance

    def get_bodies_max_distance(self, body_views):
        """
        算法优化
        @param body_views:
        @return:
        """
        max_distance = 0
        for b1, b2 in itertools.combinations(body_views, 2):
            if b1.body.ignore_mass or b2.body.ignore_mass:
                continue
            d = distance(b1.planet, b2.planet)
            if d > max_distance:
                max_distance = d
        if max_distance == 0:
            if len(body_views) > 0:
                # 如果最大距离等于0，说明只有一个有效的天体，则以第一个天体的半径为基准
                max_distance = pow(body_views[0].planet.scale_x, 3)
        return max_distance

    def adjust_system_motion_params(self):
        """
        调整天体系统运行的参数
        @return:
        """
        max_distance = self.get_bodies_max_distance(self.body_views)
        # 根据天体之间的距离，调整 application.time_scale（控制摄像头运动的速度）
        time_scale = round(pow(max_distance, 1 / 4), 2)
        if time_scale < 0.01:
            time_scale = 0.01
        # camera.scale
        # sence
        application.time_scale = time_scale
        UrsinaConfig.time_scale_offset = 1 / application.time_scale
        # UrsinaConfig.auto_scale_factor = 1.0e-9

    def on_searching_bodies(self, **kwargs):
        views = []
        for view in self.body_views:
            # if view.appeared:
            views.append(view)
        return views

    def check_interval_expired(self):
        """
        检查时间间隔是否已过期
        @return:
        """
        now = datetime.datetime.now()
        elapsed_time = now - self.last_time
        is_expired = elapsed_time >= self.interval
        if is_expired:
            self.last_time = now
        return is_expired

    def check_and_evolve(self):
        if self.check_interval_expired():
            # 获取配置中的运行速度的因子
            run_speed_factor = float(UrsinaConfig.run_speed_factor)
            if UrsinaConfig.seconds_per <= 0:
                # 配置中，如果为0秒，表示默认开始运行设置的秒数（evolve_dt）
                evolve_dt = self.evolve_dt * run_speed_factor
            else:
                # 配置中，每年、月、天等等有多少秒
                evolve_dt = UrsinaConfig.seconds_per * run_speed_factor

            UrsinaEvent.on_evolving(evolve_dt)
            # interval_fator 能让更新天体运行状态（位置、速度）更精确
            evolve_dt = evolve_dt * self.interval_fator
            evolve_args = {"evolve_dt": evolve_dt}
            UrsinaEvent.on_before_evolving(evolve_args)
            # if evolve_args["evolve_dt"] > 0:
            super().evolve(evolve_args["evolve_dt"])

            if self.show_timer or self.timer_enabled:
                timer = BodyTimer()
                timer.calc_time(evolve_dt)

    def create_timer(self, show=True):
        from simulators.ursina.entities.timer import Timer
        # 创建一个文本对象来显示计时器的时间
        self.timer = Timer(show)
        return self.timer

    def cosmic_background(self, texture='../textures/cosmic2.jpg'):
        """
        加入宇宙背景
        @param texture:
        @return:
        """
        # Add skybox

        if camera.clip_plane_near >= 0.01:
            sky_scale = 50000
        else:
            sky_scale = 500000 * camera.clip_plane_near

        from ursina import Sky
        sky = Sky(texture=texture, scale=sky_scale)
        Sky.instance = sky
        # sky = SphereSky(texture=texture, scale=sky_scale)
        sky.scale = sky_scale
        camera.sky = sky
        # sky.set_shader_input('texture_scale', Vec2(20, 20))
        # 一定要够大，如果小于 Sky(texture=texture).scale = 50000，宇宙背景就会出现黑色方洞
        if camera.clip_plane_far < sky_scale * 2:
            camera.clip_plane_far = sky_scale * 2

        # texture = load_texture(texture)
        # sky_dome = Entity(model='sky_dome', texture=texture, scale=10000,
        #                   color=color.white,
        #                   position=(0, 0, 0),
        #                   rotation=(0, 0, 0))

    def run(self, dt, **kwargs):
        # 默认非近距离查看
        view_closely = False
        if "view_closely" in kwargs:
            view_closely = kwargs["view_closely"]

        self.show_timer = False
        if "show_timer" in kwargs:
            self.show_timer = kwargs["show_timer"]

        self.timer_enabled = False
        if "timer_enabled" in kwargs:
            self.timer_enabled = kwargs["timer_enabled"]

        show_exit_button = True
        if "show_exit_button" in kwargs:
            show_exit_button = kwargs["show_exit_button"]

        if view_closely:
            # 近距离查看
            if isinstance(view_closely, float):
                if view_closely < 0.001:
                    view_closely = 0.001
                camera.clip_plane_near = view_closely
                if view_closely < 0.01:
                    # camera.fov = 60-0.01/view_closely
                    # camera.fov = 40
                    pass
            else:
                # 设置 camera 的裁剪面和位置
                camera.clip_plane_near = 0.01
        camera.fov = 60

        window.fps_counter.enabled = False
        window.exit_button.enabled = show_exit_button
        # window.editor_ui.enabled = True

        # # 场景加入雾的效果
        # scene.fog_color = color.orange
        # scene.fog_density = 800 * UrsinaConfig.SCALE_FACTOR

        # UrsinaConfig.SCALE_FACTOR = UrsinaConfig.SCALE_FACTOR * math.ceil(0.01 / pow(camera.clip_plane_near,2))

        # interval_fator 能让更新天体运行状态（位置、速度）更精确
        # 设定时间间隔为0.01秒
        self.interval_fator = 0.01
        self.evolve_dt = dt

        # interval 和 last_time 用于检查时间间隔是否已过期
        self.interval = datetime.timedelta(seconds=self.interval_fator)
        self.last_time = datetime.datetime.now() - datetime.timedelta(seconds=2)

        if "show_grid" in kwargs:
            if kwargs["show_grid"]:
                if "grid_scale" in kwargs:
                    grid_scale = kwargs["grid_scale"]
                else:
                    grid_scale = None

                if "grid_position" in kwargs:
                    grid_position = kwargs["grid_position"]
                else:
                    grid_position = None

                WorldGrid(grid_position, grid_scale)

        if "cosmic_bg" in kwargs:
            cosmic_bg = kwargs["cosmic_bg"]
            if cosmic_bg is None:
                # cosmic_bg = '../textures/cosmic1.png'
                # cosmic_bg = '../textures/cosmic2.jpg'
                cosmic_bg = '../textures/cosmic3.jpg'
            if "textures/" in cosmic_bg:
                cosmic_bg = find_file(cosmic_bg)
            else:
                cosmic_bg = find_texture(cosmic_bg)

            if cosmic_bg is not None and os.path.exists(cosmic_bg):
                self.cosmic_background(cosmic_bg)

        if self.show_timer:
            self.timer_enabled = True
            # 创建和显示计时器
            self.create_timer(True)
        elif self.timer_enabled:
            # 创建计时器，但是不显示
            self.create_timer(False)

        # 防止打开中文输入法
        # self.switch_to_english_input_method()
        #     file: 指定音乐文件的路径
        #     loop: 是否循环播放，默认为 True
        #     autoplay: 是否自动播放，默认为 True
        #     volume: 音量大小，取值范围为 0.0 到 1.0，默认为 1.0
        #     pitch: 音调，取值范围为 0.5 到 2.0，默认为 1.0
        #     time: 指定音乐从何处开始播放，单位为秒，默认为 0.0
        #     stop_when_done: 音乐播放完毕后是否停止播放，默认为 True
        if "bg_music" in kwargs:
            bg_music = kwargs["bg_music"]
        elif "background_music" in kwargs:
            bg_music = kwargs["background_music"]
        else:
            bg_music = None

        bg_music = find_file(bg_music)

        if bg_music is None:
            # bg_music = "../sounds/universe_04.mp3"  # 默认背景音乐
            bg_music = "../none"  # 默认没有背景音乐

        if os.path.exists(bg_music):
            audio = Audio(bg_music, pitch=1, loop=True, autoplay=True)
            audio.volume = 0.3

        EditorCamera(ignore_paused=True)

        if self.show_timer or self.timer_enabled:
            UrsinaEvent.on_reset()

        UrsinaEvent.on_ready()

        # ui = UrsinaUI()
        ctl = ControlUI(ControlHandler(), position=(0.6, 0.5))
        ControlUI.current_ui = ctl

        UrsinaEvent.after_ready()

        self.app.run()


if __name__ == '__main__':
    from bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon
    from bodies.body import AU
    from common.consts import SECONDS_PER_DAY

    """
    3个太阳、1个地球
    """
    bodies = [
        Sun(name='太阳1', mass=1.5e30, init_position=[849597870.700, 0, 0], init_velocity=[0, 7.0, 0],
            size_scale=5e1, texture="sun.png"),  # 太阳放大 100 倍
        Sun(name='太阳2', mass=2e30, init_position=[0, 0, 0], init_velocity=[0, -8.0, 0],
            size_scale=5e1, texture="sun.png"),  # 太阳放大 100 倍
        Sun(name='太阳3', mass=2.5e30, init_position=[0, -849597870.700, 0], init_velocity=[18.0, 0, 0],
            size_scale=5e1, texture="sun.png"),  # 太阳放大 100 倍
        Earth(name='地球', init_position=[0, -349597870.700, 0], init_velocity=[15.50, 0, 0],
              size_scale=4e3, texture="earth.png", distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    ]
    # bodies = [
    #
    #     Sun(name='太阳2', mass=1.5e30, init_position=[0, 0, 0], init_velocity=[0, -8.0, 0],
    #         size_scale=5e1, texture="sun.png"),  # 太阳放大 100 倍
    #     Sun(name='太阳2', mass=1.5e30, init_position=[849597870.700, 0, 0], init_velocity=[0, -8.0, 0],
    #         size_scale=5e1, texture="sun.png"),  # 太阳放大 100 倍
    #     Sun(name='太阳2', mass=1.5e30, init_position=[0, -849597870.700, 0], init_velocity=[0, -8.0, 0],
    #         size_scale=5e1, texture="sun.png"),  # 太阳放大 100 倍
    #     Earth(name='地球', mass=5.97237e24, init_position=[0, -349597870.700, 0], init_velocity=[15.50, 0, 0],
    #           size_scale=4e3, texture="earth.png", distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    # ]
    bodies = [
        Sun(size_scale=0.8e2),  # 太阳放大 80 倍
        Mercury(size_scale=4e3, distance_scale=1.3),  # 水星放大 4000 倍，距离放大 1.3 倍
        Venus(size_scale=4e3, distance_scale=1.3),  # 金星放大 4000 倍，距离放大 1.3 倍
        Earth(init_position=[1.12 * AU, 0, 0],
              init_velocity=[0, 29.79, 0], size_scale=4e3, distance_scale=1.3),  # 地球放大 4000 倍，距离放大 1.3 倍
        Moon(init_position=[363104 + 1.12 * AU, 0, 0],
             init_velocity=[-9, 29.79 + 1.023, 0], size_scale=4e3, distance_scale=1.3),
        Mars(size_scale=4e3, distance_scale=1.3),  # 火星放大 4000 倍，距离放大 1.3 倍
        Jupiter(size_scale=0.68e3, distance_scale=0.65),  # 木星放大 680 倍，距离缩小到真实距离的 0.65
        Saturn(size_scale=0.68e3, distance_scale=0.52),  # 土星放大 680 倍，距离缩小到真实距离的 0.52
        Uranus(size_scale=0.8e3, distance_scale=0.36),  # 天王星放大 800 倍，距离缩小到真实距离的 0.36
        Neptune(size_scale=1e3, distance_scale=0.27),  # 海王星放大 1000 倍，距离缩小到真实距离的 0.27
        Pluto(size_scale=10e3, distance_scale=0.23),  # 冥王星放大 10000 倍，距离缩小到真实距离的 0.23(从太阳系的行星中排除)
    ]

    ursina_run(bodies, SECONDS_PER_DAY, position=(AU * 2, AU * 2, AU * 3), show_grid=True)
