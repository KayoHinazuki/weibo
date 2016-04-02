
# -*- coding: utf8 -*-
try:
    import os
    import sys
    import json
    import urllib
    import binascii
    import base64
    import requests
    import rsa
    import re
    import time
    import random
    import base62

except ImportError:
    print >> sys.stderr,"%s" % (sys.exc_info(), )
    sys.exit(1)

class login(object):
    def __init__(self):
        self.session = requests.Session()
        self._match_rexp = re.compile('\((.*)\)')
        self.count = 0
    def _in(self):
        # check session cookies
        return 0
    
    def gen_time(self):
        self._timestamp = time.time()
        self._random = random.randint(100,999)
    
    def _get_time_str(self):
        return str(int(self._timestamp))+str(self._random)
    
    def increment_time(self):
        self.count += 1;
        self._random = self._random+2
        return self._get_time_str()

    def waiting_for_scan(self):
        #if self.count > 18:
        #    self.count = 0
        #    self.getQRcode()
        #    return 1
        ### here will send 3 alt to server
        response = self.session.post('http://login.sina.com.cn/sso/qrcode/check?entry=weibo&qrid='+self.qrcode+'&callback='+self.increment_time())
        try:
            json_data = self._match_rexp.search(response.text).group(1)
            data = json.loads(json_data)
           # print data['msg'].decode('gb2312')
            if int(data['retcode']) != 20000000:
                return 1
            else:
                print data
                self.alt = data['data']['alt']
                return 0  
        except Exception, e:
            raise e
    def get_session(self):
        return self.session
        
    def into(self):
        response = self.session.get('http://login.sina.com.cn/sso/login.php?entry=weibo&returntype=TEXT&crossdomain=1&cdult=3&domain=weibo.com&alt='+self.alt+'&savestate=30&callback='+self.increment_time())
        try:
            json_data = self._match_rexp.search(response.text).group(1)
            data = json.loads(json_data)
            print data
            if int(data['retcode']) == 0:
                return 1
            else:
                return 0
        except Exception, e:
            raise e
    def getQRcode(self):
        if self._in():
            print "already login!"
        else:
            # every 2 second 5 times
            self.gen_time();
            response = self.session.get("http://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_"+self._get_time_str())
            if response.status_code != 200:
                print "network error!"
                return 0    
            # find qr image from response
            try:
                json_data = self._match_rexp.search(response.text).group(1)
                data = json.loads(json_data)
                if data['retcode'] == 20000000:
                    print "### success get the qrcode ##"
                else:
                    return 0
                self.qrcode = data['data']['qrid']
                self.image = data['data']['image']
                response2 = self.session.get(self.image) # get qrimage
                f = open('qrimage.png','wb')
                f.write(response2.content)
                f.close()
                #time.sleep(1)
               # os.startfile('qrimage')        
            except Exception, e:
                raise e
                return 0
    def get_weibo(self,url):
        user_agent = {'User-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        response = self.session.get(url,headers=user_agent)
        print response.text

if __name__ == '__main__':
    lo = login()
    lo.getQRcode()
    while lo.waiting_for_scan():
        print 'waiting_for_scan'
    print '## scan success'
    if lo.into():
        lo.get_weibo('http://weibo.com/vinthony');
