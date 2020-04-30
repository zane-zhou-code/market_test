from selenium import webdriver
import time
import requests

#selenium能在登陆的时候,获取cookie,同时也能执行各种js

driver = webdriver.Chrome()
driver.get('https://weibo.com')
time.sleep(20)

driver.find_element_by_id('loginname').send_keys('13760214167')
driver.find_element_by_name('password').send_keys('ZhouHao0512')

driver.find_element_by_class_name('W_btn_a').click()
time.sleep(4)

# 页面的获取使用driver.page.source
if '请输入验证码'in driver.page_source:
    img_ele = driver.find_element_by_xpath('//a[@class="code W_fl"]/img')
    img_link = img_ele.get_attribute('src')
    response = requests.get(img_link)
    with open('验证码.jpg', 'wb')as f:
        f.write(response.content)

    input_src = input('请输入验证码')  # 需要自己输入验证码
    driver.find_element_by_name('verifycode').send_keys(input_src)
    driver.find_element_by_class_name('W_btn_a').click()

time.sleep(20)
cookie_list = driver.get_cookies()
print(cookie_list)

cookie_item_str_list = []
for cookie_item in cookie_list:
    name = cookie_item['name']
    value = cookie_item['value']
    cookie_item_str = name + '=' + value
    cookie_item_str_list.append(cookie_item_str)

cookie_str = ';'.join(cookie_item_str_list)
print(cookie_str)
driver.quit()
# .strip()去掉空格
# 拼接用urljoin
# 解耦合------------------------------------------------------------
## url_function_list = [(url, get_all_province)]
# 添加代理
# queue = Manager().Queue()
# queue.put((url, get_all_province))
# pool = Pool(6)
# res_list = []
# while True:
#     try:
#            url,func = queue.get(timeout=5)
#     except:
#         break
##           url,func = url_function_list.pop(0)# pop(-1)从后向前取
#     res = pool.apply_async(func=func, args=(url, queue)# url_function_list)
#     res_list.append(res)

##     ret = func(url, url_function_list)  # 这是根据自己写的参数来的
##    if ret:
##         print(ret)

#      for res in res_list:
#          ret = res.get()
#          if ret:
#              print(ret)
#      pool.close()
#      pool.join()
# 进程不共享空间,线程共享空间(调用manage)
#------------------------------------------------------------------
