import requests
import re
import datetime
import time
from requests.exceptions import RequestException
import pyhdb
from lxml import etree
from IDE.接口.setting import get_connection
# 定义hana连接
conn = get_connection().hana_connection(host='192.168.2.192', port='30241', user='XHZHOU', password='Zhou1234')
# def get_connection():
#     conn_obj = pyhdb.connect(
#         host="192.168.2.191",  # 192.168.2.191 生产机 192.168.2.192 开发机
#         port=30041,  # 30041生产机 30241开发机
#         user="XHZHOU",
#         password="Zhou1234"
#     )
#     return conn_obj
# 定义两个全局变量
global ccf_cookie,ccfei_cookie
# headers1 用于化纤信息网
headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "Referer": "https://www.ccf.com.cn"
}
formdata1 = {
    "custlogin": 1,
    "action": "login",
    "username": "zhongxin",
    "password": "xfm8522"
}
url1 = 'http://www.ccf.com.cn/member/member.php'
ccf = requests.Session()
cookie_jar = ccf.post(url1, headers=headers1, data=formdata1).cookies
ccf_cookie = requests.utils.dict_from_cookiejar(cookie_jar)
# headers2 用于中纤网
headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "Referer": "http://www.ccfei.com/Default.aspx"
}
formdata2 = { 'username': 'Kjg4KjI3KjY3KjI3', 'userpwd': 'KjA1Kjk0Kjk0Kjk0KjA1KjQ1Kjk0KjU1KjU1KjE1Kjk0','url':'/Default.aspx'}
url2 = 'http://www.ccfei.com/User/SmallUserLogin.aspx/UserLogin'
ccf = requests.Session()
cookie_jar = ccf.post(url2, headers=headers2, json=formdata2).cookies
ccfei_cookie = requests.utils.dict_from_cookiejar(cookie_jar)


# 设置response.post函数
def post_one_page(url, headers, data, cookies):
    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
# 设置response.get函数
def get_one_page(url, headers, data, cookies):
    try:
        response = requests.get(url, headers=headers, data=data, cookies=cookies)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
# 设置post函数获取json数据(返回response)
def post_json_page(url, headers, zjson ,cookies):
    try:
        response = requests.post(url, headers=headers, json=zjson, cookies=cookies)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        return None
# 设置获取ccf价格指数数据
def parse_one_page(html):
    html2 = etree.HTML(html)
    j = 2
    while j<=3:
        a = '//div[@class="box_products_txt"]/table/tr[%s]/td[1]/text()' % j
        b = '//div[@class="box_products_txt"]/table/tr[%s]/td[2]/text()' % j
        c = '//div[@class="box_products_txt"]/table/tr[%s]/td[3]/text()' % j
        index = html2.xpath(a)
        erdat = html2.xpath(b)
        sl = html2.xpath(c)
        yield {
            'index': index[0],
            'erdat': erdat[0].strip()[0:4]+erdat[0].strip()[5:7]+erdat[0].strip()[8:10],
            'sl': sl[0]
        }
        j = j+1
