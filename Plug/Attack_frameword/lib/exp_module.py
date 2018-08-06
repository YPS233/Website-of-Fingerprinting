__author__ = 'YPS'
import sys

# -*- coding:utf-8 -*-
# 指定攻击脚本模块
from conf.showsafe import *

sys.path.append(ROOT_PATH + '/lib')
from sqlhelper import DBHelper
from exp_http import EXPHttp
from elasticsearch import Elasticsearch
import time

file_name = REPORT_FOLD + str(time.time()) + '.cat'


class EXPModule():
    def __init__(self, exploit_file):
        global file_name
        self.exp = exploit_file
        # self.es = Elasticsearch('127.0.0.1:9200')
        self.file = open(file_name, 'a')
        self.file.write('domain_list\t\t\tattack_results\n')
        self.httptools = EXPHttp()

    # 根据exp进行全网扫描，并生成报告
    # def scanALL(self):
    #     global file_name
    #     # 数据库记录
    #     db = DBHelper()
    #     sql = "insert into job_status(status,path) values(%d,'%s')" % (0, file_name)
    #     db.excute_ddl_sql('safe_jobs', sql)
    #     # 获取全部的域名列表
    #     domain_list = []
    #     query = {
    #         'query': {
    #             'match_all': {}
    #         },
    #         '_source': ['domain']
    #     }
    #     res = self.es.search(body=query, index='showsafe', doc_type='web', size=1000000)
    #     for x in res['hits']['hits']:
    #         domain_list.append(x['source_']['domain'])
    #
    #     # 开始载入exp扫描并写入记录文件
    #     # print('[+]Start scanning in mode all, please wait...')
    #     print('[+]开始全局扫描，请稍后....')
    #     content = ''
    #     for url in domain_list:
    #         # 直接调用exp脚本，有返回值则成功无则失败
    #         res = self.exp.exploit(url)
    #         if not res:
    #             record = '%s\t\t\tFailed\n' % url
    #             content += record
    #         else:
    #             record = '%s\t\t\t%s\n' % (url, str(res))
    #             content += record
    #         self.file.write(record)
    #     # 任务完成，写入数据库
    #     sql = "update job_status set status=%d, content='%s' where id=(select tmp.id from (select id from job_status order by id desc limit 1)tmp)" % (
    #         1, content)
    #     print(sql)
    #     db.excute_ddl_sql('safe_jobs', sql)
    #     self.file.close()

    # 根据exp进行单个主机扫描，不用生成报告，直接打印
    def scanOneHost(self, target):
        # 数据库记录
        content = ''
        db = DBHelper()
        sql = "insert into job_status (status, path) values(%d, '%s')" % (0, file_name)
        db.excute_ddl_sql('safe_jobs', sql)

        # print('[+]Start scanning in mode single...')
        print('[+]开始单个主机扫描，请稍后....')
        res = self.exp.exploit(target)
        if not res:
            print('%s Exploit Failed:Unknown' % target)
            content += '%s\tExploit\tFailed:Unknown' % target
        else:
            print('Exploit Success:%s\t\t%s' % ('x', str(res)))
            content = '%sExploit\tSuccess:%s\t\t%s' % (target, 'x', str(res))

        content = content.replace('\n', ' ')
        # 直接先查询本表再更新在mysql会报错，只能在加一层刷新 http://blog.csdn.net/z_youarethebest/article/details/53785487
        sql = "update job_status set status=%d, content='%s' where id=(select tmp.id from (select id from job_status order by id desc limit 1)tmp)" % (
            1, content)
        print(sql)
        db.excute_ddl_sql('safe_jobs', sql)

    # 根据IP段扫描
    # def scanOneRange(self, startip, endip):
    #     tmp_list = []
    #     ip_list = []
    #     domain_list = []
    #     db = DBHelper()
    #     sql = "insert into job_status (status, path) values(%d, '%s')" % (0, file_name)
    #     db.excute_ddl_sql('safe_jobs', sql)
    #     print('[+]开始IP段扫描扫描，请稍后....')
    #     myscanner = Scanner()
    #     ipreverse = IPReverse()
    #     ip_list = myscanner.WebScanner(startip, endip)
    #     for x in ip_list:
    #         tmp_list = ipreverse.getDomains(x)
    #         if tmp_list == None:
    #             continue
    #         domain_list.extend(tmp_list)
    #
    #     content = ''
    #     for url in domain_list:
    #         res = self.exp.exploit(url)
    #         if not res:
    #             record = 'Exploit Failed:Unknown'
    #             content += record
    #         else:
    #             record = 'Exploit Success:%s\t\t%s' % (url, str(res))
    #             content += record
    #         self.file.write(record)
    #     sql = "update job_status set status=%d, content='%s' where id = (select tmp.id from (select id from job_status order by id desc limit 1)tmp)" % (
    #         1, content)
    #     print(sql)
    #     db.excute_ddl_sql('safe_jobs', sql)
    #     self.file.close()
