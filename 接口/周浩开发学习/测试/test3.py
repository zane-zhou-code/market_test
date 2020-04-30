from 接口.setting import get_connection,sql,fixed_params
import pandas as pd
import datetime
import numpy as np
import re


class time_list(object):
    def __init__(self, all_data):
        self.all_data = all_data
        try:
            self.begda = all_data[0][1]
            self.endda =  all_data[-1][1]
            self.id    = all_data[0][0]
            self.pid = 'D' if len(str(self.begda)) == 8 else 'M'  # pid标识日还是月
        except:
            exit()

    # 日期转换函数
    def data_convert(self, list):
        if len(str(list)) == 6:
            list = datetime.datetime.strptime(list, '%Y%m')
        elif len(str(list)) == 8:
            list = datetime.datetime.strptime(list, '%Y%m%d')
        return list
    # 生成日期数列
    def days_list(self):
        zbegda = self.data_convert(self.begda)
        zendda = self.data_convert(self.endda)
        array = []
        if len(str(self.begda)) == 6:
            array = pd.date_range(zbegda, zendda, freq='MS')
        elif len(str(self.begda)) == 8:
            array = pd.date_range(zbegda, zendda)
        return array
    #  清洗数据
    def clean_data(self):
        array = self.days_list()
        # axis 0为列(默认) 1为行
        # 建原始df,合并相同日期数据,建日期序列df_e,并合并为df_new
        df = pd.DataFrame(self.all_data, columns=['dim_id', 'erdat', 'price_old'])
        df = df.groupby([df.dim_id, df.erdat], as_index=False).sum()  # 合并相同日期数据,取和
        df.sort_values(['erdat'], ascending=True, inplace=True)  # 根据日期字段,升序排列
        df.reset_index(drop=True, inplace=True)  # 将索引列重新升序排列
        # 设置erdat_new是时间为yyyy--mm--dd(月度为当月第一日)
        df['erdat_new'] = pd.to_datetime(df['erdat']) if self.pid == 'D' \
            else pd.to_datetime([i + '01' for i in df['erdat']])
        df_e = pd.DataFrame(array, columns=['erdat_new'])
        df_new = pd.merge(df_e, df, on='erdat_new', how='left')
        return df_new,self.pid
    #  后续计算价
    def calculated_price(self):
        try:
            df_new,pid = self.clean_data()
            # 以前值方式填充矩阵
            df_new['price_new'] = df_new.price_old.fillna(method='ffill')
            df_new['dim_id'] = df_new.dim_id.fillna(method='ffill')

            df_new['dond'] = self.dond_func(df_new)
            df_new['yony'] = self.yony_func(df_new, pid)
            df_new['price_dayly'] = self.dayly_func(df_new)

            months = df_new.groupby(df_new.erdat_new.dt.year.astype(str) + df_new.erdat_new.dt.month.astype(str))
            df_new['price_monthly'] = months.apply(self.monthly_fuc).price_monthly  # apply方法 会将分组后的数据一组一组传入

            quarters = df_new.groupby(df_new.erdat_new.dt.year.astype(str) + df_new.erdat_new.dt.quarter.astype(str))
            df_new['price_quarterly'] = quarters.apply(self.quarterly_fuc).price_quarterly

            years = df_new.groupby(df_new.erdat_new.dt.year)
            df_new['price_yearly'] = years.apply(self.yearly_fuc).price_yearly

            specials = df_new.groupby(df_new.erdat_new.apply(self.special_fuc))
            df_new['special_dayly'] = specials.apply(self.monthly_fuc).price_monthly
            # df_new.to_excel(r"C:\Users\admin\Desktop\12.xlsx", index=False)  # 保存excel查看
            # df_new = df_new.loc[df_new.erdat_new>='2020-04-01',:]  #  限制要插入的数据
            return df_new
        except Exception as e:
            if re.findall('list index out of range', str(e)):
                return '\033[1;37;41m数组为空，请检查sql\033[0m'
            else:
                return '\033[1;37;41msome undefined question occured:%s\033[0m' % e
    #  定义结果输出
    def result_cal(self, sid='N'):
        df_new = self.calculated_price()
        df_new = df_new.fillna('')
        sel_list = ['dim_id', 'erdat_new', 'dond', 'yony', 'price_dayly', 'price_monthly', 'price_quarterly', 'price_yearly',
                    'special_dayly']
        result_pd = pd.DataFrame(df_new.loc[0:, sel_list])
        result_pd['erdat_new'] = [day.strftime('%Y%m%d') for day in result_pd.erdat_new] if self.pid == 'D' \
            else [day.strftime('%Y%m') for day in result_pd.erdat_new]

        # 01.同比;02.环比;03.日均;04.月均;05.季均;06.年均;10.特殊
        result = []
        cal_list = (2, 3, 4, 5, 6, 7) if sid == 'N' else (2, 3, 4, 5, 6, 7, 8)
        for i in cal_list:
            sel_newlist = sel_list[0:2] + sel_list[i:i+1]
            result_pd_new = pd.DataFrame(result_pd.loc[0:, sel_newlist])
            result_pd_new['dim_id_dr'] = result_pd_new['dim_id']
            i = str(i - 1)
            result_pd_new['dim_id'] = [id[:4] + '0' + i if len(i) == 1 else  id[:4] + i for id in result_pd_new.dim_id]
            b = np.array(result_pd_new).tolist()
            result += b
        return result

    #  转换日期格式的另一种方法
    def type_convert(self, df):
        df['tep'] = '01'
        df['erdat_new'] = df.erdat.str.cat(df.tep).astype('datatime64')
        df = self.add_delete_col(df, ad='D', del_col='tep')
        return df
    # 增加新列
    def add_delete_col(self, df, ad='A', del_col=None):
        col_name = df.columns.tolist()
        lenth = len(col_name)
        if ad == 'A':
            col_name.insert(lenth, 'price_new')
            df_new = df.reindex(columns=col_name)
            df_new.loc[:, 'price_new'] = df_new.price_old.values
        else:
            for i in range(0, lenth):
                if str(del_col) == str(col_name[i]):
                    col_name.pop(i)
                    break
            df_new = df.reindex(columns=col_name)
        return df_new

    #  周数处理
    def week_func(self, df):
        df_cp = df.copy()
        df_cp['week'] = df_cp.erdat_new.dt.week
        df_cp['month'] = df_cp.erdat_new.dt.month
        df_cp['zindex'] = df_cp.index
        df_cp2 = df_cp.copy()
        df_cp.set_index(['month'], drop=False, inplace=True)
        try:
            target_days = df_cp.loc[12, :]  # 减少检索的条目,节约时间
            for i in range(0, len(target_days.erdat_new)):
                if target_days.erdat_new.astype(str).values[i][5:] >= '12-10' and target_days.week.values[i] == 1:
                    locate = target_days.zindex.values[i]
                    df_cp2.loc[locate, ['week']] = 53
            return df_cp2['week']
        except:
            return df_cp2['week']


    #  环比计算
    def dond_func(self, df):
        df['dond'] = round(df['price_new'].pct_change(), 3)
        return df['dond']

    #  同比计算
    def yony_func(self, df, id):
        days = df.groupby(df.erdat_new.dt.day) if id == 'D' else df.groupby(df.erdat_new.dt.month)
        df['yony'] = round(days.price_new.pct_change(), 3)
        return df['yony']

    #  日均值计算
    def dayly_func(self, df):
        zi = 0
        for zi in range(0, len(df['price_old'])):
            if pd.isna(df.price_old[zi]) : break
        #  先按照最小空位的均价线填充一次,再按照五日线填充一次
        df['price_dayly'] = df.price_new.rolling(zi+1, min_periods=1).mean()
        df['price_dayly'] = df.price_dayly.rolling(5, min_periods=1).mean()
        for i in range(0, len(df)):
            if not pd.isna(df.price_old.values[i]):df.price_dayly.values[i] = df.price_old.values[i]
        return df['price_dayly']

    # 月均值计算
    def monthly_fuc(self, group):
        df = pd.DataFrame(group.loc[:, ['erdat_new', 'price_old']], columns=['erdat_new', 'price_old'])
        df.dropna(axis=0, how='any', inplace=True)
        df['price_monthly1'] = round(
            df.price_old.cumsum() / [i + 1 for i in range(0, len(df.price_old.values))], 3)
        group['price_monthly'] = round(
            group.price_dayly.cumsum() / [i + 1 for i in range(0, len(group.price_dayly.values))], 3)
        df2 = pd.merge(group, df, on=['erdat_new', 'price_old'], how='left')
        for i in range(0, len(df2)):
            if not pd.isna(df2.price_old.values[i]): group.price_monthly.values[i] = df2.price_monthly1.values[i]
        return group

    # 季均值计算
    def quarterly_fuc(self, group):
        df = pd.DataFrame(group.loc[:, ['erdat_new', 'price_old']], columns=['erdat_new', 'price_old'])
        df.dropna(axis=0, how='any', inplace=True)
        df['price_quarterly1'] = round(
            df.price_old.cumsum() / [i + 1 for i in range(0, len(df.price_old.values))], 3)
        group['price_quarterly'] = round(
            group.price_dayly.cumsum() / [i + 1 for i in range(0, len(group.price_dayly.values))], 3)
        df2 = pd.merge(group, df, on=['erdat_new', 'price_old'], how='left')
        for i in range(0, len(df2)):
            if not pd.isna(df2.price_old.values[i]): group.price_quarterly.values[i] = df2.price_quarterly1.values[i]
        return group

    # 年均值计算
    def yearly_fuc(self, group):
        df = pd.DataFrame(group.loc[:, ['erdat_new', 'price_old']], columns=['erdat_new', 'price_old'])
        df.dropna(axis=0, how='any', inplace=True)
        df['price_yearly1'] = round(
            df.price_old.cumsum() / [i + 1 for i in range(0, len(df.price_old.values))], 3)
        group['price_yearly'] = round(
            group.price_dayly.cumsum() / [i + 1 for i in range(0, len(group.price_dayly.values))], 3)
        df2 = pd.merge(group, df, on=['erdat_new', 'price_old'], how='left')
        for i in range(0, len(df2)):
            if not pd.isna(df2.price_old.values[i]): group.price_yearly.values[i] = df2.price_yearly1.values[i]
        return group

    #  特殊处理
    def special_fuc(self, group):
        if group.day >= 26:
            return str(group.year) + str(group.month + 1)
        elif group.day < 26:
            return str(group.year) + str(group.month)

