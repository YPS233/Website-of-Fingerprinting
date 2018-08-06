__author__ = 'YPS'
# -*- coding:utf-8 -*-

# 获取标准格式URL
import urllib


class EXPHttp():
    def __init__(self):
        pass

    # 在字符串中找到ch字符的下标列表
    def getlastchar(self, raw, ch):
        sort_list = []
        count = 0
        for x in raw:
            if x == ch:
                sort_list.append(count)
            count += 1
        return sort_list

    # 获取标准格式的URL：http://xxx,加上后面的目录
    def get_standard_url(self, url, data=None):
        # 判断传入的url是否为http开头
        co_list = self.getlastchar(url, r'/')
        if len(co_list) > 3:
            url = url[:co_list[3]]
        if url.count('http') != 0:
            if data:
                if url[-1] == '/':  # http://www.xxxx.com/
                    url = '{0}{1}'.format(url, urllib.parse.quote(data, "?@`[]*,+()/'&=!_%"))
                else:  # http://www.xxxx.com
                    url = '{0}{1}'.format(url, urllib.parse.quote(data, "?@`[]*,+()/'&=!_%"))
            else:
                if url[-1] == '/':  # http://www.xxxx.com/
                    url = '{0}'.format(url)
                else:  # http://www.xxxx.com
                    url = '{0}/'.format(url)
        else:
            if data:
                if url[-1] == '/':  # www.xxxx.com/club/
                    url = 'http://{0}{1}'.format(url, urllib.parse.quote(data, "?@`[]*,+()/'&=!_%"))
                else:  # www.xxxx.com/club
                    url = 'http://{0}{1}'.format(url, urllib.parse.quote(data, "?@`[]*,+()/'&=!_%"))
            else:
                if url[-1] == '/':  # www.xxxx.com/
                    url = 'http://{0}'.format(url)
                else:  # www.xxxx.com
                    url = 'http://{0}/'.format(url)
        return url

    def login(self, param):
        pass


if __name__ == '__main__':
    test = EXPHttp()
    print(test.get_standard_url('www.discuz.net'))