#!/usr/lib/env python2.7
#coding: utf-8
#author: cp(Cuiping)

import os
import requests
import socket
import re
import pandas as pd
from bs4 import BeautifulSoup
import json

class GetIpProxy(object):
    def __init__(self):
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
#        Cookie: _free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWM4ODVjMzU5NTRhNzU1YzI4MzM1YzEzMWEyNzk1MjIyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMW9zZUVHV3l2dlg2SThpTE9iSElpWCtOS0FHR2VvNkRmZGxLNHR1S3pJTGc9BjsARg%3D%3D--144fda6f7b67c36c1592d1be932ac53aaf54dce0; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1523417201; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1523424432
        #'Host': 'www.xicidaili.com',
        #'If-None-Match': 'W/"1252a773037f947f34adeb1cb8f2accd"',
        #'Referer': 'http://www.xicidaili.com/',
        #'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
    def fetch_xici_free(self, st):
        page_num = 2
        proxies_list = []
        headers = self.headers.copy()
        headers['Host'] = 'www.xicidaili.com'
        headers['Referer'] = 'http://www.xicidaili.com'
        headers['Upgrade-Insecure-Requests'] = '1'
        for i in range(1, page_num):
            #print i
            url = 'http://www.xicidaili.com/'+ str(st) + '/' + str(i)
            print url
            resp = requests.get(url, headers=headers)
            #print resp.content
            soup = BeautifulSoup(resp.content, 'html.parser')
            ips = soup.findAll('tr')
            ip_list = []
            for index in range(1, len(ips)):
                info = {}
                ip = ips[index]
                #print ip
                tds = ip.findAll('td')
                #print tds
                #print len(tds)
                #print type(tds)
                #print tds[1]
                #print dir(tds[1])
                #print type(tds[1])
                #print tds[1].contents[:]
                ip_address = tds[1].contents[0]
                port = tds[2].contents[0]
                protocol_type = tds[5].contents[0]
                info['Address'] = ip_address + ':' + str(port)
                #info['port'] = port
                info['Type'] = protocol_type
                ip_list.append(info)

            proxy_info = pd.DataFrame(ip_list)
            proxies_list.append(proxy_info)

        proxies_df = pd.concat(proxies_list)
#        proxies_df.to_csv('./first_proxies.csv', index=False)
        return proxies_df

    def fetch_xdaili_free(self):
        proxies_list = []
        headers = self.headers.copy()
        headers['Host'] = 'www.xdaili.cn'
        headers['Referer'] = 'http://www.xdaili.cn/freeproxy'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        url = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
        try:
            resp = requests.get(url, headers=headers)
            if int(resp.status_code) == 200:
                try:
                    info = json.loads(resp.content)
                except Exception, e:
                    print e
                    print resp.content
                else:
                    if int(info['ERRORCODE']) == 0:
                        ips = info['RESULT']['rows']
                        #print ips
                        if isinstance(ips, list):
                            #ips_list = []
                            for item in ips:
                                ip = {}
                                ip['Address'] = item['ip'] + ':' + item['port']
                                ip['Type'] = item['type']
                                proxies_list.append(ip)
            else:
                print 'failed to fetch from xdaili'
        except Exception, e:
            print e
            print 'failed to fetch from xdaili'
            return None
        else:
            proxies = pd.DataFrame(proxies_list)
            return proxies
                            
    def fetch_xdaili_fee(self):
        proxies_list = []
        try:
            #url = 'http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20179268842LI0gdt/d0c3c34bf83211e6942200163e1a31c0?returnType=2'
            #url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=199f073d3f0246698cd2a4e3a9fdfe95&orderno=YZ20179267433YBhYdh&returnType=2&count=15'
            #url = 'http://api.xdaili.cn/xdaili-api//newExclusive/getIp?spiderId=199f073d3f0246698cd2a4e3a9fdfe95&orderno=MF20179297691biR1yS&returnType=2&count=1&machineArea='
            #url = 'http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=199f073d3f0246698cd2a4e3a9fdfe95&returnType=2&count=1'
            url = 'http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=199f073d3f0246698cd2a4e3a9fdfe95&returnType=2&count=1'
            res = requests.get(url = url)
            print res.status_code
            #print res.content
            if int(res.status_code) == 200:
                print res.text
                print res.content
                j = json.loads(res.text)
                if int(j['ERRORCODE']) == 0:
                    if isinstance(j['RESULT'], list):
                        for i in j['RESULT']:
                            ip = {}
                            ip['Address'] = i['ip'] + ':' + i['port']
                            ip['Type'] = 'HTTP/HTTPS'
                            proxies_list.append(ip)
                            #ip = i['ip']
                            #port = i['port']
                            #proxies.append('%s:%s' % (ip, port))
                    else:
                        ip['Address'] = j['RESULT']['wanIp'] + ':' + j['RESULT']['proxyport']
                        ip['Type'] = 'HTTP/HTTPS'
                        proxies_list.append(ip)
                        #ip = j['RESULT']['wanIp']
                        #port = j['RESULT']['proxyport']
                        #proxies.append('%s:%s' % (ip, port))
        except Exception, e:
            print e
            #logger.warning('failed to fetch from xdaili fee')
            print 'failed to fetch from xdaili fee'

        proxies = pd.DataFrame(proxies_list)

        return proxies

    def checkip(self, proxy):
        http_url = 'http://ip.chinaz.com/getip.aspx'