# 重写week_fuch和clean_data
class time_list_new(time_list):
    def week_func(self, df):
        df_cp = df.copy()
        df_cp['week'] = time_list(self.all_data).week_func(df).astype(str).str.zfill(3)
        df_cp['erdat'] = df_cp.erdat.str[:4].astype(str).str.cat(df_cp.week)  # 把年和周合并拼成类似数据:2019005
        return df_cp['erdat']

    def clean_data(self):
        if self.id in ['609300', '617300', '617400', '617600', '617700', '617800', '617900',
                    '618200', '618300', '618400', '618500', '618800', '618900', '619000',
                    '619100', '622600']:
            pid = 'D'
            df = pd.DataFrame(self.all_data, columns=['dim_id', 'erdat', 'price_old'])
            df = df.groupby([df.dim_id, df.erdat], as_index=False).sum()  # 合并相同日期数据,取和
            df.sort_values(['erdat'], ascending=True, inplace=True)  # 根据日期字段,升序排列
            df.reset_index(drop=True, inplace=True)  # 将索引列重新升序排列
            df['erdat_new'] = pd.to_datetime(df['erdat'])
            df['erdat'] = self.week_func(df)
            return df, pid
        else:
            return time_list(self.all_data).clean_data()

    def result_cal(self, sid='N'):
        if self.id in ['609300', '617300', '617400', '617600', '617700', '617800', '617900',
                    '618200', '618300', '618400', '618500', '618800', '618900', '619000',
                    '619100', '622600']:
            df_new = self.calculated_price()
            df_new = df_new.fillna('')
            sel_list = ['dim_id', 'erdat', 'dond', 'yony', 'price_dayly', 'price_monthly', 'price_quarterly',
                        'price_yearly']
            result_pd = pd.DataFrame(df_new.loc[0:, sel_list])

            # 01.同比;02.环比;03.日均;04.月均;05.季均;06.年均
            result = []
            for i in (2, 3, 4, 5, 6, 7):
                sel_newlist = sel_list[0:2] + sel_list[i:i + 1]
                result_pd_new = pd.DataFrame(result_pd.loc[0:, sel_newlist])
                result_pd_new['dim_id_dr'] = result_pd_new['dim_id']
                i = str(i - 1)
                result_pd_new['dim_id'] = [id[:4] + '0' + i if len(i) == 1 else id[:4] + i for id in result_pd_new.dim_id]
                b = np.array(result_pd_new).tolist()
                result += b
            return result
        elif self.id in ['615300', '615400']:
            return time_list(self.all_data).result_cal(sid='Y')
        else:
            return time_list(self.all_data).result_cal()

def main():
    conn = get_connection().oracle_connection()
    yesterday = fixed_params().yesterday
    # day_weekbefore = fixed_params().day_weekbefore
    sel_sql1 = '''select distinct dim_id from DIM_MARKET_ID'''
    sel_sql2 = '''select dim_id, erdat, close_price
                      from DIM_MARKET_PRICE
                      where dim_id='%s' --617100 615600 622600
                      and erdat between '20200101'
                      and '20200423'
                      order by erdat'''
    ins_sql = '''insert into DIM_MARKET_PRICE_FORMULA (dim_id_dr, erdat, calced_price, dim_id)values('%s', '%s', %s, '%s')'''

    result1 = ('615300', '615400')
    for i in range(0, len(result1)):
        all_data = sql().sql_req(conn, result1[i], sql=sel_sql2)
        if all_data:
            all_results = time_list_new(all_data).result_cal()

            sql().sql_req(conn, all_results[i], sql=ins_sql)
    get_connection().close_connection(conn)

if __name__ == '__main__':
    main()


