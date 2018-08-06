# -*- coding:utf-8 -*-
'''
@author: ChanGeZ
@file: foms.py
@time: 2018/1/28 下午 03:16
'''

from django import forms

class UserForm(forms.Form):
    user = forms.CharField()
    passwd = forms.CharField()