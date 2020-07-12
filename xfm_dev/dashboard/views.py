from django.shortcuts import render
from .models import Destination,Backgroudpc
from django.http import HttpResponse, JsonResponse
import pyhdb,cx_Oracle
# from ...接口.setting import get_connection
import pandas as pd
from django.utils import six
import json,datetime
from rest_framework import viewsets
# from dashboard.serializer import BookSerializer

# Create your views here.
def index(request):
    dests = Destination.objects.all()
    backgs = Backgroudpc.objects.all()

    return render(request, 'index.html', {'dests':dests,'backgs':backgs})

def base(request):
    return render(request, 'base.html')

def sql_result(sql):
    dbcon = pyhdb.connect(host='192.168.2.192', port='30241',
                          user='XHZHOU', password='Zhou1234')
    df = pd.read_sql_query(sql, dbcon)
    return df

def ora_result(sql):
    dbcon = cx_Oracle.connect('c##XFM_TARGET/Xfm#2020@192.168.118.146:1521/PBOPDB')
    df = pd.read_sql_query(sql, dbcon)
    return df

def echarts(request):
    sql1 = '''
    select distinct b.ms,a.zb
    from"COMMON"."XFM_MARKT"a,
    "COMMON"."XFM_MARKTDZB"b
    where a.zb=b.zb
    '''
    df1 = sql_result(sql1)

    mselect_dict = {}
    for index, row in df1.iterrows():
        mselect_dict[row.MS] = {}
        mselect_dict[row.MS]['select'] = row.ZB
    zb = 'S5431567'
    sql2 = '''select zb,erdat,spj
             from"COMMON"."XFM_MARKT"
            where zb='S5431567'
            order by erdat
          '''
    df = sql_result(sql2)

    dates = list(df.ERDAT)
    prices = list(df.SPJ)
    return render(request, 'echarts.html', {'dates':dates,'prices':prices,'id':zb,'mselect_dict':mselect_dict})

def echarts2(request):
    sql1 = '''
        select distinct b.ms,a.zb
        from"COMMON"."XFM_MARKT"a,
        "COMMON"."XFM_MARKTDZB"b
        where a.zb=b.zb
        '''
    df1 = sql_result(sql1)

    mselect_dict = {}
    for index, row in df1.iterrows():
        mselect_dict[row.MS] = {}
        mselect_dict[row.MS]['select'] = row.ZB
    zb = 'S5431567'
    sql2 = '''select zb,erdat,spj
                 from"COMMON"."XFM_MARKT"
                where zb='S5431567'
                order by erdat
              '''
    df = sql_result(sql2)

    dates = list(df.ERDAT)
    prices = list(df.SPJ)
    aaa = 'base.html'
    bbb = 'main2'
    return render(request, 'echarts2.html', {'dates': dates, 'prices': prices, 'id': zb, 'mselect_dict': mselect_dict,
                                             'aaa':aaa,'main':bbb})

def echarts3(request):
    today = (datetime.datetime.strptime(datetime.date.today().strftime('%Y%m%d'), '%Y%m%d') +
            datetime.timedelta(days=-1)).strftime('%Y%m%d')
    today_c = (datetime.datetime.strptime(datetime.date.today().strftime('%Y%m%d'), '%Y%m%d') +
             datetime.timedelta(days=-1)).strftime('%Y-%m')
    dim_id = '618100'
    sql2 = '''
    select a.dim_id,a.erdat,a.close_price,b.dim_def
    from dim_market_price a,
        dim_market_id b
    where a.dim_id=b.dim_id
    and a.dim_id = '%s'
    and substr(erdat,1,6)=substr('%s',1,6)
    '''% (dim_id, today)
    df2 = ora_result(sql2)

    dates = list(df2.ERDAT)
    prices = list(df2.CLOSE_PRICE)

    return render(request, 'echarts3.html', {'dates': dates, 'prices': prices, 'id': 'POY价格', 'month':today_c})
def select_query(request):
    sql1 = '''
    select dim_id,dim_def
    from dim_market_id
    '''
    df1 = ora_result(sql1)
    mselect_dict = {}
    for index, row in df1.iterrows():
        mselect_dict[row.DIM_ID] = row.DIM_DEF
    list = eval(str(mselect_dict))
    return HttpResponse(json.dumps(list, ensure_ascii=False), content_type="application/json charset=utf-8")
