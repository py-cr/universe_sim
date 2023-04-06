# -*- coding:utf-8 -*-
# title           :ursina天体运行模拟器事件传递
# description     :ursina天体运行模拟器事件传递
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina


class UrsinaEvent:
    """
    ursina天体运行模拟器事件传递
    """

    @staticmethod
    def init():
        if hasattr(UrsinaEvent, "on_reset_funcs"):
            return
        # 重启运行的订阅事件
        UrsinaEvent.on_reset_funcs = []
        # 暂停运行的订阅事件
        UrsinaEvent.on_pause_funcs = []
        # 启动运行的订阅事件
        UrsinaEvent.on_start_funcs = []
        # 运行准备的订阅事件
        UrsinaEvent.on_ready_funcs = []

        # 搜索天体的订阅事件
        UrsinaEvent.on_searching_bodies_funcs = []
        # 应用运行的订阅事件
        UrsinaEvent.on_application_run_callback = []
        # 天体大小发生变化的订阅事件
        UrsinaEvent.on_body_size_changed_callback = []
        # 逐步演变触发的订阅事件
        UrsinaEvent.on_evolving_callback = []
        # 计时器触发的订阅事件
        UrsinaEvent.on_timer_changed_callback = []

    @staticmethod
    def on_body_size_changed_subscription(fun):
        UrsinaEvent.on_body_size_changed_callback.append(fun)

    @staticmethod
    def on_body_size_changed():
        for f in UrsinaEvent.on_body_size_changed_callback:
            f()

    @staticmethod
    def on_timer_changed_subscription(fun):
        UrsinaEvent.on_timer_changed_callback.append(fun)

    @staticmethod
    def on_timer_changed(time_text, time_data):
        for f in UrsinaEvent.on_timer_changed_callback:
            f(time_text, time_data)

    @staticmethod
    def on_evolving_subscription(fun):
        UrsinaEvent.on_evolving_callback.append(fun)

    @staticmethod
    def on_evolving(evolve_dt):
        for f in UrsinaEvent.on_evolving_callback:
            f(evolve_dt)

    @staticmethod
    def on_application_run_callback_subscription(fun):
        UrsinaEvent.on_application_run_callback.append(fun)

    @staticmethod
    def on_searching_bodies_subscription(subscription_name, fun):
        UrsinaEvent.on_searching_bodies_funcs.append((subscription_name, fun))

    @staticmethod
    def on_reset_subscription(fun):
        UrsinaEvent.on_reset_funcs.append(fun)

    @staticmethod
    def on_reset():
        for f in UrsinaEvent.on_reset_funcs:
            f()

    @staticmethod
    def on_ready_subscription(fun):
        UrsinaEvent.on_ready_funcs.append(fun)

    @staticmethod
    def on_ready():
        for f in UrsinaEvent.on_ready_funcs:
            f()

    @staticmethod
    def on_start_subscription(fun):
        UrsinaEvent.on_start_funcs.append(fun)

    @staticmethod
    def on_start():
        for f in UrsinaEvent.on_start_funcs:
            f()

    @staticmethod
    def on_pause_subscription(fun):
        UrsinaEvent.on_pause_funcs.append(fun)

    @staticmethod
    def on_pause():
        for f in UrsinaEvent.on_pause_funcs:
            f()


    @staticmethod
    def on_application_run():
        if len(UrsinaEvent.on_application_run_callback) == 0:
            return
        for f in UrsinaEvent.on_application_run_callback:
            f()
        UrsinaEvent.on_application_run_callback.clear()

    @staticmethod
    def on_searching_bodies(**kwargs):
        results = []
        for subscription_name, fun in UrsinaEvent.on_searching_bodies_funcs:
            results.append((subscription_name, fun(**kwargs)))
        return results


UrsinaEvent.init()