# 设置获取轻纺城指数数据(先获得页面url地址，再跳转取数页面)
def parse_other_page(html, header, cookies):
    html2 = etree.HTML(html)
    items,i= [],1
    while i<=28:
        a = '//ul[@class="newslist"]/li[%s]/a/@href' % i
        value = html2.xpath(a)
        items.append(value[0])
        i=i+1
    print(items)
    for i in range(0,len(items)):  # len(items)
        url='http://www.ccf.com.cn'+items[i]
        data = re.findall('/newscenter/detail-1B0000-(.*?).shtml', items[i])[0][:8]  # 获取日期
        response = requests.get(url, headers=header, cookies=cookies)
        response.encoding = 'gbk'
        html2 = etree.HTML(response.text)
        if data>='20171020':
            j = 2
            while j <= 3:
                a = '//tbody/tr[%s]/td[1]/text()' % j
                b = '//tbody/tr[%s]/td[2]/text()' % j
                zxl = html2.xpath(a)[0]
                sl = html2.xpath(b)[0]
                j = j + 1
                yield {
                    'index': str(zxl),
                    'erdat': data,
                    'sl': int(sl)
                }
        elif data>='20170117':
            j = 3
            while j <= 4:
                a = '//tbody/tr[%s]/td[1]/text()' % j
                b = '//tbody/tr[%s]/td[2]/text()' % j
                zxl = html2.xpath(a)[0]
                sl = html2.xpath(b)[0]
                j = j + 1
                yield {
                    'index': str(zxl),
                    'erdat': data,
                    'sl': int(sl)
                }
        else:
            a1 = 'normalize-space(//tbody/tr[3]/td[1]/p/text())'
            b1= '//tbody/tr[3]/td[2]/text()'
            zxl = html2.xpath(a1)
            sl = html2.xpath(b1)[0]
            yield {
                'index': str(zxl)[-3:],
                'erdat': data,
                'sl': int(sl)
            }
            a2 = '//tbody/tr[4]/td[1]/text()'
            b2 = '//tbody/tr[4]/td[2]/text()'
            zxl = html2.xpath(a2)[0]
            sl = html2.xpath(b2)[0]
            yield {
                'index': str(zxl),
                'erdat': data,
                'sl': int(sl)
            }
            zxl = html2.xpath('//tbody/tr[4]/td[1]/text()')[0]
            sl = html2.xpath('//tbody/tr[4]/td[2]/text()')[0]
            print(zxl,sl)
            yield {
                 'index': zxl,
                 'erdat': data,
                 'sl': sl
            }
#获取库存/港口数据  MEG发货统计
def parse_other2_page(html, header, cookies):
    pattern = re.compile('<li(?: | class=articlebreak )><span>.*?href="(.*?)" class="h1a2" target="_blank" onmouseover="return overlib.*?>\d+月\d+日MEG发货统计</a></li>')  # 去掉re.S 不匹配换行符
    items = re.findall(pattern, html)
    for i in range(0,len(items)):  # 暂时只取一日数据 len(items)
        url='http://www.ccf.com.cn'+items[i]
        data = re.findall('/newscenter/detail-1C0000-(.*?).shtml', items[i])[0][:8]  # 获取日期
        data = datetime.datetime.strptime(data, '%Y%m%d') + datetime.timedelta(days=-1)  # 日期减少一天
        data = data.strftime('%Y%m%d')                                                   # 转换为yyyymmdd格式
        response = requests.get(url, headers=header, cookies=cookies)
        response.encoding = 'gbk'
        html2 = response
        pattern2 = re.compile('<div id=newscontent>.*?MEG发货量在(.*?)吨.*?</div>', re.S)
        items2 = re.findall(pattern2, html2.text)[:2]
        for item in items2:
            if item == []:
                print('\033[1;37;41m----------------------MEG发货量逻辑异常-----------------------\033[0m')
            else:
                yield {
                    'index': 'MEG发货量',
                    'erdat': data,
                    'sl': item
                }
#获取库存数据
def parse_other3_page(html):
    print(html)
    html2 = etree.HTML(html)
    a = html2.xpath('//tbody/')
    pattern = re.compile(
        '<tr .*?><td align=center>(.*?)</td>.*?<td align=center>(.*?)</td>.*?<td align=center>(.*?)</td>.*?<td align=center>(.*?)</td>.*?<td align=center>(.*?)</td></tr>', re.S)
    items = re.findall(pattern, html)
    print(items)
    for item in items:
        if item == []:
            print('\033[1;37;41m----------------------总库存逻辑异常-----------------------\033[0m')
        else:
            yield {
                'index': item[0],
                'erdat': item[1].strip()[0:4] + item[1].strip()[5:7] + item[1].strip()[8:10],
                'sl': item[2]
            }
