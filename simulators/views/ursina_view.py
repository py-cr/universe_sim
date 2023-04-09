# -*- coding:utf-8 -*-
# title           :ursina天体视图
# description     :ursina天体视图（天体效果展示用，需要安装 ursina）
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
# pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
from bodies import Body
from simulators.views.body_view import BodyView
from simulators.ursina.entities.planet import Planet
import numpy as np
import math


class UrsinaView(BodyView):
    """
    ursina天体视图（天体效果展示用）
    """

    def __init__(self, body: Body, bodies_system):
        BodyView.__init__(self, body, bodies_system)
        self.velocity = body.velocity

        self.planet = Planet(self)
        body.planet = self.planet

    def update(self):
        """

        @return:
        """
        self.planet.update()

    def appear(self):
        pass

    def disappear(self):
        self.planet.destroy_all()
        self.appeared = False
