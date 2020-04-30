from selenium import webdriver
from 接口.setting import fixed_params,wechat_auto
import time,os
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.ie.options import Options as IOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pdfplumber
import pandas as pd
import re

yesterday2 = fixed_params().yesterday_l
yesterday = fixed_params().yesterday

def ie_autoload():
    ie_option = IOptions()
    # 设置隐藏模式
    ie_option.add_argument('--disable-gpu')
    ie_option.add_argument('--no-sandbox')
    ie_option.add_argument('--disable-dev-shm-usage')
    ie_driver = webdriver.Ie(options=ie_option)
    # 登陆网页保存cookie
    try:
        url1 = 'https://auth.xfmgroup.com/cas/login?' \
               'service=http%3a%2f%2fmes.xfmgroup.com%2fWebUI%2fIPWeb%2f'
        ie_driver.get(url1)
        time.sleep(5)
        ie_driver.find_element_by_xpath('//*[@id="fm1"]/div/div[3]/input[4]').click()
        time.sleep(5)
        # 进入需要计算的页面
        url2 = 'http://fbbb.xfmgroup.com/FBBB/Integrates/DispatcherIn.aspx?' \
               'funcid=00010013&DATE=%s' % yesterday2
        ie_driver.get(url2)

        # 等待frame/left加载出来
        WebDriverWait(ie_driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//frame[@name="left"]')))
        ie_driver.switch_to.frame('left')
        time.sleep(1)
        ie_driver.find_element_by_id('btnCompute').click()

        # 等待计算按钮重新加载出来
        WebDriverWait(ie_driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//input[@id="btnCompute"]')))

        # 结束
        ie_driver.quit()
    except:
        # 异常退出
        ie_driver.quit()
        wechat_auto().send_mesg(0, 'person', 5)

def chrome_autoload():
    chrome_option = COptions()
    file_dir = 'D:\\各装置主要生产日指标汇总'
    # 设置隐藏模式
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': file_dir} #设置为0，禁止弹出窗口
    chrome_option.add_experimental_option('prefs', prefs)
    chrome_option.add_argument('--headless')
    chrome_driver = webdriver.Chrome(options=chrome_option)
    try:
        # 登陆网页
        url2 = 'http://192.168.2.81:8080/BOE/OpenDocument/opendoc/openDocument.jsp?sIDType=CUID' \
               '&iDocID=AcoYQKP5WQlNng0bCsVeAcw&lsSERDAT=%s' % yesterday
        chrome_driver.get(url2)
        time.sleep(1)
        chrome_driver.find_element_by_id('_id0:logon:USERNAME').send_keys('BI_USER')
        chrome_driver.find_element_by_id('_id0:logon:PASSWORD').send_keys('Xfm@2019')
        chrome_driver.find_element_by_id('_id0:logon:logonButton').click()

        # 等待切换到opendoc框架，并等待出现webi框架，然后切换到webi框架
        WebDriverWait(chrome_driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//iframe[@id="openDocChildFrame"]')))
        chrome_driver.switch_to.frame('openDocChildFrame')

        WebDriverWait(chrome_driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//iframe[@id="webiViewFrame"]')))
        chrome_driver.switch_to.frame('webiViewFrame')

        # 等待直到加载完毕(标志是visibility是否由visible转换为hidden)
        try:
            WebDriverWait(chrome_driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='modal_waitDlg' and contains(@style,'visibility: hidden')]")))
        except Exception as e:
            print(e, '运行等待超时')

        # 开始下载文件并改名
        try:
            chrome_driver.find_element_by_id('ariaLabelledBy_alertDlg')
            chrome_driver.quit()
            return '未成功计算'
        except:
            try:
                # 等待页面加载完毕可点击,点击
                WebDriverWait(chrome_driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="_dhtmlLib_270"]')))
                chrome_driver.find_element_by_id('_dhtmlLib_270').click()

                # 等待下载框弹出,点击
                WebDriverWait(chrome_driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="check_SelectAllReport"]')))
                chrome_driver.find_element_by_id('check_SelectAllReport').click()
                time.sleep(3)

                chrome_driver.find_element_by_id('check_1783').click()
                time.sleep(3)
                chrome_driver.find_element_by_id('BtnCImg_OK_BTN_idExportDlg').click()
                time.sleep(20)
                old_dir = file_dir + '\各装置主要生产日指标汇总.pdf'
                new_dir = file_dir + '\%s 各装置主要生产日指标汇总表.pdf' % yesterday
                if os.path.exists(new_dir):
                    os.remove(new_dir)
                    time.sleep(1)
                    os.rename(old_dir, new_dir)
                else:
                    os.rename(old_dir, new_dir)
            except:
                chrome_driver.quit()
                return '未成功计算'
        # 结束
        chrome_driver.quit()
        return '下载完成'
    except:
        # 异常退出
        chrome_driver.quit()
        wechat_auto().send_mesg(0, 'person', 4)
        return '异常退出'

def question_search(date):
    file_dir = 'D:\\各装置主要生产日指标汇总'
    path = file_dir + '\%s 各装置主要生产日指标汇总表.pdf' % date
    # 定义pdf页数，并读取当页表格
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        for table in first_page.extract_tables():  # 这个pdf暂时只有一张表
            df = pd.DataFrame(table[5:])
            values = df.values  # 获取每行值
            for i in range(0, len(values)):
                if re.search(str(values[i]), '#'):  # 查找是否出现#字符
                    wechat_auto().send_mesg(0, 'person', 0)
                    return '出现特殊字符'
        return '未出现特殊字符'

if __name__ == '__main__':
    ie_autoload()
    time.sleep(1)
    response = chrome_autoload()
    i = 1  # 计算5次，若5次都失败，退出
    while response=='未成功计算'and i<=4:
        print('\033[37;40m---------------这是第%s次调用chrome-----------------\033[0m' % (i+1))
        ie_autoload()
        time.sleep(1)
        response = chrome_autoload()
        i = i+1
    # 若连续五次计算都失败,发送消息检查代码
    if i ==5:
        wechat_auto().send_mesg(0, 'person', 3)
    # 调用检测函数
    try:
        question = question_search(yesterday)
        print(question)
    except:
        print('未发现需检查文档')