# 获取库存/港口数据  MEG港口库存详细
def parse_other4_page(html, header,cookies):
    pattern = re.compile('<li(?: | class=articlebreak )><span>.*?href="(.*?)" class="h1a2" target="_blank" onmouseover="return overlib.*?MEG港口库存.*?</a></li>')  # 去掉re.S 不匹配换行符
    items = re.findall(pattern, html)
    for i in range(0,len(items)):  # 暂时只取一日数据 len(items)
        url='http://www.ccf.com.cn'+items[i]
        data = re.findall('/newscenter/detail-1C0000-(.*?).shtml', items[i])[0][:8]  # 获取日期
        response = requests.get(url, headers=header, cookies=cookies)
        response.encoding = 'gbk'
        html2 = response
        pattern2 = re.compile('<p(?:| style="text-indent: 2em;")>CCF讯.*?今日华东主港地区(.*?)约(.*?)万吨.*?</p>')
        items2 = re.findall(pattern2, html2.text)[0][1]
        if items2 == []:
            print('\033[1;37;41m----------------------MEG主港库存逻辑异常-----------------------\033[0m')
        else:
            yield {
                'index': 'MEG主港库存',
                'erdat': data,
                'sl': items2
            }

def main():
    # 定义today为当前日期 ny为年月
    today = datetime.date.today().strftime('%Y-%m-%d')
    ny = datetime.date.today().strftime('%Y-%m')
    yeday = datetime.datetime.strptime(today, '%Y-%m-%d') + datetime.timedelta(days=-4)
    yeday = yeday.strftime('%Y-%m-%d')
    sqllist = []
    headers1 = {
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    headers2 = {}
    headers3 = {}
    #  3(内盘PTA) 4(外盘PTA) 5(内盘MEG现货) 6(外盘MEG) 9(涤纶DTY 150D/48F低弹) 10(直纺半光POY 150D/48F) 12(直纺半光FDY 150D/96F)
    #  13(1.4D直纺涤短) 14(半光聚酯水平片) 15(华东聚酯水平片) 39(有光聚酯切片)
    # try:
    #     for i in(3, 4, 5, 6, 9, 10, 12 ,13 ,14 ,15, 39):  # 3, 4, 5, 6, 9, 10, 12 ,13 ,14 ,15
    #         data1 = {
    #             "Monitor_IDs": "a_210000_3,a_210000_4,a_220000_5,a_220000_6",
    #             "monitorId": i,
    #             "startdate": yeday,
    #             "enddate": today,
    #             "type": "dd"
    #         }
    #         url1 = 'http://www.ccf.com.cn/dynamic_graph/getPrice.php'
    #         response = post_one_page(url1, headers1, data1, ccf_cookie)
    #         # print(response)
    #         for item in parse_one_page(response):
    #             item=list(item.values())
    #             sqllist.append(item)
    # except:
    #     print('\033[1;37;41m----------------------未取到CCF价格数据-----------------------\033[0m')

    # # 获取轻纺城数据源 总销量 化纤布
    # try:
    #     for j in({'1'}):  # 从1到n页抓取数据
    #         url2 = 'http://www.ccf.com.cn/newscenter/index.php?cur_row_pos=0&cur_pg_num='+j+"&Class_ID=1B0000"
    #         response2 = get_one_page(url2, headers2, [], ccf_cookie)
    #         for item in parse_other_page(response2, headers2, ccf_cookie):
    #             item=list(item.values())
    #             sqllist.append(item)
    # except:
    #     print('\033[1;37;41m----------------------未取到轻纺城数据-----------------------\033[0m')
    #
    # # 获取库存/港口数据
    # try:
    #     for j in({'1'}):  # 从1到n页抓取数据
    #         url3 = 'http://www.ccf.com.cn/newscenter/index.php?cur_row_pos=0&cur_pg_num='+j+"&Class_ID=1C0000"
    #         response2 = get_one_page(url3, headers2, [], ccf_cookie)
    #         for item in parse_other2_page(response2, headers2, ccf_cookie):
    #             item=list(item.values())
    #             sqllist.append(item)
    # except:
    #     print('\033[1;37;41m----------------------未取到库存/港口数据-----------------------\033[0m')
    # #
    # # 获取库存/港口数据 MEG港口库存详细
    # try:
    #     for j in ({'1'}):  # 从1到n页抓取数据
    #         url3 = 'http://www.ccf.com.cn/newscenter/index.php?cur_row_pos=0&cur_pg_num=' + j + "&Class_ID=1C0000"
    #         response2 = get_one_page(url3, headers2, [], ccf_cookie)
    #         for item in parse_other4_page(response2, headers2, ccf_cookie):
    #             item = list(item.values())
    #             sqllist.append(item)
    # except:
    #     print('\033[1;37;41m----------------------未取到MEG港口库存数据-----------------------\033[0m')
    #
    # kczs:CCF库存指数  292000/POY库存 290000/FDY库存 291000/DTY库存 280000/涤纶短纤库存
    # fhzs:CCG负荷指数  210000/PTA负荷 222000/MEG负荷(总) 223000/MEG煤制负荷 220000/聚酯负荷
    #                  230000/直纺长丝负荷 240000/直纺短纤负荷 274000/聚酯瓶片负荷
    # xyzs:CCF下游指数  110000/江浙纺机开机率 150000/江浙加弹开机率
    try:
        sj = (['kczs',292000],['kczs',290000],['kczs',291000],['kczs',280000],
              ['fhzs',210000],['fhzs',222000],['fhzs',223000],['fhzs',220000],['fhzs',230000],['fhzs',240000],['fhzs',274000],
              ['xyzs',110000],['xyzs',150000])
        for l in range(0,1):# len(sj)
            data2 = {
                "ProdClass": sj[l][0],
                "ProdID": sj[l][1],
                "startDate": "2019-06-01",
                "endDate": today
            }
            url4 = 'http://www.ccf.com.cn/dynamic_graph/index.php'
            response = post_one_page(url4, headers2, data2, ccf_cookie)
            for item in parse_other3_page(response):
                item = list(item.values())
                sqllist.append(item)
    except:
        print('\033[1;37;41m----------------------未取到库存指数数据-----------------------\033[0m')
    #
    # zjson = {
    #     'pid': 79,
    #     'ptext': 'PTA%u6D41%u901A%u73AF%u8282',
    #     'date1': '2019-05',
    #     'date2': ny
    # }
    # url5 = 'http://www.ccfei.com/Price/InventoryChart.aspx/GetData'
    # response3 = post_json_page(url5, headers3, zjson, ccfei_cookie)
    # a = response3.json()
    # b = a["d"]
    # c = json.loads(b)
    # try:
    #     answer = c[1][0]
    #     for i in range(0, len(answer)):
    #         x, y = answer[i][0], answer[i][2]
    #         answer[i][0] = 'PTA流通环节库存'
    #         answer[i][1] = y[:4] + y[5:7] + y[8:10]
    #         answer[i][2] = x
    #         sqllist.append(answer[i])
    # except:
    #     print('\033[1;37;41m----------------------未取到PTA流通环节库存-----------------------\033[0m')
    # 合并所有sqlist
    sqltuple = tuple(sqllist)
    # 定义连接，并插入数据
    # conn = get_connection()
    cursor = conn.cursor()
    for i in range(0,len(sqltuple)):
        print(sqltuple[i])
        try:
            cursor.execute(
                '''insert into "COMMON"."XFM_MARKT" (ZB , ERDAT ,SPJ)values (%s,%s,%s)''', sqltuple[i])
            time.sleep(0.1)
        except:
            continue
    conn.commit()


if __name__ == '__main__':
    main()