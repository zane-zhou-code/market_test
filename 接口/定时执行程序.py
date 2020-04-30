import random
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

# 提取市场部数据
def timeTask():
    os.system("D:\production\接口\正式market程序.py")
# print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
# ccf爬取市场部展示数据
def timeTask2():
    os.system("D:\production\接口\爬取数据源--使用requests.py")
# 执行HANA流程链
def timeTask3():
    os.system("D:\production\接口\hana处理链.py")
# MES定时执行计算并下载报表
def timeTask4():
    os.system("D:\production\接口\SC-Autoload.py")
# 定时发送邮件--各装置主要生产日指标报表
def timeTask5():
    os.system("D:\production\接口\SC_Send_emails.py")
# 定时推送生产报表
def timeTask6():
    os.system("D:\production\接口\SC_Send_files.py")
# 定时间内随机执行爬取CCF网页
def action():
    scheduler.remove_job('ccf_schedule')
    amh = random.randint(9, 12)
    pmh = random.randint(18, 21)
    min = random.randint(0, 60)
    hor = '%s,%s' %(amh, pmh)
    print('\033[37;40m-----------------爬虫程序预计执行时间 %s点 %s分------------------\033[0m'% (hor, min))
    scheduler.add_job(timeTask2, 'cron', hour=hor, minute=min, start_date='2019-10-20', id='ccf_schedule')
if __name__=='__main__':
    scheduler=BackgroundScheduler()
    scheduler.add_job(timeTask,'cron',hour='6-10,13,17', minute='30', start_date='2019-10-03')
    # scheduler.add_job(timeTask2, 'cron', hour='6-10,17', minute='35', start_date='2019-10-20')
    scheduler.add_job(timeTask2, 'cron', year='2019', hour='12', minute='30', id='ccf_schedule')
    scheduler.add_job(action, 'cron', hour='8', minute='55', start_date='2020-01-04')

    scheduler.add_job(timeTask3, 'cron', hour='1,13,21,23', minute='40', start_date='2019-10-24')
    scheduler.add_job(timeTask4, 'cron', hour='12,14', start_date='2020-01-15')
    scheduler.add_job(timeTask5, 'cron', hour='13', minute='30', start_date='2020-01-15')
    scheduler.add_job(timeTask6, 'cron', hour='13', minute='45', start_date='2020-02-24')
    scheduler.start()

    while True:
        # 显示蓝底白字
        print('\033[37;44m执行时间--------------------------------------------'+time.ctime().strip()+'\033[0m')
        #print(scheduler.get_jobs())
        time.sleep(240)