def market_dates(request):
    form_dict = dict(six.iterlists(request.GET))
    bmonth = form_dict['START_time'][0].replace('-', '')
    emonth = form_dict['END_time'][0].replace('-', '')
    prices_n, zzb, zid_fuc= {}, [], []
    df1 = pd.DataFrame([], columns=['erdat'])
    for i in range(0, len(form_dict['DIMENSION_select[]'])):
        prices = []
        zb = form_dict['DIMENSION_select[]'][i]
        zzb.append(zb)
        sql = '''select a.dim_id,a.erdat,a.close_price,b.dim_def
            from dim_market_price a,
                dim_market_id b
            where a.dim_id=b.dim_id
            and a.dim_id = '%s'
            and substr(erdat,1,6) between '%s' and '%s'
            order by erdat
            '''% (zb, bmonth, emonth)
        df = ora_result(sql)
        zid_fuc.append(df['DIM_DEF'][0])
        df2 = pd.DataFrame(list(df.ERDAT), columns=['erdat'])
        df1 = pd.concat([df2, df1],ignore_index=True).drop_duplicates()
        for j in range(0, len(list(df.ERDAT))):
            prices_o = []
            prices_o.append(list(df.ERDAT)[j])
            prices_o.append(list(df.CLOSE_PRICE)[j])
            prices.append(prices_o)
        prices_n = dict(prices_n, **{zb: prices})
    dates = list(df1.erdat)
    ret = {
        'DATES': dates,
        'PRICES': prices_n,
        'ZID': zzb,
        'ZID_FUC': zid_fuc
    }
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json charset=utf-8")
def market_dates2(request):
    form_dict = dict(six.iterlists(request.GET))
    bmonth = form_dict['START_time2'][0].replace('-', '')
    emonth = form_dict['END_time2'][0].replace('-', '')
    zid = form_dict['DIMENSION_select2[]']
    zid_fuc = []
    df_origin = pd.DataFrame([], columns=['ERDAT'])
    for i in range(0, len(zid)):
        sql = '''select a.dim_id,a.erdat,a.close_price,b.dim_def
                from dim_market_price a,
                    dim_market_id b
                where a.dim_id=b.dim_id
                and a.dim_id = '%s'
                and substr(erdat,1,6) between '%s' and '%s'
                order by erdat
                ''' % (zid[i], bmonth, emonth)
        df = ora_result(sql)
        zid_fuc.append(df['DIM_DEF'][0])
        # 取数列,并重命名,结果为(index,erdat,i,...,price_i,...,def_i,...)
        df_origin = pd.merge(df, df_origin, on=['ERDAT'], how='outer')
        df_origin = df_origin.rename(columns={'DIM_ID': zid_fuc[i]})
        df_origin = df_origin.rename(columns={'CLOSE_PRICE': 'PRICE' + zid_fuc[i]})
        df_origin = df_origin.rename(columns={'DIM_DEF': 'DEF' + zid_fuc[i]})

    head = ['DIM_ID']+ list(df_origin['ERDAT'])
    result = [head,]
    for i in range(0, len(zid)):
        values = [zid_fuc[i]]+ list(df_origin['PRICE'+zid_fuc[i]])
        result.append(values)
    ret = {
        'RESULT': result,
        'RHEAD': zid_fuc
    }
    print(result)
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json charset=utf-8")
def market_dates3(request):
    form_dict = dict(six.iterlists(request.GET))
    bmonth = form_dict['START_time3'][0].replace('-', '')
    emonth = form_dict['END_time3'][0].replace('-', '')
    zid = form_dict['DIMENSION_select3[]']
    zid_fuc = []
    df_origin = pd.DataFrame([], columns=['ERDAT'])
    for i in range(0, len(zid)):
        sql = '''select a.dim_id,a.erdat,a.close_price,b.dim_def
                from dim_market_price a,
                    dim_market_id b
                where a.dim_id=b.dim_id
                and a.dim_id = '%s'
                and substr(erdat,1,6) between '%s' and '%s'
                order by erdat
                ''' % (zid[i], bmonth, emonth)
        df = ora_result(sql)
        zid_fuc.append(df['DIM_DEF'][0])
        # 取数列,并重命名,结果为(index,erdat,i,...,price_i,...,def_i,...)
        df_origin = pd.merge(df, df_origin, on=['ERDAT'], how='outer')
        df_origin = df_origin.rename(columns={'DIM_ID': zid_fuc[i]})
        df_origin = df_origin.rename(columns={'CLOSE_PRICE': 'PRICE' + zid_fuc[i]})
        df_origin = df_origin.rename(columns={'DIM_DEF': 'DEF' + zid_fuc[i]})

    head = ['DIM_ID']+ list(df_origin['ERDAT'])
    result = [head,]
    for i in range(0, len(zid)):
        values = [zid_fuc[i]]+ list(df_origin['PRICE'+zid_fuc[i]])
        result.append(values)
    ret = {
        'RESULT': result,
        'RHEAD': zid_fuc
    }
    print(result)
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json charset=utf-8")

