# # import requests
# # url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=27_KLL9BbJSgyBZYUA_cdd75SuaVxjesiILNmWobU4AkaEU-wphy0QAJU8M1whvPUDWGQo6UXsDrc3KQSTC7qwmz2uLohMCa1HIT7DkuaUqrWfcwiZFG7RJwI4TnPfTc77Dv8IpnTZwLrSnB5Q9ILKiAAAXAZ&type=image"
# # data = {'media':open("C:\\Users\\admin\\Desktop\\1.jpg",'rb')}
# # r = requests.post(url=url,files=data)
# # print(r)
# # dict = r.json()
# # print(dict)
# # print(dict['media_id'])
#
# import os
# os.system('chcp 65001')  # 更改GBK编码为UTF8编码
# # cmd = '''curl -F media=@C:\\Users\\admin\\Desktop\\ccc.jpg "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=27_5A5uVrr1wySuc7By4Bt8Z4KuQwMLbWi3hFffE3MuSinIhEC-Ck-slQUrhyesdztI4SZmDwldVLRokr8PBtHdqRIA-oQK1TpfaCDxoOkYKLN5nrCQqj6VPjkaT5hlBMJnQew5IoWBws_R20NqGOKaABAJRN&type=image"
# # '''
# # print(os.system(cmd))
# print(os.system('curl  https://www.baidu.com'))
#
#
#
#
# import os
#
# a = 'C:\\curl\\curl\\bin\\curl.exe'
# os.system('chcp 65001')
# a = os.system('%s -d wd=hua https://www.baidu.com/' % a)
#
# print(a)
#
# print("ok..")
#
# '''curl "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=TYPE" -F media=@media.file -F  description='{"title":VIDEO_TITLE, "introduction":INTRODUCTION}' '''
#
# k = 'http://mmbiz.qpic.cn/mmbiz_jpg/Cw9HUFy1omLmdH2NcujMSgSQXicnp0Q1BnOuPm8K2iczh43KnNwAPMjxciajib9z0w3yt96aVpsMXb3HM84tiaJHmUA/0?wx_fmt=jpeg'
import json

a = '{"errcode":45009,"errmsg":"reach max api daily quota limit hints: [gE-3R2BwA!]"}'
a = json.loads(a)
print(a['errcode'])