#        https_url = 'https://exmail.qq.com'
#        http_url = 'http://proxy.mimvp.com/test_proxy2.php'
        #https_url = 'https://proxy.mimvp.com/test_proxy2.php'
        https_url = 'https://exmail.qq.com'
        #socket.setdefaulttimeout(3)
        result_list = []
        for index, sr in proxy.iterrows():
           try:
               proxy_type = sr['Type']
               proxy_host = 'http://' + sr['Address']
               if proxy_type == 'HTTPS':
                   url = https_url
                   proxies = {'https': proxy_host}
               elif proxy_type == 'HTTP':
                   url = http_url
                   proxies = {'http': proxy_host}
               elif proxy_type == 'HTTP/HTTPS':
                   url = http_url
                   proxies = {'http': proxy_host, 'https': proxy_host}
               

               resp = requests.get(url, proxies=proxies)
               #print resp.status_code
#               print proxy_host, proxy_type
#               print resp.content
              
#               print json.loads(resp.content)
#               try:
#                   info = json.loads(resp.content)
#               except Exception, e:
#                   sr['Status'] = False
#                   print e
#               else:
#                   sr['Status'] = True
#                   print resp.status_code
#                   print proxy_host, proxy_type
#                   print resp.content
               m = re.findall('无效用户', resp.content)
               if len(m) > 0:
                   sr['Status'] = False
               else:
                   print resp.status_code
                   print proxy_host, proxy_type
                   print resp.content
               #if resp.status_code == 200:
                   sr['Status'] = True
                   #validate_list.append(sr)
           except Exception, e:
               print e
               sr['Status'] = False
           result_list.append(sr)
        proxies_ip = pd.DataFrame(result_list)
#        proxies_ip.to_csv('./proxies_ip.csv', index=False)
        return proxies_ip

    def fetch_proxies(self):
        old_proxies = pd.read_csv('./proxies_ip.csv')
#        proxies_df = self.fetch_xici_free('nn')
        #proxies_df = self.fetch_xdaili_free()
        proxies_df = self.fetch_xdaili_fee()
        proxies_df['Status'] = None
        proxies_df = pd.concat([old_proxies, proxies_df])
        #print proxies_df
        #proxies_df.to_csv('./xdaili_proxies_ip.csv', index=False, na_rep='NaN')
        failed_df = proxies_df[(proxies_df['Status']==False)]
        check_df = proxies_df[(proxies_df['Status'].isnull()) | (proxies_df['Status']==True)]
        df = self.checkip(check_df)
        df = pd.concat([failed_df, df])
        df.to_csv('./proxies_ip.csv', index=False)

def main():
    data_fetcher = GetIpProxy()
    data_fetcher.fetch_proxies()

#    nn_df = data_fetcher.fetch_xici_free('nn')
    #nt_df = data_fetcher.fetch_xici_free('nt')
#    proxies_df = nn_df#pd.concat([nn_df, nt_df])
#    proxies_df.to_csv('./full_proxies_ip.csv', index=False)
#    proxies_df = pd.read_csv('./full_proxies_ip.csv')
#    succ_df = data_fetcher.checkip(proxies_df)
#    succ_df.to_csv('./proxies_ip.csv', index=False)


if __name__ == '__main__':
    main()

