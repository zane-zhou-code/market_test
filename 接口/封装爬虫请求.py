import json
import requests
import re
import datetime
import time
from multiprocessing import Pool
from requests.exceptions import RequestException
from lxml import etree
import random
import ast
from 接口.setting import get_connection,sql,wechat_auto

class get_market_values(object):
    # 请求头部信息
    _headers = {
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    # 获取ccf和中纤网登陆cookie
    def ccf_cookie(self):
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
        sleeptime = random.randint(60, 120)
        print('\033[37;40m-------------------已登陆CCF获取cookies休眠', sleeptime,'秒------------------\033[0m')
        time.sleep(sleeptime)
        ccf_cookie = requests.utils.dict_from_cookiejar(cookie_jar)
        return ccf_cookie
    def ccfei_cookie(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Referer": "http://www.ccfei.com/Default.aspx"
        }
        formdata = {'username': 'Kjg4KjI3KjY3KjI3', 'userpwd': 'KjA1Kjk0Kjk0Kjk0KjA1KjQ1Kjk0KjU1KjU1KjE1Kjk0',
                     'url': '/Default.aspx'}
        url2 = 'http://www.ccfei.com/User/SmallUserLogin.aspx/UserLogin'
        ccf = requests.Session()
        cookie_jar = ccf.post(url2, headers=headers, json=formdata).cookies
        ccfei_cookie = requests.utils.dict_from_cookiejar(cookie_jar)
        return ccfei_cookie
    def icis_cookie(self):
        counter = 1
        while counter <= 2:
            try:
                headers_o = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
                }
                # 利用最终url跳转url2-logon,跳转url3-connect_authorize,跳转url4-login(取网页参数asp、rvfc和cookies)
                url = 'https://www.icis.com/Dashboard/PurchasedPriceHistory/DisplayChartDualYAxis'
                response = requests.post(url, headers=headers_o, timeout=120, allow_redirects=False)
                url2 = 'https://www.icis.com' + response.headers['location']

                response_lgo = requests.get(url2, headers=headers_o, timeout=120, allow_redirects=False)
                url3 = response_lgo.headers['location']

                response_coa = requests.get(url3, headers=headers_o, timeout=120, allow_redirects=False)
                url4 = response_coa.headers['location']
                cookie_coa = requests.utils.dict_from_cookiejar(response_coa.cookies)

                response_lgi = requests.get(url4, headers=headers_o, timeout=120, cookies=cookie_coa, allow_redirects=False)
                html = etree.HTML(response_lgi.text)
                set_para = '//*[@id="login-form"]/input/@value'
                asp = html.xpath(set_para)[0]
                rvfc = html.xpath(set_para)[1]
                cookie_lgi = requests.utils.dict_from_cookiejar(response_lgi.cookies)

                data_o = {
                    'ReturnUrl': asp,
                    'Username': 'henglilh@hengli.com',
                    'Password': 'HLlh2018',
                    'button': 'login',
                    '__RequestVerificationToken': rvfc,
                    'RememberLogin': 'false',
                }
                response_lgi_y = requests.post(url4, headers=headers_o, data=data_o, cookies=cookie_lgi, timeout=120,
                                               allow_redirects=False)
                cookies_lgi_y = requests.utils.dict_from_cookiejar(response_lgi_y.cookies)

                url5 = 'https://www.icis.com/Dashboard/'
                response_das = requests.get(url5, headers=headers_o, cookies=cookies_lgi_y, timeout=120)
                cookies_das = requests.utils.dict_from_cookiejar(response_das.cookies)
                html2 = etree.HTML(response_das.text)
                set_para2 = '//*[@class="    primaryBG"]/input/@value'
                rvfc2 = html2.xpath(set_para2)[0]
                return (cookies_das, rvfc2)
            except:
                pass
            counter = counter + 1
    # 定义response的get post json 函数，获取网页文本
    def get_one_page(self, url, headers, data, cookies):
        try:
            response = requests.get(url, headers=headers, data=data, cookies=cookies)
            response.encoding = 'gbk'
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None
    def post_one_page(self, url, headers, data, cookies):
        try:
            response = requests.post(url, headers=headers, data=data, cookies=cookies)
            response.encoding = 'gbk'
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None
    def post_json_page(self, url, headers, zjson, cookies): # 此处返回response
        try:
            response = requests.post(url, headers=headers, json=zjson, cookies=cookies)
            if response.status_code == 200:
                return response
            return None
        except RequestException:
            return None
    # 定义爬取网页函数
    def parse_one_page(self):
        assert (0)
    # 转换yield为数组
    def arry_list(self, func, *params):
        _sqllist = []
        try:
            for item in func.parse_one_page(*params):
                 item = list(item.values())
                 _sqllist.append(item)
            return tuple(_sqllist)
        except:
            return self.parse_one_page()
    # 定义并发作业 1.生成进程池的类(能够重用进程,能够限制进程的数量)
    #             2.将任务设置进入进程池
    #             3.进程池关闭
    #             4.等待所有进程结束
    def parse_concurrent(self, *params):
        pool = Pool(6)
        # 接受进程池的返回值
        res_list = []
        for func in (ccf_price_values(), qfc_sales_values(), meg_send_values(),
                     meg_stock_values(), stock_load_values(),
                     pta_stock_values(), export_polyester(),
                     cj_metal(), icis_price()):
            sleeptime = random.randint(60, 120)
            print('\033[37;40m-------------------进程池休眠', sleeptime, '秒------------------\033[0m')
            time.sleep(sleeptime)
            res = pool.apply_async(func=self.arry_list, args=(func, *params))
            res_get_list = res.get()
            for i in range(0, len(res_get_list)):
                res_list.append(res_get_list[i])
            print('\033[37;40m-------------------已完成 ',str(func),' 取数------------------\033[0m')
        pool.close()
        pool.join()
        return tuple(res_list)
