import pandas as pd
from WindPy import *
import pyhdb
from sqlalchemy import create_engine
import datetime,time
import os

# DataFrame.to_sql(name, con, schema=None,
# if_exists='fail', index=True, index_label=None,
# chunksize=None, dtype=None, method=None)
# engine = create_engine('dialect+driver://username:password@host:port/database')
# dialect -- 数据库类型
# driver -- 数据库驱动选择
# username -- 数据库用户名
# password -- 用户密码
# host 服务器地址
# port 端口
# database 数据库
engine = create_engine('hana+pyhdb://XHZHOU:Zhou1234@192.168.2.192:30241')
df = pd.DataFrame({'SECID': ['M0000005'], 'TRADEDATE':
                   ['20190911'], 'OPENPRICE': [54.84]})
with engine.connect()as conn:
     #df.to_sql(name='''"XHZHOU"."CS" ''',con=conn,if_exists='append',index=False, index_label='SECID,TRADEDATE')
    #rst = conn.execute('''SELECT * FROM "XHZHOU"."CS"''')

    #for row in rst:
    #    print(row)
    exit()



w.start()
stock = w.wsd('300059.SZ','close','20190909', '20190909',"Fill=Previous")
data1=w.wset('SectorConstituent','sectorId=a001010100000000;field=wind_code')#获取所有A股数据
print(stock)
index_data = pd.DataFrame()
index_data['trade_date']=stock.Times
index_data['stock_code']=stock.Codes[0]
index_data['close']=stock.Data[0]
#print(index_data)
#print(index_data.values)
print(data1.Data[0])



class WindStock():

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def AStockHisData(self, symbols, start_date, end_date, step=0):
        '''
        逐个股票代码查询行情数据
        wsd代码可以借助 WindNavigator自动生成copy即可使用;时间参数不设，默认取当前日期，可能是非交易日没数据;
        只有一个时间参数时，默认作为为起始时间，结束时间默认为当前日期；如设置两个时间参数则依次为起止时间
        '''
        print(self.getCurrentTime(), ": Download A Stock Starting:")
        for symbol in symbols:
            w.start()
            try:
                stock = w.wsd('300059.SZ','close','20190909', '20190909',"Fill=Previous")
                print(stock)
                index_data = pd.DataFrame()
                index_data['trade_date'] = stock.Times
                stock.Data[0] = symbol
                index_data = index_data[index_data['open'] > 0]
            except Exception as e:
                continue
            print(stock)