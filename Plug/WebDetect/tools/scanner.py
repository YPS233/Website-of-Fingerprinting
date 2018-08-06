# -*- coding:utf-8 -*-
import requests
import urllib
import sys, os, socket, time, re

'''
网络扫描类
扫描一个IP网段，指定端口，默认80
如202.206.32.1/24  80端口
'''


class Scanner():
    # 利用socket扫描端口是否开放
    def portScanner(self, ip, port=80):
        server = (ip, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        ret = sock.connect_ex(server)  # 返回0为成功
        if not ret:
            sock.close()
            print('%s:%s is opened...' % (ip, port))
            return True
        else:
            sock.close()
            print('%s:%s NO' % (ip, port))
            return False

    # IP从字符转化为数字IP
    def iptonum(self, ip):
        IP = [int(x) for x in ip.split('.')]
        # print(IP[0] << 24 | IP[1] << 16 | IP[2] << 8 | IP[3])
        # 数字进行二进制移位并相加，得到IP地址的数字
        # 即数字转化为二进制后每8位表示一段
        return IP[0] << 24 | IP[1] << 16 | IP[2] << 8 | IP[3]

    # 数字IP转化为字符串IP
    def numtoip(self, num):
        ip = ['', '', '', '']
        ip[3] = (num & 0xff)
        ip[2] = (num & 0xff00) >> 8
        ip[1] = (num & 0xff0000) >> 16
        ip[0] = (num & 0xff000000) >> 24
        return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])

    def iprange(self, ip1, ip2):
        num1 = self.iptonum(ip1)
        num2 = self.iptonum(ip2)
        tmp = num2 - num1  # 共tmp个IP地址
        return num1, num2, tmp

    def WebScanner(self, startip, endip, port=80):
        ip_list = []
        res = ()
        res = self.iprange(startip, endip)
        if res[2] < 0:
            print('endip must be bigger than startone')
            return None
        else:
            for x in range(int(res[2] + 1)):
                startipnum = self.iptonum(startip)
                startipnum = startipnum + x
                if self.portScanner(self.numtoip(startipnum), port):
                    ip_list.append(self.numtoip(startipnum))
            return ip_list


if __name__ == '__main__':
    S = Scanner()
    print(S.WebScanner('192.168.1.1', '192.168.2.1', 135))