# 获取ccf价格数据
class ccf_price_values(get_market_values):
    def parse_one_page(self, *params):
        #  3(内盘PTA) 4(外盘PTA) 5(内盘MEG现货) 6(外盘MEG) 9(涤纶DTY 150D/48F低弹) 10(直纺半光POY 150D/48F) 12(直纺半光FDY 150D/96F)
        #  13(1.4D直纺涤短) 14(半光聚酯水平片) 15(华东聚酯水平片) 39(有光聚酯切片)
        counter=1
        while counter<=2:
            try:
                for i in (3, 4, 5, 6, 9, 10, 12, 13, 14, 15, 39):  # 3, 4, 5, 6, 9, 10, 12 ,13 ,14 ,15
                    data = {
                        "Monitor_IDs": "a_210000_3,a_210000_4,a_220000_5,a_220000_6",
                        "monitorId": i,
                        "startdate": params[0][0],
                        "enddate": params[0][1],
                        "type": "dd"
                    }
                    url = 'http://www.ccf.com.cn/dynamic_graph/getPrice.php'
                    cookies = ast.literal_eval(params[0][3])
                    response = self.post_one_page(url, self._headers, data, cookies)
                    html2 = etree.HTML(response)
                    sleeptime = random.randint(15, 30)
                    print('\033[37;40m-------------------获取指标%s价格数据休眠%s秒------------------\033[0m' % (i, sleeptime))
                    time.sleep(sleeptime)
                    if str(params[0][0])[:7] == str(params[0][1])[:7]:
                        for i in (2, 3):
                            a = '//div[@class="box_products_txt"]/table/tr[%s]/td[1]/text()' % i
                            b = '//div[@class="box_products_txt"]/table/tr[%s]/td[2]/text()' % i
                            c = '//div[@class="box_products_txt"]/table/tr[%s]/td[3]/text()' % i
                            index = html2.xpath(a)
                            erdat = html2.xpath(b)
                            sl = html2.xpath(c)
                            if index==[]:
                                break
                            yield {
                                'index': str(index[0]),
                                'erdat': str(erdat[0].strip()[0:4] + erdat[0].strip()[5:7] + erdat[0].strip()[8:10]),
                                'sl': int(sl[0])
                            }
                    else:
                        a = '//div[@class="box_products_txt"]/table/tr[%s]/td[1]/text()' % 2
                        b = '//div[@class="box_products_txt"]/table/tr[%s]/td[2]/text()' % 2
                        c = '//div[@class="box_products_txt"]/table/tr[%s]/td[3]/text()' % 2
                        index = html2.xpath(a)
                        erdat = html2.xpath(b)
                        sl = html2.xpath(c)
                        for i in range(0, len(index)):
                            yield {
                                'index': str(index[i]),
                                'erdat': str(erdat[i].strip()[0:4] + erdat[i].strip()[5:7] + erdat[i].strip()[8:10]),
                                'sl': int(sl[i])
                            }
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到CCF价格数据-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 6)
            counter = counter + 1
