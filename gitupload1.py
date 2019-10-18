#-*- coding:utf-8 -*-
import requests
import sys
import json
import base64
import datetime
import re
import time
import os

def getihuan():
    proxy_url = "http://144.202.83.23:5010/get/"
    proxy = requests.get(proxy_url).json().get('proxy')
    print(proxy)
    url = "https://ip.ihuan.me/tqdl.html"
    key_url = "https://ip.ihuan.me/mouse.do"
    #key_url = "http://ip.cn"
    cookies = {'statistics':'db1fd09d3852aaa0ada1a473309c178d','Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829':'1569338278,1569338412,1569338416','Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829':'1569375327'}
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36','Referer':'https://ip.ihuan.me/ti.html'}
    response_key = requests.get(key_url,headers=headers,cookies=cookies,proxies={"https":"https://"+proxy},timeout=10)
    #print(response_key.text)
    key = re.match(r'.*val\("(.*?)".*',response_key.text).group(1)
    data = {"num":200,"type":1,"key":key}
    print("FETCHING IP......")
    info = os.stat('a.txt')
    if info.st_size > 500000:
        with open('a.txt','w') as f:
            f.write("")

    response = requests.post(url,data,headers=headers,cookies=cookies,proxies={"https":"https://"+proxy},timeout=10)

    #print(response.text)
    ips = re.match(r'.*</div><div class="panel-body">(.*?)</div>.*',response.text).group(1).split('<br>')
    for proxy in ips:
        if len(proxy)<22 and len(proxy)>0:
            with open('a.txt','a+',encoding='utf-8') as f:
                f.write(proxy+'\n')

def gitupload():

    content_url = "https://api.github.com/repos/Libraggbond/example/contents"

    file_url = "https://api.github.com/repos/Libraggbond/example/contents/proxylist.txt"

    headers = {"Authorization":"token 09c05ae0f1398e6800bc9d098022bb6ebb4b98d4","Content-Type":"application/json"}

    sha = requests.get(content_url,headers=headers).json()[6].get('sha')

    file = open('a.txt','rb')

    filecontent = str(base64.b64encode(file.read()),'utf-8')

    file.close()

    print("UPLOADING")

    data = json.dumps({"message":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"content": filecontent,"sha": sha})

    result = requests.put(file_url,data=data,headers=headers)

    if result.status_code == 200:
        print("UPLOAD SUCCESS:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print("ERROR")

if __name__ =='__main__':
    while True:
        upload = True
        try:
            print("STARTING: "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            getihuan()
        except Exception as e:
            print("IP FETCH ERROR")
            upload = False
        if upload == True:
            gitupload()
            time.sleep(600)