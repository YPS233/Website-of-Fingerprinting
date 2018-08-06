# -*- coding:utf-8 -*-
"""
@author: ChanGeZ
@file: test.py
@time: 2018/2/11 下午 06:23
"""

import json
with open('apps_new.json') as fb:
    apps = json.load(fb)
cat = apps['categories']
for num, cat_name in cat.items():
    # print(131)
    print("%s=item['%s']" % (cat_name.replace(' ','_'), cat_name), end=",")
