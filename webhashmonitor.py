import hackhttp
import hashlib
import pymongo
import time


client = pymongo.MongoClient()

db = client.hashdb

hashs = db.urlhash

urls = ["http://qepb.qingdao.gov.cn/n28356059/index.html","http://120.221.95.83/m2/index.aspx","http://219.147.6.195:8402/kqfb","http://219.147.6.195:8402/newhb/Login.aspx","http://219.147.6.195:8403","http://219.147.6.195:8403/login.aspx"]

#urls = ["http://qepb.qingdao.gov.cn/n28356059/index.html","http://120.221.95.83/m2/index.aspx"]

hh =  hackhttp.hackhttp()

for url in urls:

	# init hash

	# try:

	# 	code, head, html, redirect_url, log = hh.http(url)

	# 	hashtext = {"url":url,"hash":hashlib.sha256(html).hexdigest(),"time":time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))}
	
	# 	hashs.insert_one(hashtext)

	# 	print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;32mInsert OK\033[0m"


	# except:

	# 	print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;31mWarning\033[0m"

	
	#update hash

	# try:

	# 	code, head, html, redirect_url, log = hh.http(url)

	# 	hashtext = {"url":url,"hash":hashlib.sha256(html).hexdigest(),"time":time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))}
		
	# 	res = hashs.find_one_and_update({"url":url},{"$set":{"hash":hashlib.sha256(html).hexdigest(),"time":time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))}},return_document=pymongo.ReturnDocument.AFTER)

	# 	#print res
	# 	print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;32mUpdate OK\033[0m"


	# except:

	#  	print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;31mWarning\033[0m"


	 #verify

	try:

		code, head, html, redirect_url, log = hh.http(url)

		rs = hashs.find_one({"hash":hashlib.sha256(html).hexdigest()})

		if rs :

			print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;32mOK\033[0m"

		else:

			print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;31mWarning\033[0m"

	except:

		print url + '------' + time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())) + "------\033[1;31mAccess Warning\033[0m"




