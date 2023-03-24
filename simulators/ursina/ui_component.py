# -*- coding:utf-8 -*-
# title           :ursina UI组件
# description     :ursina UI组件
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from ursina import Ursina, window, Entity, Grid, Mesh, camera, Text, application, color, mouse, Vec2, Vec3, \
    load_texture, held_keys, Button, Tooltip
from ursina.prefabs.first_person_controller import FirstPersonController
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import WindowPanel, InputField, Button, Slider, ButtonGroup
from simulators.ursina.ursina_config import UrsinaConfig


class UiSlider(Slider):
    """

    """
    def __init__(self, text, min=0.01, max=3, step=.01, default=1):
        # Text.default_font = 'msyhl.ttc'  # 'simsun.ttc'
        super().__init__(text=text,
                         height=Text.size,
                         y=-.6,
                         step=step,
                         min=min,
                         max=max,
                         default=default,
                         color=color.rgba(0.0, 0.0, 0.0, 0.5),
                         ignore_paused=False,
                         dynamic=True)
        # self.label.scale *= 8/10
        self.label.font = UrsinaConfig.CN_FONT
        # self.knob.text_entity.font = ""
        # self.knob.text_entity.scale *= 8/10
        # self.height *= 8/10


class SwithButton(ButtonGroup):
    """

    """
    def __init__(self, options, default, tooltips=None):
        super().__init__(options, min_selection=1, default=default,
                         selected_color=color.rgba(0.1, 0.6, 0.1, 1.0), ignore_paused=True,
                         color=color.rgba(0.0, 0.0, 0.0, 0.5))
        # self.label.scale = 0.8
        # self.label.font = UrsinaConfig.CN_FONT
        for i, button in enumerate(self.buttons):
            button.text_entity.font = UrsinaConfig.CN_FONT
            if tooltips is not None:
                if len(tooltips) > i:
                    tooltip = Tooltip(tooltips[i])
                    tooltip.font = UrsinaConfig.CN_FONT
                    button.tooltip = tooltip
        self.x = -0.5


class Buttons(ButtonGroup):
    """

    """
    def __init__(self, options, default=None, tooltips=None):
        min_selection = len(options)
        super().__init__(options, min_selection=1, default=default,
                         color=color.rgba(0.1, 0.6, 0.1, 1.0), ignore_paused=True,
                         selected_color=color.rgba(0.0, 0.0, 0.0, 0.5))
        # self.label.scale = 0.8
        # self.label.font = UrsinaConfig.CN_FONT\
        for i, button in enumerate(self.buttons):
            button.text_entity.font = UrsinaConfig.CN_FONT

            # button.scale_x = 2
            if tooltips is not None:
                if len(tooltips) > i:
                    tooltip = Tooltip(tooltips[i])
                    tooltip.font = UrsinaConfig.CN_FONT
                    button.tooltip = tooltip
        self.x = -0.5


class UiButton(Button):
    """

    """
    def __init__(self, text, on_click):
        super(UiButton, self).__init__(text=text, origin=(0, 0), y=2,
                                       on_click=on_click, color=color.rgba(0.0, 0.0, 0.0, 0.5),
                                       ignore_paused=False)
        self.text_entity.font = UrsinaConfig.CN_FONT
