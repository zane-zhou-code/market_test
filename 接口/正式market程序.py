from WindPy import *
from 接口.setting import get_connection,sql,fixed_params
import numpy as np

def main():
    # w.wsd：获取历史序列数据
    # w.wsi：获取分钟数据 data= w.wsi(品种代码,指标,开始时间,结束时间,可选参数)；
    # w.wst：获取日内tick级别数据 data= w.wst(品种代码,指标,开始时间,结束时间,可选参数)
    # w.wss：获历史截面数据 data= w.wss(品种代码,指标,可选参数)
    # w.wsq：获取和订阅实时行情数据 data=w.wsq(品种代码,指标,可选参数,回调函数)
    # w.wset：获取板块、指数等成分数据 data=w.wset(数据集名称,可选参数)
    # w.weqs：获取条件选股结果 data= w.weqs(filtername,…)
    # w.wpf：获取资产管理、组合管理数据 data=w.wpf(产品名，数据表名,可选参数)
    # w.tlogon交易登录 data = w.tlogon(BrokerID, DepartmentID, LogonAccount, Password, AccountType,...)
    w.start()
    w.isconnected()  # 即判断WindPy是否已经登陆成功
    conn = get_connection().hana_connection()

    # 定义执行语句与所取参数
    # 自定义data存储所需行业数据 美原油期货/布伦特期货/石脑油:CFR日本/PX:CFR中国主港/MX:FOB韩国/醋酸:山东/乙烯:CFR东北亚/甲醇:华东地区
    #                           MEG外盘/PTA外盘/PTA主力期货
    # 存储所需PTA及EG各期数据 PTA主力收盘价/PTA一月/PTA三月/PTA五月/PTA七月/PTA九月/PTA十一月/EG一月/EG五月/EG六月/EG九月
    data = [['M0000005', 'S0031525', 'S5428960', 'S5432004', 'S5419003', 'S5439491', 'S5400549',
             'S5470115', 'S0181381', 'M0000186', 'M0000188',
             'TA.CZC', 'TA01M.CZC', 'TA03M.CZC', 'TA05M.CZC', 'TA07M.CZC', 'TA09M.CZC', 'TA11M.CZC',
             'EG01M.DCE', 'EG05M.DCE', 'EG06M.DCE', 'EG09M.DCE', 'S0266311',
             'M0066316', 'M0000185', 'S5446052', 'S0049499','S5400548','S5400550','S5140506','S0069597','S5419004',
             'M0096870','M0331299','M0017138',

             'M0017126', 'M0000138', 'M5567889', 'M0012303', 'M5528818', 'M5543249', 'M5206730',
             'M5525755', 'M0001384', 'M0290205', 'G0000001', 'G1503455', 'G8405271',
             'G0008071', 'G0006148', 'G0000027', 'G1500813', 'G1400631', 'G0006148', 'G0000027',
             'G1500813', 'G1400631', 'G0006243', 'G0002323', 'G1500013', 'G1400007', 'G0006318',
             'G0008060', 'G8405269', 'G8405314', 'G0002325', 'G1137704', 'G1109369',
             'S0049499', 'S0049521', 'S5401631', 'S5404287', 'S5402198', 'S5404854',
             'S0027307', 'S5401186', 'S0071220', 'S5439164', 'S5439171', 'S5439172',
             'S0028007', 'S0106137', 'S0070115', 'S0070116', 'S0070117', 'S0070118',
             'S0070130', 'S0070136', 'S0070138', 'S5319442', 'S5319443', 'S5319444',
             'S5319446', 'S5319447', 'S5319448',
             'S0049638', 'S0049656', 'S0049668', 'S0049707', 'S0049722',
             'S0049641', 'S0049644', 'S0049647', 'S0049650', 'S0049653',
             'S0049659', 'S0049662', 'S0049665', 'S0049671', 'S0049674', 'S0049677',
             'S0049680', 'S0049683', 'S0049686', 'S0049689', 'S0049692', 'S0049710',
             'S0049713', 'S0049716', 'S0049719', 'S0049725', 'S0049728', 'S0049731',
             'S0049766', 'S0049772', 'S0049784', 'S0049790', 'S0049796',

             'G1112986', 'G0007980', 'G0008073', 'G0006147', 'S5431567', 'S5440395', 'S5416997',
             'M0017139', 'M0017140', 'M0017141', 'M0017142', 'M0017143', 'M0017144', 'M0017145',

             'S5470327', 'S5422007', 'S5440460', 'S0182141', 'S5456800',
             ], ]  # 27个行业数据 + 97个新增数据
    sel_sql = '''
    select ifnull(to_char(add_days(current_date,-3),'yyyy-mm-dd'),'1995-01-01')
    from dummy
    '''
    del_sql = '''
    delete from"COMMON"."XFM_MARKT"
    where erdat='%s'
    and zb in %s ''' % ('%s', str(tuple(data[0])))
    ins_sql = '''
    insert into"COMMON"."XFM_MARKT" (ZB , ERDAT ,SPJ)values ('%s','%s',%s)
    '''
    # 取表中最大日期后一天，与系统前一天日期
    results = sql().sql_req(conn, sql=sel_sql)
    table_mer = results[0][0]
    yesterday = fixed_params().yesterday
    yesterday_l = fixed_params().yesterday_l
    sql().sql_req(conn, yesterday, sql=del_sql)

    for j in range(0, len(data[0])):  # 循环27个行业数据
        print("\n\n-----第 %i 次通过edb来提取 %s 收盘价数据-----\n" % (j, str(data[0][j])))
        edbdata = w.edb(str(data[0][j]), table_mer, yesterday_l, "Fill=Previous")
        if edbdata.ErrorCode != 0:
            continue
        print(edbdata)
        for i in range(0, len(edbdata.Times)):  # 循环所有日期数据
            sqllist = []
            sqllist.append(str(edbdata.Codes[0]))  # 插入code数据
            print(sqllist)
            sqllist.append(edbdata.Times[i].strftime('%Y%m%d'))  # 插入日期数据
            for k in range(0, len(edbdata.Fields)):  # 循环所有获取数据（这里只有收盘价）
                sqllist.append(edbdata.Data[k][i])  # 插入收盘价数据
            if sqllist[2]is None or np.isnan(sqllist[2]):  # 判断是否为NAN,是则进入下个日期循环
                continue
            sqltuple = tuple(sqllist)
            print(sqltuple)
            sql().sql_req(conn, sqltuple, sql=ins_sql)
    get_connection().close_connection(conn)

if __name__ == '__main__':
    main()