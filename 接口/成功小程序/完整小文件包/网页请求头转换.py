import re,execjs
header_str = '''
Host: s1.hdslb.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/css,*/*;q=0.1
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
DNT: 1
Connection: keep-alive
'''
pattern = '^(.*?): (.*)$'
a = {}
for line in header_str.splitlines():
    new_str = re.sub(pattern, '\'\\1\': \'\\2\',', line)
    print(new_str)

