import hackhttp

hh = hackhttp.hackhttp()

with open ('dga.txt') as f:
	dgas = f.readlines(100)
	for dga in dgas[18:]:
		url = dga.split('\t')[1]
		url = 'http://' + url 
		print url
		try:
			hh.http(url)
		except:
			pass
