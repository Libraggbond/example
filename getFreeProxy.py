# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import re
import sys
import requests
from time import sleep

sys.path.append('..')

from Util.WebRequest import WebRequest
from Util.utilFunction import getHtmlTree

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :return:
        """
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        key = 'ABCDEFGHIZ'
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    ip = ul.xpath('./span[1]/li/text()')[0]
                    classnames = ul.xpath('./span[2]/li/attribute::class')[0]
                    classname = classnames.split(' ')[1]
                    port_sum = 0
                    for c in classname:
                        port_sum *= 10
                        port_sum += key.index(c)
                    port = port_sum >> 3
                    yield '{}:{}'.format(ip, port)
                except Exception as e:
                    print(e)

    @staticmethod
    # def freeProxy02(count=20):
    #     """
    #     代理66 http://www.66ip.cn/
    #     :param count: 提取数量
    #     :return:
    #     """
    #     urls = [
    #         "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
    #         "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=0&s"
    #         "tart=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip"
    #     ]

    #     try:
    #         import execjs
    #         import requests

    #         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    #                    'Accept': '*/*',
    #                    'Connection': 'keep-alive',
    #                    'Accept-Language': 'zh-CN,zh;q=0.8'}
    #         session = requests.session()
    #         src = session.get("http://www.66ip.cn/", headers=headers).text
    #         src = src.split("</script>")[0] + '}'
    #         src = src.replace("<script>", "function test() {")
    #         src = src.replace("while(z++)try{eval(", ';var num=10;while(z++)try{var tmp=')
    #         src = src.replace(");break}", ";num--;if(tmp.search('cookie') != -1 | num<0){return tmp}}")
    #         ctx = execjs.compile(src)
    #         src = ctx.call("test")
    #         src = src[src.find("document.cookie="): src.find("};if((")]
    #         src = src.replace("document.cookie=", "")
    #         src = "function test() {var window={}; return %s }" % src
    #         cookie = execjs.compile(src).call('test')
    #         js_cookie = cookie.split(";")[0].split("=")[-1]
    #     except Exception as e:
    #         print(e)
    #         return

    #     for url in urls:
    #         try:
    #             html = session.get(url.format(count), cookies={"__jsl_clearance": js_cookie}, headers=headers).text
    #             ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html)
    #             for ip in ips:
    #                 yield ip.strip()
    #         except Exception as e:
    #             print(e)
    #             pass
    def freeProxy02(count=2000):
    
        #print("UUUUUUUUUUUU")
        proxy = requests.get("http://144.202.83.23:5010/get/").json().get("proxy")
        proxies = "http://{}".format(proxy)
        urls = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=0&s"
            "tart=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip"
            ]

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                               'Accept': '*/*',
                               'Connection': 'keep-alive',
                               'Accept-Language': 'zh-CN,zh;q=0.8'}
            #session = requests.session()
            #src = requests.get("http://www.66ip.cn/", headers=headers).text
       
        except Exception as e:
            pass
            print(e)

        for url in urls:
            #print (url)
            try:
                html = requests.get(url.format(count), headers=headers,proxies={"http":proxies}).text
                ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html)
                for ip in ips:
                    yield ip.strip()
            except Exception as e:
                print(e)
                GetFreeProxy.freeProxy02(count=2000)
                #print(e)
                #pass

    @staticmethod
    def freeProxy03(page_count=20):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
           #'http://www.xicidaili.com/nn/',  # 高匿
           #'http://www.xicidaili.com/nt/',  # 透明
            'http://www.xicidaili.com/wn/',
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxy04():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))

                # HTML中的port是随机数，真正的端口编码在class后面的字母中。
                # 比如这个：
                # <span class="port CFACE">9054</span>
                # CFACE解码后对应的是3128。
                port = 0
                for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                                          "/attribute::class")[0]. \
                        replace("port ", ""):
                    port *= 10
                    port += (ord(_) - ord('A'))
                port /= 8

                yield '{}:{}'.format(ip_addr, int(port))
            except Exception as e:
                pass

    @staticmethod
    def freeProxy05():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06():
        """
        码农代理 https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/']
        for url in urls:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy07():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2",'http://www.ip3366.net/free/?stype=3']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        #print("UUUUUUUUUUUU")
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=2):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    # @staticmethod
    # def freeProxy10():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxy11():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    # @staticmethod
    # def freeProxy12():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    @staticmethod
    def freeProxy13(max_page=10):
        """
        http://www.qydaili.com/free/?action=china&page=1
        齐云代理
        :param max_page:
        :return:
        """
        base_url = 'http://www.qydaili.com/free/?action=china&page='
        request = WebRequest()
        for page in range(1, max_page + 1):
            url = base_url + str(page)
            r = request.get(url, timeout=10)
            proxies = re.findall(
                r'<td.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td.*?>(\d+)</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy14(max_page=10):
        """
        http://www.89ip.cn/index.html
        89免费代理
        :param max_page:
        :return:
        """
        base_url = 'http://www.89ip.cn/index_{}.html'
        request = WebRequest()
        for page in range(1, max_page + 1):
            url = base_url.format(page)
            r = request.get(url, timeout=10)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)
    @staticmethod
    def freeProxy15():
        url = "https://raw.githubusercontent.com/Libraggbond/example/master/proxylist.txt"

        try:
            response = requests.get(url)

            for ips in response.text.split('\n'):
                yield ips.strip()
        except Exception as e:
            pass
        # url = "https://ip.ihuan.me/tqdl.html"
        # key_url = "https://ip.ihuan.me/mouse.do"
        # cookies = {'statistics':'db1fd09d3852aaa0ada1a473309c178d','Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829':'1569338278,1569338412,1569338416','Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829':'1569375327'}
        # headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36','Referer':'https://ip.ihuan.me/ti.html'}
        # response_key = requests.get(key_url,headers=headers,cookies=cookies)
        # #print(response_key.text)
        # key = re.match(r'.*val\("(.*?)".*',response_key.text).group(1)
        # data = {"num":3000,"type":1,"key":key}
        # #print(key)

        # response = requests.post(url,data,headers=headers,cookies=cookies)

        # #print(response.text)
        # ips = re.match(r'.*</div><div class="panel-body">(.*?)</div>.*',response.text).group(1).split('<br>')
        # for proxy in ips:
        #     if len(proxy)<22 and len(proxy)>0:
        #         yield proxy
    @staticmethod
    def freeProxy16():
        url = "http://www.xiladaili.com/https/{}/"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                                       'Accept': '*/*',
                                       'Connection': 'keep-alive',
                                       'Accept-Language': 'zh-CN,zh;q=0.8'}

        for i in range(10):
            try:
                proxy = requests.get("http://144.202.83.23:5010/get/").json().get("proxy")
                proxies = "http://{}".format(proxy)
                response = requests.get(url.format(str(i)),headers=headers,proxies={"http":proxies},timeout=10)
                # print(url.format(str(i)))
                # print (response.text)
                ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", response.text)
                for proxy in ips:
                    yield proxy
            except Exception as e:
                pass
                
    @staticmethod
    def freeProxy17():
        url = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"

        try:
            response = requests.get(url)

            for ips in response.text.split('\n'):
                yield ips.strip()
        except Exception as e:
            pass

    @staticmethod
    def freeProxy18():
        url = "https://raw.githubusercontent.com/dxxzst/free-proxy-list/master/README.md"

        try:

            reponse = requests.get(url)

            results = reponse.text.split("\n")

            for ips in results:
                if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',ips):
                    yield ips.split('|')[1] + ":"+ips.split('|')[2]

        except Exception as e:
            pass

    @staticmethod
    def freeProxy19():
        url = "https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json"

        response = requests.get(url)

        proxies = response.json().get('proxies')

        for ips in proxies:

            yield ips.get('ip') + ":" + ips.get('port')


if __name__ == '__main__':
    from CheckProxy import CheckProxy

    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy01)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy02)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy03)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy04)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy05)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy06)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy07)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy08)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy09)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy13)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxy14)

    CheckProxy.checkAllGetProxyFunc()
