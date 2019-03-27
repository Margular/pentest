#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import socks
import socket
import urllib.request

def change_proxy(proxy = None):
    if proxy is None:
        with open('proxy.json' , 'r') as f:
            proxies = eval(f.read())
            proxy = random.choice(proxies)

    protocol = proxy['protocol'].lower()
    ip = proxy['ip']
    port = int(proxy['port'])

    #安装代理
    if protocol in [ 'socks4' , 'socks5' ]:
        socks.set_default_proxy(socks.SOCKS4 if protocol == 'socks4' else socks.SOCKS5 , ip , port)
        socket.socket = socks.socksocket
    elif protocol in [ 'http' , 'https' ]: 
        proxy_support = urllib.request.ProxyHandler({protocol : '%s:%d' % (ip , port)})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
    else:
        raise ValueError('Unknown proxy type %s about %s:%d' % (protocol , ip , port))
    return (protocol , '%s:%d' % (ip , port))