# 获取轻纺城数据源 总销量 化纤布
class qfc_sales_values(get_market_values):
    def parse_one_page(self, *params):
        counter = 1
        while counter <= 2:
            try:
                for j in ({'1'}):  # 从1到n页抓取数据
                    url = 'http://www.ccf.com.cn/newscenter/index.php?cur_row_pos=0&cur_pg_num=' + j + "&Class_ID=1B0000"
                    cookies = ast.literal_eval(params[0][3])
                    response = self.get_one_page(url, self._headers, [], cookies)
                    sleeptime = random.randint(5, 10)
                    print('\033[37;40m-------------------获取轻纺城网页url休眠', sleeptime, '秒------------------\033[0m')
                    time.sleep(sleeptime)
                    pattern = re.compile(
                        '<li(?: | class=articlebreak )><span>.*?href="(.*?)" class="h1a2" target="_blank" onmouseover="return overlib.*?</a></li>',
                        re.S)
                    items = re.findall(pattern, response)
                    # 获取页面的url信息
                    for i in range(0, 3):  # len(items)
                        url = 'http://www.ccf.com.cn' + items[i]
                        data = re.findall('/newscenter/detail-1B0000-(.*?).shtml', items[i])[0][:8]  # 获取日期
                        response = requests.get(url, [], cookies=cookies)
                        sleeptime = random.randint(15, 30)
                        print('\033[37;40m-------------------获取新一条轻纺城数据休眠', sleeptime, '秒------------------\033[0m')
                        time.sleep(sleeptime)
                        response.encoding = 'gbk'
                        html2 = etree.HTML(response.text)
                        if data >= '20171020':
                            j = 2
                            while j <= 3:
                                a = '//tbody/tr[%s]/td[1]/text()' % j
                                b = '//tbody/tr[%s]/td[2]/text()' % j
                                zxl = html2.xpath(a)[0]
                                sl = html2.xpath(b)[0]
                                yield {
                                    'index': str(zxl),
                                    'erdat': str(data),
                                    'sl': int(sl)
                                }
                                j = j + 1
                        elif data >= '20170117':
                            j = 3
                            while j <= 4:
                                a = '//tbody/tr[%s]/td[1]/text()' % j
                                b = '//tbody/tr[%s]/td[2]/text()' % j
                                zxl = html2.xpath(a)[0]
                                sl = html2.xpath(b)[0]
                                yield {
                                    'index': str(zxl),
                                    'erdat': str(data),
                                    'sl': int(sl)
                                }
                                j = j + 1
                        else:
                            a1 = 'normalize-space(//tbody/tr[3]/td[1]/p/text())'
                            b1 = '//tbody/tr[3]/td[2]/text()'
                            zxl = html2.xpath(a1)
                            sl = html2.xpath(b1)[0]
                            yield {
                                'index': str(zxl)[-3:],
                                'erdat': str(data),
                                'sl': int(sl)
                            }

                            a2 = '//tbody/tr[4]/td[1]/text()'
                            b2 = '//tbody/tr[4]/td[2]/text()'
                            zxl = html2.xpath(a2)[0]
                            sl = html2.xpath(b2)[0]
                            yield {
                                'index': str(zxl),
                                'erdat': str(data),
                                'sl': int(sl)
                            }

                            zxl = html2.xpath('//tbody/tr[4]/td[1]/text()')[0]
                            sl = html2.xpath('//tbody/tr[4]/td[2]/text()')[0]
                            yield {
                                'index': str(zxl),
                                'erdat': str(data),
                                'sl': int(sl)
                            }
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到轻纺城数据-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 7)
            counter = counter + 1
