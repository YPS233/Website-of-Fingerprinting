# -*- coding:utf-8 -*-
import os
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from Web.models import *
from ShowSafe.settings import ATTACK_CLI_PATH
from Plug.Db.sqlhelper import DBHelper
from Plug.WebDetect.Detect import Detect
from Plug.tools.db_connector import WebCategories
import json
import time
import os
import re
from Web.foms import UserForm


# Create your views here.

# 主页面显示
def index(request):
    print(request.user.has_perm("polls.use_attack"))
    if request.user.is_authenticated():
        return render(request, 'indexl.html')
    else:
        return render(request, 'index.html')


# 用户登录
def account_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # print('----%s %s----' % username, password)
    user = auth.authenticate(username=username, password=password)
    print(user)
    if username == "" and password == "":
        return render(request, 'index.html', {'login_info': '用户名或密码为空'})
    elif user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/detect/')
    elif username and password:
        return render(request, 'index.html', {'login_info': '密码不正确'})
    else:
        return render(request, 'index.html', {'login_info': '未知问题'})


'''
用户注册:使用系统自动的User对象(username,password,email)
权限控制:使用is_staff(是否有网站管理权限)和is_supperuer(是否有超级管理员权限)
使用攻击模块权限？
'''


# res = '/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/'


def account_register(request):
    # 注册条件
    if 'username' in request.POST and 'password' in request.POST and 'email' in request.POST:
        condition = True
    else:
        condition = False
    if condition:
        # 判断数据
        # 两次密码不同
        if request.POST['password'] != request.POST['repassword']:
            return render(request, 'register.html', {'regis_info': '两次输入的密码不同'})
        # 用户名已经存
        elif User.objects.filter(username=request.POST['username']):
            return render(request, 'register.html', {'regis_info': '此用户名已经被注册'})
        # 邮箱格式不正确
        elif re.match(r'.+@\w+\.\w+', request.POST['email']) is None:
            return render(request, 'register.html', {'regis_info': '邮箱格式错误'})
        # 开始注册
        else:
            user = User(username=request.POST['username'], email=request.POST['email'], )
            user.set_password(request.POST['password'])
            user.save()
            return render(request, 'index.html', {'regis_info': '注册成功！请登录'})
    else:
        # 填写内容不完整
        return render(request, 'index.html')


# 用户退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


def getlastchar(raw, ch):
    # 判断raw中有多少个ch，在第几位
    sort_list = []
    count = 0
    for x in raw:
        if x == ch:
            sort_list.append(count)
        count += 1
    return sort_list

# https://www.52pojie.cn/
# url标准化
def get_standard_url(url):
    # 判断传入的url是否为http开头
    co_list = getlastchar(url, r'/')
    if len(co_list) > 3:
        url = url[:co_list[3]]
    if url.count('https') != 0:
        if url[-1] == '/':  # http://www.xxxx.com/
            url = '{0}'.format(url)
        else:  # http://www.xxxx.com
            url = '{0}/'.format(url)
    elif url.count('http') != 0:
        if url[-1] == '/':  # http://www.xxxx.com/
            url = '{0}'.format(url)
        else:  # http://www.xxxx.com
            url = '{0}/'.format(url)
    else:
        if url[-1] == '/':  # www.xxxx.com/
            url = 'http://{0}'.format(url)
        else:  # www.xxxx.com
            url = 'http://{0}/'.format(url)
    return url


# 搜索主页面
def detect(request):
    # 检查是否登录
    if request.user.is_authenticated():
        if 'q' not in request.GET:
            return render(request, 'detect.html', {'user': request.user})
        else:
            url = get_standard_url(request.GET['q'])
            print(url)
            db = DBHelper()
            # 检查是否为已经识别过的URL
            res = db.excute_dql_sql('showsafe', "select * from web_Appstore where url='%s'" % url)
            if res:
                # 已经识别过的直接将缓存结果返回前端
                result = eval(res[2])
            else:
                # 指纹识别
                detect = Detect(url)
                result = detect.analyze_with_categorise()
                # 结果保存
                obj = Appstore(url=url, finger=result, user=request.user)
                obj.save()

            # 处理返回数据
            column1 = [['url']]
            column2 = [[url]]
            for app, catt in result.items():
                if catt['categories'] != []:
                    column1.append([catt['categories'][0]])
                    column2.append([app])
            result1 = [column1, column2]
            print(result1)
            return render(request, 'result.html', {'user': request.user, 'result': result1})
    else:
        # 没有登录
        print(3)
        return render(request, 'index.html')


def attack_module(request):
    path = ''
    # 如果用户已经登录
    if request.user.is_authenticated():
        # if not request.user.has_perm("")
        if 'cmd' not in request.POST:
            return render(request, 'attack.html', {'user': request.user})
        else:
            # 执行命令
            db = DBHelper()
            url = get_standard_url(request.POST['cmd'])
            # 判断数据库中是否已经次网站的测试结果记录
            reste = db.excute_dql_sql('showsafe', "select * from job_status where url='%s'" % url, mode='mu')
            if not reste:
                BASE_PATH = 'E:/python/MyZoomEye/Plug/Attack_frameword/poc'
                # 判断数据中是否有次网站的指纹记录
                res = db.excute_dql_sql('showsafe', "select * from web_Appstore where url='%s'" % url)
                if res:
                    result = eval(res[2])  # 可能会出现问题
                else:
                    detect = Detect(url)
                    result = detect.analyze_with_categorise()
                    # 结果保存
                    obj = Appstore(url=url, finger=result, user=request.user)
                    obj.save()

                # 根据result获取poc_name,需要的参数是包名.类名，如wordpress.wordpress_admin_ajax_filedownload
                pocpath = []
                for app_name, cat in result.items():
                    if cat['categories'] != []:
                        POC_PATH = '{0}/{1}/{2}/'.format(BASE_PATH, cat['categories'][0], app_name)
                        POC_PATH = POC_PATH.replace(' ', '')
                        if os.path.exists(POC_PATH):
                            for filename in os.listdir(POC_PATH):
                                if filename != '__init__.py' and filename.endswith('.py'):
                                    mod_name = filename.split('.')[0]
                                    argv = '{0}.{1}'.format(app_name.lower(), mod_name)
                                    pocpath.append(argv)
                        else:
                            continue
                # 选择测试及演示选择的poc，根据路径加载，保存结果，显示结果
                if pocpath == []:
                    # 不存在相应poc，请人工测试
                    resre = 'nopoc'
                else:
                    # 执行 python3 E:/python/MyZoomEye/Plug/Attack_frameword/showsafecli.py -m exp_name -o single -n POC_name -u xxx
                    cmds = []
                    for x in range(len(pocpath)):
                        cmd = 'python3 %s -m exp_name -o single -n %s -u %s' % (
                            ATTACK_CLI_PATH, pocpath[x], url)
                        cmds.append(cmd)
                        os.system(cmd)

                    resre = db.excute_dql_sql(
                        'showsafe', "select * from job_status where url='%s'" % url, mode='mu')


            else:
                resre = reste
        print(resre)
        return render(request, 'attack.html', {'user': request.user, 'results': resre, 'download_path': path})
    else:
        # 没有登录
        return render(request, 'index.html')
