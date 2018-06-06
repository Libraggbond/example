# -- coding: utf-8 --
import requests
import re
import sys
import HTMLParser
import lxml.html
reload(sys)
sys.setdefaultencoding("utf-8")

#url = sys.argv[1]
url = "http://127.0.0.1:8888/1/host/172.16.2.45.html"
response = requests.get(url)
response.encoding='utf-8'
res = response.text
res2 = res.strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('<br/>', '').strip()
res1 = re.sub('\s{2,}',' ',res2)
selector = lxml.html.fromstring(res1)

table = selector.xpath('//*[@id="vuln_list"]/tbody/tr')  #通过漏洞概况中，看看有几个存在漏洞的端口
for m in range(1,len(table)+1):
	tr = selector.xpath('//*[@id="vuln_list"]/tbody/tr[{}]/td[4]/ul/li'.format(str(m))) #每个端口下有几个漏洞
	for n in range(1,len(tr)+1):
		span = selector.xpath('//*[@id="vuln_list"]/tbody/tr[{}]/td[4]/ul/li[{}]/div/span'.format(str(m),str(n)))[0] #定位每个漏洞
		if "level_danger_high" in lxml.html.tostring(span):  #如果是高风险
			table = re.search(r'.*(table_\d*_\d*).*',lxml.html.tostring(span)).group(1)   #从高危漏洞的位置获取table_x_xxxxx
			vul_name = selector.xpath('//*[@id="vuln_list"]/tbody/tr[{}]/td[4]/ul/li[{}]/div/span'.format(str(m),str(n))) #获取漏洞名
			desc = selector.xpath('//*[@id="{}"]/td/table/tr[1]/td/text()'.format(table))[0] #从对应的table_x_xxxx获取漏洞描述
			solu = selector.xpath('//*[@id="{}"]/td/table/tr[2]/td/text()'.format(table))[0] #获取解决方案
			print vul_name[0].text,desc,solu
			


"""


//*[@id="vuln_list"]/tbody/tr[1]/td[4]/ul/li[1]/div/span
//*[@id="vuln_list"]/tbody/tr[1]/td[4]/ul/li[2]/div/span
//*[@id="vuln_list"]/tbody/tr[2]/td[4]/ul/li/div/span
//*[@id="vuln_list"]/tbody/tr[3]/td[4]/ul/li[1]/div/span
//*[@id="vuln_list"]/tbody/tr[7]/td[4]/ul/li/div/span
//*[@id="table_2_290303"]/td/table/tbody/tr[2]/td
"""