#获取库存/港口数据  MEG发货统计
class meg_send_values(get_market_values):
    def parse_one_page(self, *params):
        # 获取库存/港口数据
        counter = 1
        while counter <= 2 :
            try:
                for j in ({'1'}):  # 从1到n页抓取数据
                    url = 'http://www.ccf.com.cn/newscenter/index.php?cur_row_pos=0&cur_pg_num=' + j + "&Class_ID=1C0000"
                    cookies = ast.literal_eval(params[0][3])
                    response = self.get_one_page(url, {}, [], cookies)
                    sleeptime = random.randint(10, 15)
                    print('\033[37;40m-------------------获取MEG发货统计url休眠', sleeptime, '秒------------------\033[0m')
                    time.sleep(sleeptime)
                    pattern = re.compile(
                        '<li(?: | class=articlebreak )><span>.*?href="(.*?)" class="h1a2" target="_blank" onmouseover="return overlib.*?>\d+月\d+日MEG发货统计</a></li>')  # 去掉re.S 不匹配换行符
                    items = re.findall(pattern, response)
                    for i in range(0, 3):  # len(items)
                        url = 'http://www.ccf.com.cn' + items[i]
                        data = re.findall('/newscenter/detail-1C0000-(.*?).shtml', items[i])[0][:8]  # 获取日期
                        data = datetime.datetime.strptime(data, '%Y%m%d') + datetime.timedelta(days=-1)  # 日期减少一天
                        data = data.strftime('%Y%m%d')  # 转换为yyyymmdd格式
                        response = requests.get(url, headers={}, cookies=cookies)
                        sleeptime = random.randint(30, 45)
                        print('\033[37;40m-------------------获取新一条MEG发货统计数据休眠', sleeptime, '秒------------------\033[0m')
                        time.sleep(sleeptime)
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
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到库存/港口数据-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 8)
            counter = counter + 1
# 获取库存/港口数据 MEG港口库存详细
class meg_stock_values(get_market_values):
    def parse_one_page(self, *params):
        # MEG港口库存详细
        counter = 1
        while counter <= 2 :
            try:
                for j in ({'1'}):  # 从1到n页抓取数据
                    url = 'http://www.ccf.com.cn/newscenter/index.php?cur_row_pos=0&cur_pg_num=' + j + "&Class_ID=1C0000"
                    cookies = ast.literal_eval(params[0][3])
                    response = self.get_one_page(url, {}, [], cookies)
                    sleeptime = random.randint(10, 15)
                    print('\033[37;40m-------------------获取MEG港口库存url休眠', sleeptime, '秒------------------\033[0m')
                    time.sleep(sleeptime)
                    pattern = re.compile(
                        '<li(?: | class=articlebreak )><span>.*?href="(.*?)" class="h1a2" target="_blank" onmouseover="return overlib.*?MEG港口库存.*?</a></li>')  # 去掉re.S 不匹配换行符
                    items = re.findall(pattern, response)
                    for i in range(0, 3):  # 暂时只取一日数据 len(items)
                        url = 'http://www.ccf.com.cn' + items[i]
                        data = re.findall('/newscenter/detail-1C0000-(.*?).shtml', items[i])[0][:8]  # 获取日期
                        response = requests.get(url, cookies=cookies)
                        sleeptime = random.randint(30, 45)
                        print('\033[37;40m-------------------获取新一条MEG港口库存数据休眠', sleeptime, '秒------------------\033[0m')
                        time.sleep(sleeptime)
                        response.encoding = 'gbk'
                        html2 = response
                        pattern2 = re.compile('<p(?:| style="text-indent: 2em;")>(?:CCF讯|受封航影响).*?今日华东主港地区(.*?)约(.*?)万吨.*?</p>')
                        items2 = re.findall(pattern2, html2.text)[0][1]
                        if items2 == []:
                            print('\033[1;37;41m----------------------MEG主港库存逻辑异常-----------------------\033[0m')
                        else:
                            yield {
                                'index': 'MEG主港库存',
                                'erdat': data,
                                'sl': items2
                            }
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到MEG港口库存数据-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 9)
            counter = counter + 1
