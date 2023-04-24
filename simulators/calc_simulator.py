# -*- coding:utf-8 -*-
# title           :计算运行模拟器（无界面）
# description     :计算运行模拟器（无界面）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# mayavi version  :4.8.1
# ==============================================================================
from simulators.simulator import Simulator
from common.system import System
from simulators.views.body_view import BodyView
from common.singleton import Singleton


class CalcView(BodyView):
    """
    无界面
    """

    def update(self):
        pass

    def appear(self):
        if hasattr(self.body, "torus_stars"):
            # 暂不支持环状小行星群
            return

    def disappear(self):
        pass


class CalcSimulator(Simulator):
    """
    计算运行模拟器（无界面）
    主要用于天体测试数据计算
    """

    def __init__(self, bodies_sys: System):
        super().__init__(bodies_sys, CalcView)

    def run(self, dt, **kwargs):
        on_finished = None
        if "on_finished" in kwargs:
            on_finished = kwargs["on_finished"]

        on_ready = None
        if "on_ready" in kwargs:
            on_ready = kwargs["on_ready"]

        evolve_next = None
        if "evolve_next" in kwargs:
            evolve_next = kwargs["evolve_next"]

        after_evolve = None
        if "after_evolve" in kwargs:
            after_evolve = kwargs["after_evolve"]

        before_evolve = None
        if "before_evolve" in kwargs:
            before_evolve = kwargs["before_evolve"]

        if on_ready is not None:
            on_ready(self)

        if evolve_next is None:
            if before_evolve is not None:
                before_evolve(self)

            self.evolve(dt)

            if after_evolve is not None:
                after_evolve(self)
        else:
            while evolve_next(self):
                if before_evolve is not None:
                    before_evolve(self)

                self.evolve(dt)

                if after_evolve is not None:
                    after_evolve(self)

        if on_finished is not None:
            on_finished(self)


if __name__ == '__main__':
    from sim_scenes.func import calc_run
    from bodies import Sun, Earth
    from common.consts import SECONDS_PER_WEEK

    """
    3个太阳、1个地球
    """
    bodies = [
        Sun(name='太阳1', mass=1.5e30, init_position=[849597870.700, 0, 0], init_velocity=[0, 7.0, 0],
            size_scale=5e1, texture="sun1.jpg"),  # 太阳放大 100 倍
        Sun(name='太阳2', mass=2e30, init_position=[0, 0, 0], init_velocity=[0, -8.0, 0],
            size_scale=5e1, texture="sun2.jpg"),  # 太阳放大 100 倍
        Sun(name='太阳3', mass=2.5e30, init_position=[0, -849597870.700, 0], init_velocity=[18.0, 0, 0],
            size_scale=5e1, texture="sun2.jpg"),  # 太阳放大 100 倍
        Earth(name='地球', init_position=[0, -349597870.700, 0], init_velocity=[15.50, 0, 0],
              size_scale=4e3, distance_scale=1),  # 地球放大 4000 倍，距离保持不变
    ]


    def on_finished(simulator):
        print(simulator)


    def on_ready(simulator):
        print(simulator)


    def after_evolve(simulator):
        print(simulator)


    def before_evolve(simulator):
        print(simulator)


    def evolve_next(simulator):
        if not hasattr(simulator, "loop"):
            simulator.loop = 10
        else:
            simulator.loop -= 1
        print(simulator.bodies_sys.bodies)
        return simulator.loop > 0


    calc_run(bodies, SECONDS_PER_WEEK,
             on_ready=on_ready,
             on_finished=on_finished,
             after_evolve=after_evolve,
             before_evolve=before_evolve,
             evolve_next=evolve_next)
