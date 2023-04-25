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


class CalcContext(Singleton):
    def __init__(self, simulator):
        self.simulator = simulator
        self.evolve_count = 0
        if not hasattr(self, "_params"):
            # 存放参数字典数据,通过 get_param 获取
            self._params = {}

    def init_param(self, key, value):
        """
        只会初始化一次（除非删除掉）
        @param key:
        @param value:
        @return:
        """
        if key not in self._params:
            self.put_param(key, value)
        return self

    @property
    def bodies(self) -> []:
        return self.simulator.bodies_sys.bodies

    @property
    def system(self) -> System:
        return self.simulator.bodies_sys

    @property
    def params(self):
        return self._params

    def put_param(self, key, data):
        self._params[key] = data
        return self

    def get_param(self, key):
        """
        获取参数值
        @param key:
        @return:
        """
        if self._params is None or len(self._params) == 0:
            return None

        if key not in self._params.keys():
            return None

        return self._params[key]


class CalcSimulator(Simulator):
    """
    计算运行模拟器（无界面）
    主要用于天体测试数据计算
    """

    @staticmethod
    def init():
        if hasattr(CalcSimulator, "on_reset_funcs"):
            return
        # 重启运行的订阅事件
        CalcSimulator.on_reset_funcs = []
        # 运行准备的订阅事件
        CalcSimulator.on_ready_funcs = []
        # 运行结束的订阅事件
        CalcSimulator.on_finished_funcs = []
        # 演变前触发的订阅事件
        CalcSimulator.on_before_evolve_funcs = []
        # 演变后触发的订阅事件
        CalcSimulator.on_after_evolve_funcs = []

    @staticmethod
    def on_before_evolve_subscription(fun):
        CalcSimulator.on_before_evolve_funcs.append(fun)

    @staticmethod
    def on_before_evolve_unsubscription(fun):
        CalcSimulator.on_before_evolve_funcs.remove(fun)

    @staticmethod
    def on_before_evolve(dt, context):
        for f in CalcSimulator.on_before_evolve_funcs:
            f(dt, context)

    @staticmethod
    def on_after_evolve_subscription(fun):
        CalcSimulator.on_after_evolve_funcs.append(fun)

    @staticmethod
    def on_after_evolve_unsubscription(fun):
        CalcSimulator.on_after_evolve_funcs.remove(fun)

    @staticmethod
    def on_after_evolve(dt, context):
        for f in CalcSimulator.on_after_evolve_funcs:
            f(dt, context)

    @staticmethod
    def on_finished_subscription(fun):
        CalcSimulator.on_finished_funcs.append(fun)

    @staticmethod
    def on_finished_unsubscription(fun):
        CalcSimulator.on_finished_funcs.remove(fun)

    @staticmethod
    def on_finished(context):
        for f in CalcSimulator.on_finished_funcs:
            f(context)

    @staticmethod
    def on_reset_subscription(fun):
        CalcSimulator.on_reset_funcs.append(fun)

    @staticmethod
    def on_reset_unsubscription(fun):
        CalcSimulator.on_reset_funcs.remove(fun)

    @staticmethod
    def on_reset(context):
        for f in CalcSimulator.on_reset_funcs:
            f(context)

    @staticmethod
    def on_ready_subscription(fun):
        CalcSimulator.on_ready_funcs.append(fun)

    @staticmethod
    def on_ready_unsubscription(fun):
        CalcSimulator.on_ready_funcs.remove(fun)

    @staticmethod
    def on_ready(context):
        for f in CalcSimulator.on_ready_funcs:
            f(context)

    def __init__(self, bodies_sys: System):
        super().__init__(bodies_sys, CalcView)

    def run(self, dt, **kwargs):
        evolve_next = None
        if "evolve_next" in kwargs:
            evolve_next = kwargs["evolve_next"]

        def on_reset(c):
            c.evolve_count = 0

        CalcSimulator.on_reset_subscription(on_reset)
        context = CalcContext(self)

        CalcSimulator.on_ready(context)

        if evolve_next is None:
            # 至少会执行一遍（如果需要执行多遍，需要实现 evolve_next）
            CalcSimulator.on_before_evolve(dt, context)
            self.evolve(dt)
            context.evolve_count += 1
            CalcSimulator.on_after_evolve(dt, context)
        else:
            while evolve_next(context):
                CalcSimulator.on_before_evolve(dt, context)
                self.evolve(dt)
                context.evolve_count += 1
                CalcSimulator.on_after_evolve(dt, context)

        CalcSimulator.on_finished(context)


CalcSimulator.init()

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


    def evolve_next(context: CalcContext):
        simulator = context.simulator
        print(simulator.bodies_sys.bodies)
        return context.evolve_count < 2


    calc_run(bodies, SECONDS_PER_WEEK,
             evolve_next=evolve_next)