#获取库存数据
class stock_load_values(get_market_values):
    def parse_one_page(self, *params):
        # kczs:CCF库存指数  292000/POY库存 290000/FDY库存 291000/DTY库存 280000/涤纶短纤库存
        # fhzs:CCG负荷指数  210000/PTA负荷 222000/MEG负荷(总) 223000/MEG煤制负荷 220000/聚酯负荷
        #                  230000/直纺长丝负荷 240000/直纺短纤负荷 274000/聚酯瓶片负荷
        # xyzs:CCF下游指数  110000/江浙纺机开机率 150000/江浙加弹开机率
        counter = 1
        while counter <= 2:
            try:
                sj = (['kczs', 292000], ['kczs', 290000], ['kczs', 291000], ['kczs', 280000],
                      ['fhzs', 210000], ['fhzs', 222000], ['fhzs', 223000], ['fhzs', 220000], ['fhzs', 230000],
                      ['fhzs', 240000], ['fhzs', 274000],
                      ['xyzs', 110000], ['xyzs', 150000])
                for l in range(0, len(sj)):
                    data = {
                        "ProdClass": sj[l][0],
                        "ProdID": sj[l][1],
                        "startDate": "2019-06-01",
                        "endDate": params[0][1]
                    }
                    url = 'http://www.ccf.com.cn/dynamic_graph/index.php'
                    cookies = ast.literal_eval(params[0][3])
                    response = self.post_one_page(url, {}, data, cookies)
                    sleeptime = random.randint(10, 15)
                    print('\033[37;40m-------------------获取库存数据休眠', sleeptime, '秒------------------\033[0m')
                    time.sleep(sleeptime)
                    pattern = re.compile(
                        '<tr .*?><td align=center>(.*?)</td>.*?<td align=center>(.*?)</td>.*?<td align=center>(.*?)</td>.*?<td align=center>(.*?)</td>.*?<td align=center>(.*?)</td></tr>',
                        re.S)
                    items = re.findall(pattern, response)
                    for item in items:
                        if item == []:
                            print('\033[1;37;41m----------------------总库存逻辑异常-----------------------\033[0m')
                        else:
                            yield {
                                'index': item[0],
                                'erdat': item[1].strip()[0:4] + item[1].strip()[5:7] + item[1].strip()[8:10],
                                'sl': item[2]
                            }
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到库存指数数据-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 10)
            counter = counter + 1
