# Author: zjun
# Github: https://github.com/bestreder
# Date: 2020-02-23

import requests
import socket
import re
from urllib.parse import urlparse
import argparse
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)

# browser=webdriver.Chrome()

headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}


def get_domain(domain):
    # url转域名
    res = urlparse(domain)
    return res.netloc


def get_seo(domain):
    # 爱站网seo
    azurl = 'https://www.aizhan.com/seo/'
    url = azurl + domain
    browser.get(url)
    browser.refresh()
    html = browser.page_source
    pattern = re.compile(
        '''<li>百度权重：<a id="baidurank_br" target="_blank".*?alt="(.*?)"></a></li>
							<li>移动权重：<a id="baidurank_mbr" target="_blank".*?alt="(.*?)"></a></li>
							<li>360权重：<a id="360_pr" target="_blank".*?alt="(.*?)"></a></li>
							<li>神马：<a id="sm_pr" target="_blank".*?alt="(.*?)"></a></li>
							<li>搜狗：<a id="sogou_pr" target="_blank".*?alt="(.*?)"></a></li>
							<li>谷歌PR：<a id="google_pr" target="_blank".*?alt="(.*?)"></a></li>.*?<li>备案号：<a target="_blank".*?id="icp_icp">(.*?)</a></li>
							<li>性质：<span id="icp_type">(.*?)</span></li>
							<li>名称：<span id="icp_company">(.*?)</span></li>
							<li>审核时间：<span id="icp_passtime">(.*?)</span></li>''', re.S)
    seos = re.findall(pattern, html)
    for seo in seos:
        print('百度权重:{}  移动权重:{}  360权重:{}  神马:{}  搜狗:{}  谷歌PR:{}'.format(
            seo[0], seo[1], seo[2], seo[3], seo[4], seo[5]))
        print('备案号:{}  性质:{}  名称:{}  审核时间:{}'.format(seo[6], seo[7], seo[8],
                                                     seo[9]))


def get_ip(domain):
    # 域名转ip
    try:
        result = socket.getaddrinfo(domain, None)
        ip = result[0][4][0]
        return ip
    except:
        return None


def get_ipaddress(ip):
    # 获取ip定位
    try:
        url = ('https://www.ip.cn/?ip={}'.format(ip))
        r = requests.get(url=url, headers=headers, timeout=3)
        pattern = re.compile(
            'setTimeout.*?所在地理位置：<code>(.*?)</code></p><p>GeoIP: <code>(.*?)</code>',
            re.S)
        address = re.findall(pattern, r.text)
        for add in address:
            print('GeoIP:{}'.format(add[1]))
            print('地理位置:{}'.format(add[0]))
    except:
        pass


def main(domain):
    try:
        print(url.strip())
        if '://' in domain:
            domain = get_domain(domain)
        ip = get_ip(domain)
        print('IP:{}'.format(ip))
        if ip == None:
            get_seo(domain)
        else:
            get_ipaddress(ip)
            get_seo(domain)
    except:
        print('连接失败')
    finally:
        print(' ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The script is Information gathering and SEO query')
    parser.add_argument('-u', '--url', required=False, help='target url')
    parser.add_argument('-f', '--file', required=False, help='target file')
    args = parser.parse_args()
    file = args.file
    url = args.url
    if url == None:
        if file != None:
            with open(file, 'r') as f:
                url_list = f.readlines()
            for url in url_list:
                pool = Pool()
                pool.map(main, (url.strip(), ))
        else:
            print(r'''
 _        __
(_)_ __  / _| ___  ___  ___ __ _ _ __
| | '_ \| |_ / _ \/ __|/ __/ _` | '_ \
| | | | |  _| (_) \__ \ (_| (_| | | | |
|_|_| |_|_|  \___/|___/\___\__,_|_| |_|
			by:zjun
		    www.zjun.info

usage: infoscan.py [-h] [-u URL] [-f FILE]
				''')
    else:
        main(url)
    browser.quit()
