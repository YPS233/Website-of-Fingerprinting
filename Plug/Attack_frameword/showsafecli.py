__author__ = 'YPS'
# -*- coding:utf-8 -*-
import sys
import os
import imp
import importlib
from optparse import OptionParser, OptionGroup
from conf.showsafe import *
from lib.exp_module import EXPModule
from sqlhelper import DBHelper
from lib.kwords_module import KEYModule
from lib.exp_http import EXPHttp


class Safecatcli():
    def __init__(self):
        self.exp_module = None
        self.keywords_module = None
        self.httptools = EXPHttp()

    '''
    根据EXP进行测试
    全网测试
    python3 showsafecli.py -m exp_name -n faq_sqlin_exploit -o all 
    单个IP测试
    python3 showsafecli.py -m exp_name -n faq_sqlin_exploit -o single -u xxx.x.xxx.xx
    IP段测试
    python3 showsafecli.py -m exp_name -n faq_sqlin_exploit -o range -startip xxx.xx.xxx.xx -endip xxx.xx.xxx.xxx
    根据关键字进行测试
    python3 showsafecli.py -m flag
    
    '''

    def optionInit(self):
        parser = OptionParser()
        # 通用命令  -m 确定使用脚本测试还是关键字测试  -n EXP模块名字 -u 目标URL或者IP
        parser.add_option('-m', '--module', help="Define the name of module[exp_name/keyword]", dest='module_name')
        parser.add_option('-n', '--name', help="Define the name of poc file", dest='exp_name')
        parser.add_option('-u', '--url', help="Define the target url or ip addr", dest='thost')

        # 指定脚本参数组 -o 测试全域名all或单个目标single或IP段range -s 开始IP -e 结束IP
        exp_module = OptionGroup(parser, 'Exploit module')
        exp_module.add_option('-o', '--option', help="Define scan tye[all/single/range]", dest='option')
        exp_module.add_option('-s', '--startip', help="Define the start ip addr in your range", dest='startip', )
        exp_module.add_option('-e', '--endip', help="Define the end ip addr in your addr", dest='endip')
        parser.add_option_group(exp_module)

        # 指定关键字组 -k 关键字 -q 查询条件 如城市国家限制
        # 目前是载入所有exp进行测试（不完善）
        flag_module = OptionGroup(parser, 'Keyword module')
        flag_module.add_option('-k', '--keyword', help="Define the keyword", dest='keyword')
        # 得到你想要测试的url
        flag_module.add_option('-q', '--query', help="Define the type of domain , use query", dest='query')
        parser.add_option_group(flag_module)

        (option, args) = parser.parse_args()
        return (option, args)

    def loaddir(self):
        for x in os.walk(ROOT_PATH):
            sys.path.append(x[0].replace('\\', '/'))

    def run(self):
        (option, args) = self.optionInit()
        # print((option, args))
        self.loaddir()

        if option.module_name == 'exp_name':
            if option.option == 'all':
                print('全网扫描模式')
                # 根据EXP名字查找模块文件
                fp, pathname, desctiption = imp.find_module(option.exp_name)
                # 加载找到的文件 exp_file为模块文件
                exp_file = imp.load_module(option.exp_name, fp, pathname, desctiption)
                # 从文件初始化为类的对象
                exp_file = exp_file.SafecatExploit()
                # 初始化一个扫描脚本的对象，将要运行的EXP对象作为参数传入
                self.exp_module = EXPModule(exp_file)

            elif option.option == 'single' and option.thost:
                target = self.httptools.get_standard_url(option.thost)
                mod = importlib.import_module(option.exp_name)
                print('[+] Test %s' % option.exp_name)
                # 通过module名字获取module中类的对象
                for name in dir(mod):
                    # dir(mod) 返回mod的属性，方法列表，getattr()获取列表中名字为变量name的那一个属性或方法；这里是取得类名
                    var = getattr(mod, name) # var即为最终获取到的类名
                    try:
                        poc = var(target) # 通过类名初始化类的对象
                    except Exception:
                        pass
                result = poc.run() # 执行类的对象的方法
                db = DBHelper()
                sql = "insert into job_status (url, pocname, result) values('%s','%s','%s')" \
                      % (option.thost, mod.__name__, result)
                db.excute_ddl_sql('showsafe', sql)
        else:
            print('请输入-m确定测试模式')


if __name__ == '__main__':
    cli = Safecatcli()
    cli.run()