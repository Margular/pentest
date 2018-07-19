#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
import argparse
import time
import random
from agent import *

def chinaz(domain):
    regexp = r'''<a href='[^']+?([^']+?)' target=_blank>\1</a>'''
    regexp_next = r'''<a href="javascript:" val="%d" class="item[^"]*?">%d</a>'''
    url = 'http://s.tool.chinaz.com/same?s=%s&page=%d'

    page = 1
    while True:
        if page > 1:
            time.sleep(1)   #防止拒绝访问
        req = urllib.request.Request(url % (domain , page) , headers = {'User-Agent' : random.choice(agent())})
        html = urllib.request.urlopen(req).read().decode('utf-8')  #取得页面
        for site in re.findall(regexp , html):
            yield site
        if re.search(regexp_next % (page+1 , page+1) , html) is None:
            break
        page += 1
    for site in aizhan(domain):
        yield site

def aizhan(domain):
    regexp = r'''<a href="[^']+?([^']+?)/" rel="nofollow" target="_blank">\1</a>'''
    regexp_next = r'''<a href="http://dns.aizhan.com/[^/]+?/%d/">%d</a>'''
    url = 'http://dns.aizhan.com/%s/%d/'

    page = 1
    while True:
        if page > 2:
            time.sleep(1)   #防止拒绝访问
        req = urllib.request.Request(url % (domain , page) , headers = {'User-Agent' : random.choice(agent())})
        try:
            html = urllib.request.urlopen(req).read().decode('utf-8')  #取得页面
        except urllib.error.URLError as e:
            if hasattr(e , 'code'):
                if e.code == 400:
                    break
        for site in re.findall(regexp , html):
            yield site
        if re.search(regexp_next % (page+1 , page+1) , html) is None:
            break
        page += 1

def same_ip(domain):
    sites = []
    for site in chinaz(domain):
        sites.append(site)
    sites = set(sites)  # 去重
    return sites

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '同IP网站查询工具')
    parser.add_argument('domain' , help = '域名或IP')
    args = parser.parse_args()
    for website in same_ip(args.domain):
        print(website)
