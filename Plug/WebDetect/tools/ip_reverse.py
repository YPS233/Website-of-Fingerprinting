# -*- coding:utf-8 -*-
import requests
import socket
from bs4 import BeautifulSoup

# 通过dns.aizhan.com来反查域名

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari'}


class IPReverse():
    def getDomains(self, ip):
        res = requests.get('http://dns.aizhan.com/' + ip + '/')
        bs = BeautifulSoup(res.content, 'lxml')
        table = bs.find_all('table')
        finded = table[0].find_all('a', rel='nofollow', target='_blank')
        # finded = bs.find_all('a', rel='nofollow', target='_blank')
        doman_lists = []
        for x in finded:
            doman_lists.append(x.string)
        return doman_lists

    def getDomainbysocket(self, ip):
        result = socket.gethostbyaddr(ip)
        return result


if __name__ == '__main__':
    ipre = IPReverse()
    doman_list = ipre.getDomainbysocket('216.8.63.226')
    print(doman_list)
