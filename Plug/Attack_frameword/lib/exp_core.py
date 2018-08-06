__author__ = 'YPS'
# -*- coding:utf-8 -*-
# 攻击脚本的抽象类，限制编写规则

import urllib
import requests


class ExploitCore():
    def initialize(self, info={}):
        return info

    def exploit(self):
        pass

    def pocTest(self):
        pass
