#coding=utf-8

# python http客户端 基于python的库 urllib

import urllib
import urllib2
import cookielib
import json

#发送跨域POST请求
def send_post_request(url,data,csrftoken,headers) :
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'csrftoken=%s'%(csrftoken)))
    opener.addheaders.extend(headers.items())
    result = json.loads(opener.open(url,data).read())

#获取csrf token
def get_csrf_token(url) :
    import urllib
    import urllib2
    import cookielib
    f = urllib.urlopen(url)
    result_data = json.loads(f.read())
    result_data["headers"] = f.headers
    return result_data

def post(*args,**options):
    url = options.get('url',None)
    data = options.get('data',{})
    if not url :
        raise "url error"
    if type(data) != type({}):
        raise "request data error"
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    result = json.loads(opener.open(url, data).read())
    return result

def get(*args,**options):
    import urllib
    import urllib2
    import cookielib
    url = options.get('url', None)
    data = options.get('data', {})
    if not url:
        raise "url error"
    if type(data) != type({}):
        raise "request data error"
    f = urllib.urlopen(url)
    result = json.loads(f.read())
    return result