# 获取PTA流通环节库存
class pta_stock_values(get_market_values):
    _sqllist = []
    def parse_one_page(self, *params):
        zjson = {
            'pid': 79,
            'ptext': 'PTA%u6D41%u901A%u73AF%u8282',
            'date1': '2019-05',
            'date2': params[0][2]
        }
        counter = 1
        while counter <= 2:
            try:
                url = 'http://www.ccfei.com/Price/InventoryChart.aspx/GetData'
                cookies = ast.literal_eval(params[0][4])
                response3 = self.post_json_page(url, {}, zjson, cookies)
                a = response3.json()
                b = a["d"]
                c = json.loads(b)
                answer = c[1][0]
                for i in range(0, len(answer)):
                    x, y = answer[i][0], answer[i][2]
                    yield {
                        'index': 'PTA流通环节库存',
                        'erdat': y[:4] + y[5:7] + y[8:10],
                        'sl': x
                    }
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到PTA流通环节库存-----------------------\033[0m')
            counter = counter + 1
# 获取出口聚酯数据
class export_polyester(get_market_values):
    _sqllist = []
    _value_list = (
        {'id': '54022000',
        'product2': '%u6DA4%u7EB6%u5DE5%u4E1A%u4E1D',
        'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口涤纶工业丝'},
        {'id': '54023310',
        'product2': '%u6DA4%u7EB6DTY',
        'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口涤纶DTY'},
        {'id': '54023390',
         'product2': '%u5176%u4ED6%u6DA4%u7EB6DTY',
         'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口其他涤纶DTY'},
        {'id': '54024600',
         'product2': '%u6DA4%u7EB6POY',
         'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口涤纶POY'},
        {'id': '54024700',
         'product2': '%u6DA4%u7EB6FDY',
         'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口涤纶FDY'},
        {'id': '54025200',
         'product2': '%u5176%u4ED6%u6DA4%u7EB6%u957F%u4E1D',
         'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口其他涤纶长丝'},
        {'id': 'DLCS',
         'product2': '%u6DA4%u7EB6%u957F%u4E1D%28%u6C47%u603B%29',
         'product1': '%u6DA4%u7EB6%u957F%u4E1D',
         'name': '出口涤纶长丝汇总'},
        {'id': '55032000',
         'product2': '%u6DA4%u7EB6%u77ED%u7EA4',
         'product1': '%u6DA4%u7EB6%u77ED%u7EA4',
         'name': '出口涤纶短纤'},
        {'id': 'JZPP',
         'product2': '%u805A%u916F%u74F6%u7247',
         'product1': '%u805A%u916F%u539F%u6599',
         'name': '出口聚酯瓶片'},
        {'id': 'JZQP',
         'product2': '%u805A%u916F%u5207%u7247',
         'product1': '%u805A%u916F%u539F%u6599',
         'name': '出口聚酯切片'},
                  )

    def parse_one_page(self, *params, value_list = _value_list):
        for item in range(0, len(value_list)):
            zjson = {
                'id': value_list[item]['id'],
                'product2': value_list[item]['product2'],
                'product1': value_list[item]['product1'],
                'date1': '2019-10',
                'date2': params[0][2]
            }
            url = 'http://www.ccfei.com/Price/CustomsExport.aspx/GetData'
            cookies = ast.literal_eval(params[0][4])
            response3 = self.post_json_page(url, {}, zjson, cookies)
            a = response3.json()
            b = a["d"]
            c = json.loads(b)
            counter = 1
            while counter <= 2:
                try:
                    answer = c[1][0]
                    for i in range(0, len(answer)):
                        x, y= answer[i][0], answer[i][2]
                        yield {
                            'index': value_list[item]['name'],
                            'erdat': y[:4] + ('0'+ y[5:6]if re.search('月', y[5:7]) else y[5:7]) ,
                            'sl': x
                        }
                    break
                except:
                    if counter == 2:
                        print('\033[1;37;41m----------------------未取到%s-----------------------\033[0m' % value_list[item]['name'])
                counter = counter + 1
            sleeptime = random.randint(1, 4)
            time.sleep(sleeptime)
# 爬取长江有色钴锰价格
class cj_metal(get_market_values):
    def parse_one_page(self, *params):
        counter = 1
        while counter <= 2:
            try:
                for pagnum in {1}:
                    page = '&pos=%s&act=next&page=%s' % ((pagnum-1)*60,pagnum)
                    url = 'http://www.ometal.com/bin0/new/searchkey_cj.asp?type=%B3%A4%BD%AD%D3%D0%C9%AB%BD%F0%CA%F4%CF%D6%BB%F5&searchtype=&newsort=7'+ page
                    response = self.get_one_page(url, self._headers, [], [])
                    pattern = re.compile(
                                '<tr>[\s\S]*?<td align="left" class="s105">·[\s\S]*?<a href="(.*?)" target="_blank">'
                                '<span style="color:black;background-color:yellow">长江有色金属现货</span>.*?'
                                ,re.S)  # [\s\S]*?匹配包含换行的任意字符
                    items = re.findall(pattern, response)

                    for i in range(0, 5):  # 只爬取前五个页面
                        time.sleep(0.5)
                        url2 = 'http://www.ometal.com' + items[i]
                        response2 = self.get_one_page(url2, self._headers, [], [])
                        # html找不到钴或者电解锰，跳出本次循环
                        if response2.find('钴') == -1 or response2.find('电解锰') == -1 or response2.find('均价') == -1:
                            continue
                        html = etree.HTML(response2)
                        # 处理网页，方便正则匹配
                        response2 = response2.replace('&nbsp;',' ')
                        #  时间格式转换
                        day_ori= items[i][9:items[i].find('marketnew') - 1]
                        day = datetime.datetime.strptime(day_ori, '%Y/%m/%d').strftime('%Y%m%d')
                        #  爬取名称
                        key_values = {'1#钴': 11, '1#电解锰': 15}
                        for j in (11, 15):
                            if day > '20190110' and response2.find('吨') != -1:  # 2019年1月10日前并且含有单位吨按如下格式爬取，否则进入else循环
                                try:
                                    name_str = '//div[@id="fontzoom"]/table/tbody/tr[%s]/td[1]/p/text() | //*[@id="fontzoom"]/div/div/table/tbody/tr[%s]/td[1]/p/text() |' \
                                               '//div[@id="fontzoom"]/table/tbody/tr[%s]/td[1]/p/span[2]/text() | //div[@id="fontzoom"]/table/tbody/tr[%s]/td[1]/text() |' \
                                               '//div[@id="fontzoom"]/div/table/tbody/tr[%s]/td[1]/p/text() | //*[@id="fontzoom"]/table/tbody/tr[%s]/td[1]/p/strong/span/text()' % (
                                               j, j, j, j, j, j)
                                    sl_str = '//div[@id="fontzoom"]/table/tbody/tr[%s]/td[5]/p/text() | //*[@id="fontzoom"]/div/div/table/tbody/tr[%s]/td[5]/p/text() |' \
                                             '//div[@id="fontzoom"]/table/tbody/tr[%s]/td[5]/p/span/text() | //div[@id="fontzoom"]/table/tbody/tr[%s]/td[5]/text() |' \
                                             '//div[@id="fontzoom"]/div/table/tbody/tr[%s]/td[5]/p/text() | //*[@id="fontzoom"]/table/tbody/tr[%s]/td[5]/p/strong/span/text()' % (
                                             j, j, j, j, j, j)
                                    name = html.xpath(name_str)[0]
                                    sl = str(html.xpath(sl_str)[0]).replace(',', '')
                                    yield {
                                        'index': '1#钴' if j == 11 else '1#电解锰',
                                        'erdat': day,
                                        'sl': int(sl)
                                    }
                                except:
                                    name = list(key_values.keys())[list(key_values.values()).index(j)]
                                    pattern = re.compile(
                                        '''%s[\s\S]*?(?:.*?(?:mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"|mso-font-kerning: 0.0000pt; mso-spacerun: 'yes';")>){3}'''
                                        '''(.*?)[</span>]{1}''' % name
                                    , re.S)  # [\s\S]*?匹配包含换行的任意字符
                                    sl = str(re.findall(pattern, response2)[0]).replace(',', '')
                                    yield {
                                        'index': '1#钴'if j == 11 else '1#电解锰',
                                        'erdat': day,
                                        'sl': int(sl)
                                                }
                            elif day > '20190110' and response2.find('吨') == -1:
                                sl_str = '//div[@id="fontzoom"]/table/tbody/tr[%s]/td[4]/text()' % j
                                sl = str(html.xpath(sl_str)[0]).replace(',', '')
                                yield {
                                    'index': '1#钴' if j == 11 else '1#电解锰',
                                    'erdat': day,
                                    'sl': int(sl)
                                }
                            else:
                                try:
                                    name = list(key_values.keys())[list(key_values.values()).index(j)]
                                    pattern = re.compile(
                                        '''%s</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>''' % name
                                        , re.S)
                                    sl = str(re.findall(pattern, response2)[0][2]).replace(',', '')
                                    yield {
                                        'index': '1#钴'if j == 11 else '1#电解锰',
                                        'erdat': day,
                                        'sl': int(sl)
                                    }
                                except:
                                    try:
                                        if j == 11:
                                            name_str2 = '1# 钴'
                                        else:
                                            name_str2 = '1# 电解锰'
                                        pattern = re.compile('%s(?:</p></td><td.*?><p.*?>(.*?)){4}</p>' % name_str2, re.S)
                                        sl = str(re.findall(pattern, response2)[0]).replace(',', '')
                                        yield {
                                            'index': '1#钴'if j == 11 else '1#电解锰',
                                            'erdat': day,
                                            'sl': int(sl)
                                        }
                                    except:
                                        try:
                                            if j == 11:
                                                name_str2 = '1# 钴'
                                            else:
                                                name_str2 = '1# 电解锰'
                                            pattern = re.compile('%s(?:</td><td.*?>(.*?)){4}</td>' % name_str2, re.S)
                                            sl = str(re.findall(pattern, response2)[0]).replace(',', '')
                                            yield {
                                                'index': '1#钴'if j == 11 else '1#电解锰',
                                                'erdat': day,
                                                'sl': int(sl)
                                            }
                                        except:
                                            if j == 11:
                                                name_str2 = '钴'
                                            else:
                                                name_str2 = '电解锰'
                                            pattern = re.compile('%s</span></p>(?:</td><td.*?><p>(.*?)</p>){4}' % name_str2, re.S)
                                            sl = str(re.findall(pattern, response2)[0]).replace(',', '')
                                            yield {
                                                'index': '1#钴'if j == 11 else '1#电解锰',
                                                'erdat': day,
                                                'sl': int(sl)
                                            }
                break
            except:
                if counter == 2:
                    print('\033[1;37;41m----------------------未取到钴与电解锰价格数据-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 11)
            counter = counter + 1
# 爬取冰醋酸价格
class icis_price(get_market_values):
    _sqllist = []
    def parse_one_page(self, *params):
        data = {
            '__RequestVerificationToken':params[0][5][1],
            'StartDate': str(params[0][0]).replace('-', '/'),
            'EndDate': str(params[0][1]).replace('-', '/'),
            "FrequencyCode": "Daily",
            "IncludePrePublishedPrices": "false",
            "SelectedQuotes[0][Id]": "{i}petchem/8602792",
            "SelectedQuotes[0][PriceOption]": "Average",
            "SelectedQuotes[0][UsePrimaryYAxis]": "true",
            "PrimaryYAxisUnitCode": "ZZZ",
            "PrimaryYAxisCurrencyCode": "ZZZ",
            "SecondaryYAxisUnitCode": "ZZZ",
            "SecondaryYAxisCurrencyCode": 'ZZZ',
            "isFormulaRequest": "false",
            "preEntitledWorkspaceName":'',
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
            "X-Requested-With": "XMLHttpRequest",
        }
        counter = 1
        while counter <= 2:
            try:
                url = 'https://www.icis.com/Dashboard/PurchasedPriceHistory/DisplayChartDualYAxis'
                response3 = requests.post(url, data=data, headers=headers, cookies=params[0][5][0], timeout=120)
                a = response3.json()
                c = a['chartLines'][0]['pointList']
                for i in range(0, len(c)):
                    x, y = c[i]['pointPrice'], c[i]['pointDateString'].replace('-','')
                    yield {
                        'index': '冰醋酸中间价',
                        'erdat': str(y),
                        'sl': x
                    }
                break
            except:
                if counter == 2 :
                    print('\033[1;37;41m----------------------未取到冰醋酸中间价-----------------------\033[0m')
                    wechat_auto().send_mesg(0, 'person', 12)
            counter = counter + 1

def main():
    try:
        # 定义today为当前日期 ny为年月
        today = datetime.date.today().strftime('%Y-%m-%d')
        ny = datetime.date.today().strftime('%Y-%m')
        yeday = datetime.datetime.strptime(today, '%Y-%m-%d') + datetime.timedelta(days=-4)
        yeday = yeday.strftime('%Y-%m-%d')
        # 设定传递参数，依次为昨日，今日和年月
        ccf_cookie = str(get_market_values().ccf_cookie())
        ccfei_cookie = str(get_market_values().ccfei_cookie())
        icis_cookie = get_market_values().icis_cookie()

        param = [yeday, today, ny, ccf_cookie, ccfei_cookie, icis_cookie]
        sqltuple = get_market_values().parse_concurrent(param)
        # 定义连接，并插入数据
        conn = get_connection().hana_connection()
        ins_sql = '''insert into"COMMON"."XFM_MARKT" (ZB , ERDAT ,SPJ) values ('%s','%s',%s)'''
        sql().sql_req(conn, tuple(sqltuple), sql=ins_sql)
        get_connection().close_connection(conn)
    except Exception as e:
        print(e)
        wechat_auto().send_mesg(0, 'person', 13)
if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print("Time used:", end - start)