def analysis(request):
    dbcon = pyhdb.connect(host='192.168.2.192', port='30241',
                          user='XHZHOU', password='Zhou1234')
    sql = '''select zb,erdat,spj
                 from"COMMON"."XFM_MARKT"
                where zb='S5431567'
                and left(erdat,6)='201511'
            '''
    df = pd.read_sql_query(sql, dbcon)

    dates = list(df.ERDAT)
    prices = list(df.SPJ)
    return render(request, 'analysis.html', {'dates': dates, 'prices': prices})

def filter(request):
    D_MULTI_SELECT = {
        'TC I': '[TC I]',
        'TC II': '[TC II',
        'TC III': '[TC III]',
        'TC IV': '[TC IV]',
        '通用名|MOLECULE': 'MOLECULE',
        '商品名|PRODUCT': 'PRODUCT',
        '包装|PACKAGE': 'PACKAGE',
        '生产企业|CORPORATION': 'CORPORATION',
        '企业类型': 'MANUF_TYPE',
        '剂型': 'FORMULATION',
        '剂量': 'STRENGTH'
    }
    mselect_dict = {}
    for key, value in D_MULTI_SELECT.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list 以后可以后端通过列表为每个多选控件传递备选项

    context = {
        'mselect_dict': mselect_dict
    }
    return render(request, 'filter.html', context)

def query(request):
    form_dict = dict(six.iterlists(request.GET))
    print(form_dict)
    bmonth = form_dict['START_time'][0]
    emonth = form_dict['END_time'][0]
    bmonth = bmonth.replace('-', '')
    emonth = emonth.replace('-', '')

    prices, zzb = [], []
    df1 = pd.DataFrame([], columns=['erdat'])
    for i in range(0, len(form_dict['DIMENSION_select[]'])):
        zb = form_dict['DIMENSION_select[]'][i]
        zzb.append(zb)
        sql = '''select zb,erdat,spj
                     from"COMMON"."XFM_MARKT"
                    where zb='%s'
                    and left(erdat,6) between '%s' and '%s'
                    order by erdat
                  '''% (zb, bmonth, emonth)
        df = sql_result(sql)
        df2 = pd.DataFrame(list(df.ERDAT), columns=['erdat'])
        df1 = pd.concat([df2, df1],ignore_index=True).drop_duplicates()

        prices.append(list(df.SPJ))
    dates = list(df1.erdat)
    ret = {
        'a': dates,
        'b': prices,
        'id': zzb
    }
    print(ret)
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式

