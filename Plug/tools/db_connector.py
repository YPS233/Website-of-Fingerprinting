# -*- coding:utf-8 -*-
"""
@author: ChanGeZ
@file: db_connector.py
@time: 2018/2/11 下午 05:01
"""

import os
import sys
import django

sys.path.append("E:\python\MyZoomEye")
os.environ['DJANGO_SETTINGs_MODULE'] = 'ShowSafe.settings'

from ShowSafe import settings
django.setup()
from Web.models import WebCategories