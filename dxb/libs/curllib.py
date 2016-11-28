#coding=utf-8

# python http客户端 基于python的库 urllib

import pdb
import urllib
import urllib2
import cookielib
import json
import httplib  

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

def json_post(ip,port,path,data):
    pdb.set_trace()
    try:  
        conn = httplib.HTTPConnection("www.dh3t.com",port)
    except Exception,e:  
        print e  
    headers = {"Content-Type":"application/json"}  
    param = (data)
    conn.request("POST" ,path, json.JSONEncoder().encode(param), headers)  
    response = conn.getresponse()  
    data = response.read()  
    print data  
    conn.close() 

if __name__ == "__main__":
    data = {
      "account":"dh6806",
      "password":"52c6db220833cd648eed69dcf2245375",
      "msgid":"2c92825934837c4d0134837dcba00150",
      "phones":"15996458299",
      "content":"测试发送短信",
      "sign":"【南京擎盾】"
    }
    ip = "www.dh3t.com"
    port = 80
    path = "/json/sms/Submit"
    json_post(ip, port, path, data)
