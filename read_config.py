# -*- coding:utf8 -*-
try:
    import json
except Exception, e:
    raise e
    
def get_config():
    path = 'weibo.cfg'
    with open(path) as f:
        try:
            return json.loads(f.read())
        except Exception, e:
            raise e
            return 0

if __name__ == '__main__':
    print get_config()            
