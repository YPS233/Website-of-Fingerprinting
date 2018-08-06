__author__ = 'YPS'
# -*- coding:utf-8 -*-
# 指定关键字模块
import time
import sys
import os
import imp
from sqlhelper import DBHelper
from exp_http import EXPHttp
from conf.showsafe import *
from elasticsearch import Elasticsearch

file_name = REPORT_FOLD + str(time.time()) + '.cat'


class KEYModule():
    def __init__(self, flag):
        global file_name
        self.es = Elasticsearch('127.0.0.1:9200')
        self.flag = flag
        self.file = open(file_name, 'a')
        self.httptools = EXPHttp()

    # 载入相应模块的exp对象,导入目录下的EXP文件,将所有EXP文件转化为类的对象，并返回
    def loadExp(self):
        expfile_list = []
        expobj_list = []
        path = '%s/discuz/%s' % (ROOT_PATH, self.flag)
        sys.path.append(path)
        print(path, ROOT_PATH)
        '''
        os.walk 返回三个返回值
        dirpath 是一个string，代表目录的路径，
        dirnames 是一个list，包含了dirpath下所有子目录的名字。
        filenames 是一个list，包含了非目录文件的名字(带后缀)。
        '''
        for x in os.walk(path):
            for y in x[2]:
                if str(y).endswith('pyc') or str(y).startswith('__init__'):
                    continue
                expfile_list.append(str(y).replace('.py', ''))
        for x in expfile_list:
            fp, pathname, description = imp.find_module(x)
            obj = imp.load_module(x, fp, pathname, description)
            expfile_list.append(obj.ShowsafaExploit())
        return expobj_list

    # 语法解析功能 把输入的攻击命令转为查询所用的DSL语言
    def queryParser(self, query):
        tmp = query.split(' ')
        met = []
        query_dice = {}
        res_list = []
        for x in tmp:
            if x.count(":") == 0:
                res_list.append(x)
            else:
                x = x.replace('+', ' ')
                meta = x.aplit(':')
                res_list.append({meta[0]: meta[1]})
        should_list = []
        must_ist = []
        tmp = []
        for x in res_list:
            if str(x).count(':'):
                tmp = [
                    {'match': {'ip': x}},
                    {'match': {'country': x}},
                    {'match': {'domain': x}},
                    {'match': {'ip': x}},
                    {'match': {'serverinfo': x}},
                    {'match': {'flag': x}},
                    {'match': {'http_response': x}}
                ]
                should_list.extend(tmp)
            else:
                must_ist.append({'match': x})

        query_dsl = {
            'query': {
                'bool': {
                    'should': should_list,
                    'must': must_ist
                }
            },
            '_source': ['domain']
        }
        return query_dsl

    # 根据用户搜索进行exp
    def scanByQuery(self, query):
        content = ''
        # 数据库记录
        db = DBHelper()
        sql = "insert into job_status (status, path) valuse(%d, '%s')" % (0, file_name)
        db.excute_ddl_sql('safe_jobs', sql)

        # 获取所有的EXP对象
        self.exp_list = self.loadExp()
        # 生成报告头
        self.file.write('domain\t\t\tattack_results\n')

        query_dsl = self.queryParser(query)
        query_res = self.es.search(body=query_dsl, index='showsafe', doc_type='web', size=100000)
        domain_list = [x['_source']['domain'] for x in query_res['hits']['hits']]
        for target in domain_list:
            target = self.httptools.get_standard_url(target)
            print('[+]TargetHOST:%s' % target)
            for obj in self.exp_list:
                res = obj.expoit(target)
                if not res:
                    record = '%s\t\t\tFailed\n' % target
                    content += record
                    print(record)
                else:
                    record = '%s\t\t\t%s\n' % target
                    content += record
                    print(record)
                self.file.write(record)
        content = content.replace('\n', ' ')
        sql = "update job_status set status=%d,content='%s' where id =(select tmp.id from (select id from job_status order by id desc limit 1)tmp)" % (
        1, content)
        print(sql)
        db.excute_ddl_sql("safe_jobs", sql)
        self.file.close()

    # 用所有exp攻击一个域名
    def scanByDomain(self, domain):
        # 数据库记录
        content = ''
        db = DBHelper()
        sql = "insert into job_status (status, path) valuse(%d, '%s')" % (0, file_name)
        db.excute_ddl_sql('safe_jobs', sql)

        # 生成报告头
        self.exp_list = self.loadExp()
        self.file.write('domain\t\t\tattack_results\n')

        domain = self.httptools.get_standard_url(domain)
        for obj in self.exp_list:
            res = obj.expoit(domain)
            if not res:
                print('%s Exploit Failed:Unknow' % domain)
                content += '%s\tExploit\tFailed:Unknow' % domain
            else:
                print('Exploit Success:%s' % str(res))
                content += '%sExploit\tSuccess:%s' % (domain, str(res))
        # 完成后修改数据库，可添加一项时间列，记录任务开始时间，任务完成后查找当前开始时间的行 状态修改为完成
        sql = "update job_status set status=%d,content='%s' where id=(select tmp.id from (select id from job_status order by id desc limit 1)tmp)" % (
        1, content)
        print(sql)
        db.excute_ddl_sql('safe_jobs, sql')


if __name__ == '__main__':
    a = KEYModule('discuz')
    print(a.loadExp())

    print(STATIC_PATH)