def query2(request):
    sql = '''select zb,erdat,spj
                 from"COMMON"."XFM_MARKT"
                where zb='S5431567'
                order by erdat
    '''
    df = sql_result(sql)

    dates = list(df.ERDAT)
    prices = list(df.SPJ)
    ret2 = {
        'a': dates,
        'b': prices,
        'id': 'S5431567'
    }
    # print(ret2)
    return HttpResponse(json.dumps(ret2, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式

def text(request):
    return render(request, 'text.html')

def text2(request):
    return render(request, 'text2.html')

def text3(request):
    return render(request, 'text3.html')

def text4(request):
    return render(request, 'text4.html')


def zzzzzz(request):
    today = (datetime.datetime.strptime(datetime.date.today().strftime('%Y%m%d'), '%Y%m%d') +
             datetime.timedelta(days=-1)).strftime('%Y%m%d')
    today_c = (datetime.datetime.strptime(datetime.date.today().strftime('%Y%m%d'), '%Y%m%d') +
               datetime.timedelta(days=-1)).strftime('%Y-%m')
    dim_id = '618100'
    sql2 = '''
        select a.dim_id,a.erdat,a.close_price,b.dim_def
        from dim_market_price a,
            dim_market_id b
        where a.dim_id=b.dim_id
        and a.dim_id = '%s'
        and substr(erdat,1,6)=substr('%s',1,6)
        ''' % (dim_id, today)
    df2 = ora_result(sql2)

    dates = list(df2.ERDAT)
    prices = list(df2.CLOSE_PRICE)

    return render(request, 'zzzzzz.html', {'dates': dates, 'prices': prices, 'id': 'POY价格', 'month': today_c})

def semantic(request):
    return render(request, 'semantic.html')

def echarts4(request):
    return render(request, 'echarts4.html')

def query3(request):
    sql = '''select zb,erdat,spj
                 from"COMMON"."XFM_MARKT"
                where zb='S5431567'
                and erdat between'20150101'and '20150201'
                order by erdat
    '''
    df = sql_result(sql)

    dates = list(df.ERDAT)
    prices = list(df.SPJ)
    ret2 = {
        'a': dates,
        'b': prices,
    }
    # print(ret2)
    return HttpResponse(json.dumps(ret2, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式

def query4(request):
    sql = '''select zb,erdat,spj
                 from"COMMON"."XFM_MARKT"
                where zb='S5431567'
                and erdat between'20150101'and '20160501'
                order by erdat
    '''
    df = sql_result(sql)

    dates = list(df.ERDAT)
    prices = list(df.SPJ)
    ret2 = {
        'a': dates,
        'b': prices,
    }
    # print(ret2)
    return HttpResponse(json.dumps(ret2, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式

def query5(request):
    sql1 = '''
        select distinct b.ms,a.zb
        from"COMMON"."XFM_MARKT"a,
        "COMMON"."XFM_MARKTDZB"b
        where a.zb=b.zb
        '''
    df1 = sql_result(sql1)

    mselect_dict = {}
    for index, row in df1.iterrows():
        mselect_dict[row.MS] = row.ZB
    list = eval(str(mselect_dict))
    return HttpResponse(json.dumps(list, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式

def query6(request):
    list={
        'a':[1],
        'b':3,
        'c':4
    }
    return HttpResponse(json.dumps(list, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式

def test(request):
    return JsonResponse({'status':0, 'message':'This is test file'})

# 总览--销售
def overallviewsd(request):
    list = {
        'dbsd01_sales':3048,
        'dbsd01_salesyoy':'3.85%',
        'dbsd01_money': 4052,
        'dbsd01_moneyyoy': '4.85%',
        'dbsd01_price': 682,
        'dbsd01_priceyoy': '5.85%',
    }
    return HttpResponse(json.dumps(list, ensure_ascii=False),
                        content_type="application/json charset=utf-8")
# 总览--人资
def overallviewhr(request):
    list = {
        'dbhr01_amount':120491,
        'dbhr01_bukrs':['公司名称', "中辰", "中盈", "中维", "中辰", "中石"],
        'dbhr01_bukrs_amonut': ['人数', 435, 310, 234, 135, 1548,],
    }
    return HttpResponse(json.dumps(list, ensure_ascii=False),
                        content_type="application/json charset=utf-8")
# 总览--生产
def overallviewsc(request):
    list = {
        'dbsc01_product':250049,
        'dbsc01_zzh':['装置名称', "ZCP01", "ZCP02", "ZCP03", "ZCP04", "ZCP05", "ZCP06", 'ZCP07', 'ZCP08', 'HCP01',
              'HCP02', 'HCP03', 'HCP04', 'HCP05', 'HCP06'],
        'dbsc01_zzho': ["ZCP01", "ZCP02", "ZCP03", "ZCP04", "ZCP05", "ZCP06", 'ZCP07', 'ZCP08', 'HCP01',
                       'HCP02', 'HCP03', 'HCP04', 'HCP05', 'HCP06'],
        'dbsc01_zzh_product': ['产量', 40, 20, 35, 60, 55, 10, 11, 21, 5, 19, 28, 4, 9, 111],

    }
    return HttpResponse(json.dumps(list, ensure_ascii=False),
                        content_type="application/json charset=utf-8")
# 总览--库存
def overallviewmm(request):
    list = {
        'dbsd01_sales':3048,
        'dbsd01_salesyoy':'3.85%',
        'dbsd01_money': 4052,
        'dbsd01_moneyyoy': '4.85%',
        'dbsd01_price': 682,
        'dbsd01_priceyoy': '5.85%',
    }
    return HttpResponse(json.dumps(list, ensure_ascii=False),
                        content_type="application/json charset=utf-8")
# 总览--安全
def overallviewaq(request):
    list = {
        'dbsd01_sales':3048,
        'dbsd01_salesyoy':'3.85%',
        'dbsd01_money': 4052,
        'dbsd01_moneyyoy': '4.85%',
        'dbsd01_price': 682,
        'dbsd01_priceyoy': '5.85%',
    }
    return HttpResponse(json.dumps(list, ensure_ascii=False),
                        content_type="application/json charset=utf-8")