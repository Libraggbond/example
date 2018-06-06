# coding=utf8
import urllib2
import string
import urllib
import re
import random
import time
#设置多个user_agents，防止百度限制IP
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
    (KHTML, like Gecko) Element Browser 5.0', \
    'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
    Version/6.0 Mobile/10A5355d Safari/8536.25', \
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/28.0.1468.0 Safari/537.36', \
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
def baidu_search(keyword,pn):
  p= {'wd': keyword} 
  #print p
  res=urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=100").format(pn))
  #print res
  html=res.read()
  #print html
  return html
def getList(regex,text):
  arr = []
  res = re.findall(regex, text)

  #print res
  if res:
    for r in res:
      arr.append(r)
      #print r
  return arr
def getMatch(regex,text):
  res = re.search(regex, text)
  if res:
    #print res
    return res.group(1)
  return ""
def clearTag(text):
  p = re.compile(u'<[^>]+>')
  retval = p.sub("",text)
  return retval
def geturl(keyword):
  result = []
  for page in range(30):
    #print page
    pn=page*10
    #print pn 
    html = baidu_search(keyword,pn)
    html_join = "".join(html.split())
    #print html_join

    #print type(html)
    #content = unicode(html, 'utf-8','ignore')
    #print content
    arrList = getList(r'<div.*?class=\"resultc.*?\}\">(.*?)<\/div><\/div>', html_join)

    for item in arrList:
      #print item
      info = {}
      title_regex = r"<a.*?data-click.*?>(.*?)</a>"
      content_regex = r"<div.*?class=\"`c-abstract\">(.*?)</div>"
      location_regex = r"<div.*?class=\"f13\">.*?href=\"(.*?)\""
      info['title'] = getMatch(title_regex,item)
      info['content'] = getMatch(content_regex,item)
      location = getMatch(location_regex,item)
      #print location
      #result.append(info)
      #link = getMatch(regex,item)
      #url = link[0]
      #print url
      #获取标题
      #title = clearTag(link[1]).encode('utf8')
      try:
        #time.sleep(1)
        domain=urllib2.Request(location)
        r=random.randint(0,9)
        #print r,len(user_agents)
        domain.add_header('User-agent', user_agents[r])
        domain.add_header('connection','keep-alive')
        #print location
        response=urllib2.urlopen(location)
        info['location']=response.geturl()
        info['code'] = response.getcode()
        #print info

      #except  urllib2.HTTPError,e:
        #print 
      except:
        pass
        #info['code'] = e.code
        #info['location'] = e.geturl()
      
      if 'location' in info:

        result.append(info['location'])
      result = list(set(result))
        
      #print result
        
  
    #print each['location'],each['code']
    
    with open("baidu.txt",'a+') as f:
      
      #f.write("当前检测关键字为： 娱乐城" +  "\n")
      #f.write("**********检测到可疑内容**********" + "\n")
      for i in result:
        print i
        f.write(i + "\n")

        #f.write("地址：" + each['location'] + "\n")
      #f.write("标题："+ each['title'] + "\n")
      #f.write("摘要内容：" + each['content'] + "\n")
      #f.write("地址返回码：" + str(each['code']) + "\n")
      #f.write("---------------END--------------" + "\n")
if __name__=='__main__':
  #geturl('site:upc.edu.cn 娱乐城')
  geturl('intitle: 中国海洋大学')
