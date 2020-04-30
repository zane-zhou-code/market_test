from WindPy import *
import cx_Oracle
import numpy as np
from IDE.接口.setting import get_connection
import pandas as pd
#cur.execute：执行单条sql语句
#cur.executemany：执行多条sql语句

conn = get_connection().oracle_connection('192.168.2.74','1521','c##XFM_TARGET','Xfm#2020','orcl')


cursor = conn.cursor()# 使用cursor()方法获取操作游标


result=cursor.execute('''
    select dim_id,erdat,close_price
    from DIM_MARKET_PRICE
    where dim_id='617100'
    and erdat between '20190401'and'20200410'
''')#使用execute方法执行SQL语句

all_data=cursor.fetchall()#获取所有数据
print(all_data)
df = pd.DataFrame(all_data, columns=['aaa', 'erdat', 'ccc'])  # columns=['指标ID', '日期', '价格']
df['erdat'] = pd.to_datetime(df['erdat'])

df = df.set_index(df['erdat'].values)
df.plot()
print(df['2020'].head(2))
df2 = round(df.iloc[0:, 2].mean(), 3)
# for i in range (0, len(df)):
#     df['环比'][i] = df['价格'].diff()
df['环比'] = round(df.ccc.pct_change(), 3)
df['同比数据'] = df.ccc.pct_change(12)
# df['ddd'] = df.ccc.shift()




print(df)
# print(df2)
# print(df['2020'].head())


# w.start();
# w.isconnected()  # 即判断WindPy是否已经登陆成功
# #
# #
# # #TA.CZC
# #
# #
# # #data = w.edb("M0000005,S0031525,S5428960,S5432004,S5400548,S5439491,S5400549,S5422062,S5435639,S5435641,S0181381,", "2019-09-04", "2019-09-05", "Fill=Previous")
# # #data2 = w.wsi("TA.CZC,TA01M.CZC,TA03M.CZC,TA05M.CZC,TA07M.CZC,TA09M.CZC,TA11M.CZC,EG01M.DCE,EG05M.DCE,EG06M.DCE,EG09M.DCE","close","2019-09-04 21:00:00")# 取PTA收盘价等信息
# # #data2 = w.wsd("TA.CZC,TA01M.CZC,TA03M.CZC,TA05M.CZC,TA07M.CZC,TA09M.CZC,TA11M.CZC,EG01M.DCE,EG05M.DCE,EG06M.DCE,EG09M.DCE","close","2019-09-04", "2019-09-04", "Fill=Previous")
# # '''
# # data2 = w.wsi("600000.SH","close,amt","2019-09-06 9:00:00")#取浦发银行分钟收盘价等信息
# # data3 = w.wss("600000.SH,000001.SZ","eps_ttm,orps,surpluscapitalps","rptDate=20190601")
# # data4 = w.wset("SectorConstituent",u"date=20190906;sector=全部A股")#取全部A股股票代码、名称信息
# # '''
# #  #print(data)
# # #print(data2)
# #
# # # 自定义data1存储所需行业数据 美原油期货/布伦特期货/石脑油:CFR日本/PX:CFR中国主港/MX:FOB韩国/醋酸:山东/乙烯:CFR东北亚/甲醇:华东地区
# #                              #MEG外盘/PTA外盘/PTA主力期货
# # # 自定义data2存储所需PTA各期数据 PTA主力收盘价/PTA一月/PTA三月/PTA五月/PTA七月/PTA九月/PTA十一月/EG一月/EG五月/EG六月/EG九月
# data=[['M0000005','S0031525','S5428960','S5432004','S5400548','S5439491','S5400549','S5422062','S5435639','S5435641','S0181381',
#          'TA.CZC','TA01M.CZC','TA03M.CZC','TA05M.CZC','TA07M.CZC','TA09M.CZC','TA11M.CZC','EG01M.DCE','EG05M.DCE','EG06M.DCE','EG09M.DCE','EG.DCE','M0067855','M0000185','S5446052','S0049499'],]#27个行业数据
# # data2=[['TA.CZC','TA01M.CZC','TA03M.CZC','TA05M.CZC','TA07M.CZC','TA09M.CZC','TA11M.CZC','EG01M.DCE','EG05M.DCE','EG06M.DCE','EG09M.DCE','EG.DCE','M0067855','M0000185','S5446052','S0049499'],]#16个合约数据
# # print(len(data1[0]))
# #
# for j in range(0,len(data[0])):#循环27个行业数据
#     print("\n\n-----第 %i 次通过edb来提取 %s 收盘价数据-----\n" % (j, str(data[0][j])))
#     edbdata = w.edb(str(data[0][j]), '2019-9-1','2019-9-10', "Fill=Previous")
#     if edbdata.ErrorCode!=0:
#         continue
#     print(edbdata)
#     for i in range(0,len(edbdata.Times)):#循环所有日期数据
#         sqllist = []
#         sqltuple = ()
#         sqllist.append(str(edbdata.Codes[0]))#插入code数据
#         print(sqllist)
#         sqltuple = tuple(sqllist)
#         if len(edbdata.Times)>=1:
#           sqllist.append(edbdata.Times[i].strftime('%Y%m%d'))#插入日期数据
#         for k in range(0, len(edbdata.Fields)):#循环所有获取数据（这里只有收盘价）
#             sqllist.append(edbdata.Data[k][i])#插入收盘价数据
#         if np.isnan(sqllist[2]):#判断是否为NAN,是则进入下个日期循环
#             continue
#         sqltuple = tuple(sqllist)
#         print(sqltuple)
#         try:
#             cursor.execute('insert into scott.zcat values(:id ,:erdat ,:drj)',sqltuple)
#         except:
#             continue
#     conn.commit()
# conn.close()
