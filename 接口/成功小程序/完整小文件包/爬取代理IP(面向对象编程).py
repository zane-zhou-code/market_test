import requests
from lxml import etree
from multiprocessing import Pool

class GetProxy(object):

    def get_all_proxy(self):
        assert(0)

    # 核实代理IP是否可用
    def validate_proxy(self, proxy_str):
        url = 'http://www.baidu.com'
        proxy = {
            'http': proxy_str,
            'https': proxy_str
        }
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            print('这个proxy可用', proxy)
            return proxy
        except:
            print('这个proxy不可用')
            return None

    # 定义并发作业 1.生成进程池的类(能够重用进程,能够限制进程的数量)
    #             2.将任务设置进入进程池
    #             3.进程池关闭
    #             4.等待所有进程结束
    def validate_proxy_concurrent(self):
        pool = Pool(50)
        # 接受进程池的返回值
        res_list = []
        for proxy in self.get_all_proxy():
            res = pool.apply_async(func=self.validate_proxy, args=(proxy,))
            res_list.append(res)
        # 获取返回值
        good_proxy_list = []
        for res in res_list:
            good_proxy = res.get()
            if good_proxy:
                good_proxy_list.append(good_proxy)
        pool.close()
        pool.join()
        return good_proxy_list

class GetXicidailiProxy(GetProxy):
    # 获取西刺代理所有IP
    def get_all_proxy(self):
        url = 'https://www.xicidaili.com/nn/'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
        response = requests.get(url, headers =headers)
        html_ele = etree.HTML(response.text)
        tr_ele_list = html_ele.xpath('//table[@id="ip_list"]/tr')  # 获取id为ip_list的所有tr
        tr_ele_list = tr_ele_list[1:]
        for tr_ele in tr_ele_list:
            ip = tr_ele.xpath('./td[2]/text()')[0]  # 获取第二个td的内容(text)
            port = tr_ele.xpath('./td[3]/text()')[0]  # 获取第三个td的内容(text)
            proxy_str = 'http://' + ip + ':' + port   # 获取IP地址
            yield proxy_str

if __name__ == '__main__':
    import time
    start_time =time.time()
    xici_proxy = GetXicidailiProxy()
    good_proxy_list = xici_proxy.validate_proxy_concurrent()
    print('所有好用的porxy是:', good_proxy_list)
    end_time = time.time()
    print('总的时间是:', str(end_time-start_time))


