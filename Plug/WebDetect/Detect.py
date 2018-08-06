# -*- coding:utf-8 -*-
"""
@author: ChanGeZ
@file: DDetect.py
@time: 2018/2/8 下午 05:08
"""

import json
import requests
import warnings
from bs4 import BeautifulSoup
import re
from urllib import parse

'''
(0)  每个app的名字为 下面整个字典的key
(1)  headers特征   kay: headers
(2)  html特征      key: html
(3)  url特征       key：url
(4)  meta特征      key: meta
(5)  script特征    key: script
(6)  cat分类       key: cat
'''


class Detect:
    def __init__(self, url, verify=True):
        """
        获取url的html，headers
        :param url: str
            目标url
        :param verify: bool
            是否使用SSL
        """
        # 获取基础数据

        self._initurl(url, verify=verify)
        try:
            self.headers.keys()
        except AttributeError:
            raise ValueError("Headers must be a dictionary-like object")
        # 获取script，meta数据
        self._parse_html()

        # 获取指纹数据
        with open('Plug/WebDetect/apps_new.json', 'r') as rules_json:
            self.rules = json.load(rules_json)
        self.categories = self.rules['categories']  # 类别的字典
        self.apps = self.rules['apps']  # apps指纹的字典
        # 校验数据格式正确性
        for name, app in self.apps.items():
            self._prepare_app(app)

    def _initurl(self, url, verify):
        try:
            response = requests.get(url, verify=verify, timeout=2.5)
            self.url = response.url
            self.html = response.text
            self.headers = response.headers
        except Exception as e:
            print(e)
            self.url = url
            self.html = None
            self.headers = None

    def _parse_html(self):
        """
        使用bp分析html，抓取script数据和meta数据
        """
        self.parsed_html = soup = BeautifulSoup(self.html, 'lxml')
        self.scripts = [script['src'] for script in
                        soup.findAll('script', src=True)]
        self.meta = {
            meta['name'].lower():
                meta['content'] for meta in soup.findAll('meta', attrs=dict(name=True, content=True))
        }

    def _prepare_app(self, app):
        """
        校验app中的数据格式正确
        :param app: 指纹数据中的app
        """
        # url，htm，script，implies四项中键对应的值为列表格式
        for key in ['url', 'html', 'script', 'implies']:
            try:
                value = app[key]
            except KeyError:
                app[key] = []
            else:
                if not isinstance(value, list):
                    app[key] = [value]
        # headers，meta两项是否存在，若不存在修改为空字典
        for key in ['headers', 'meta']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}
        # meta的值为字典
        obj = app['meta']
        if not isinstance(obj, dict):
            app['meta'] = {'generator': obj}
        # 确保每一个键都是小写
        for key in ['headers', 'meta']:
            obj = app[key]
            app[key] = {k.lower(): v for k, v in obj.items()}  # 取出每一个键和值，将键小写重新组成字典
        # 初始化正则表达式
        for key in ['url', 'html', 'script']:
            app[key] = [self._prepare_pattern(pattern) for pattern in app[key]]
        # 初始化多个指纹的正则表达式
        for key in ['headers', 'meta']:
            obj = app[key]
            for name, pattern in obj.items():
                obj[name] = self._prepare_pattern(obj[name])

    def _prepare_pattern(self, pattern):
        """
        将正则表达式初始化为re对象
        :param pattern: 要转化的正则表达式
        """
        regex, _, rest = pattern.partition('\\;')  # 将字符串以参数分割，返回三部分，参数前的，全部字符串，参数后的
        try:
            return re.compile(regex, re.I)
        except re.error as e:
            warnings.warn("出错 '{error}' 出正则表达式： {regex}".format(error=e, regex=regex))
            return re.compile(r'(?!x)x')
            # 这是一个不会匹配任何字符的正则表达式，来源:
            # http://stackoverflow.com/a/1845097/413622

    def has_app(self, app):
        """
        指纹识别，值针对某一app的每一项，顺序是从低难度匹配到高难度匹配
        调用时使用遍历
        """
        # url识别
        for regex in app['url']:
            if regex.search(self.url):
                return True

        # headers识别
        for name, regex in app['headers'].items():
            if name in self.headers:
                content = self.headers[name]
                if regex.search(content):
                    return True

        # script识别
        for regex in app['script']:
            for script in self.scripts:
                if regex.search(script):
                    return True

        # meta识别
        for name, regex in app['meta'].items():
            if name in self.meta:
                content = self.meta[name]
                if regex.search(content):
                    return True

        # html识别
        for regex in app['html']:
            if regex.search(self.html):
                return True

    def get_implied_apps(self, detected_apps):
        """
        根据已经识别出的app，从json数据中获取使用的其他app
        :param detected_apps: 已经识别出的app  type为set即集合，使用集合目的是去重
        """
        _implied_apps = set()  # 集合

        def _get_implied_apps(apps):
            for app in apps:
                try:
                    _implied_apps.update(set(self.apps[app]['implies']))
                except KeyError:
                    pass
            return _implied_apps

        implied_apps = _get_implied_apps(detected_apps)
        all_implied_appd = set()
        # 两层调用，查出所使用的所有app
        while not all_implied_appd.issuperset(implied_apps):
            all_implied_appd.update(implied_apps)
            implied_apps = _get_implied_apps(all_implied_appd)

        return all_implied_appd

    def get_categories(self, app_name):
        """
        获取一个app的类别列表
        :param app_name: app名称
        :return: app类别列表
        """
        cat_nums = self.apps.get(app_name, {}).get("cats", [])  # get函数的参数：键名，如果不存在返回的默认值
        cat_names = [self.categories.get("%s" % cat_num, "") for cat_num in cat_nums]

        return cat_names

    def analyze(self):
        """
        获取web页面使用的所有app
        :return:
        """
        detected_apps = set()
        for app_name, app in self.apps.items():
            if self.has_app(app):
                detected_apps.add(app_name)

        # 通过探测到的app，反查json指纹数据，获取比如某cms使用的其他app，并与探测到的app取并集，然后去重
        detected_apps |= self.get_implied_apps(detected_apps)

        return detected_apps

    def analyze_with_categorise(self):
        detected_apps = self.analyze()
        categorised_apps = {}

        for app_name in detected_apps:
            cat_names = self.get_categories(app_name)
            categorised_apps[app_name] = {"categories": cat_names}

        return categorised_apps

    def getlastchar(self, raw, ch):
        sort_list = []
        count = 0
        for x in raw:
            if x == ch:
                sort_list.append(count)
            count += 1
        return sort_list


if __name__ == '__main__':
    detect = Detect('http://www.renyu.net')
    print(detect.analyze())
    print(detect.analyze_with_categorise())
