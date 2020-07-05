import re,execjs
header_str = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 264
Content-Type: application/x-www-form-urlencoded
Cookie: JSESSIONID=8B1C8038969FD62463CB022052A97C24; OpenDocumentPLATFORMSVC_COOKIE_CMS=XFMDBO%3A6400; OpenDocumentPLATFORMSVC_COOKIE_USR=z0007fF_HY%5D%40af%4000%40%23%2444; OpenDocumentPLATFORMSVC_COOKIE_AUTH=secEnterprise; OpenDocumentPLATFORMSVC_COOKIE_TOKEN=
Host: 192.168.2.81:8080
Origin: http://192.168.2.81:8080
Pragma: no-cache
Referer: http://192.168.2.81:8080/BOE/OpenDocument/2003281506/OpenDocument/opendoc/openDocument.faces
Upgrade-Insecure-Requests: 1
User-Agent: Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14

'''
pattern = '^(.*?): (.*)$'
a = {}
for line in header_str.splitlines():
    new_str = re.sub(pattern, '\'\\1\': \'\\2\',', line)
    print(new_str)

