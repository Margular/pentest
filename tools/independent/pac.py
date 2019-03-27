#!/usr/bin/env python3

HTTP = []
HTTPS = []

with open('proxy.json' , 'r') as f:
    proxies = eval(f.read())
    for proxy in proxies:
        if proxy['protocol'] == 'HTTP':
            HTTP.append(proxy['ip'] + ':' + proxy['port'])
        elif proxy['protocol']  == 'HTTPS':
            HTTPS.append(proxy['ip'] + ':' + proxy['port'])

with open('pac.pac' , 'w') as f:
    f.write(r'''function FindProxyForURL(url , host)
{
    if (url.indexOf('http://') == 0)
        return randomHttp();
    else if (url.indexOf('https://') == 0)
        return randomHttps();
    else
        return 'DIRECT';
}

function randomHttp()
{
    switch (Math.floor(Math.random()*''')
    f.write(str(len(HTTP)))
    f.write(r'''))
    {
    ''')
    for count in range(0,len(HTTP)):
        f.write('\tcase %d:\n' % count)
        f.write('\t\t\treturn ''')
        f.write('"PROXY %s";' % HTTP[count])
        f.write(r'''
            break;
    ''')
    f.write('}\n}\n')

    f.write(r'''
function randomHttps()
{
    switch (Math.floor(Math.random()*''')
    f.write(str(len(HTTPS)))
    f.write(r'''))
    {
    ''')
    for count in range(0,len(HTTPS)):
        f.write('\tcase %d:\n' % count)
        f.write('\t\t\treturn ''')
        f.write('"PROXY %s";' % HTTPS[count])
        f.write(r'''
            break;
    ''')
    f.write('}\n}')

