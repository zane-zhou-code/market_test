import numpy as np
import matplotlib.pyplot as plt
import time
import pylab as pl
from scipy import interpolate
from scipy.interpolate import interp1d

import pyhdb

def get_connection():
    conn_obj = pyhdb.connect(
        host="192.168.2.192",  # 192.168.2.191 生产机 192.168.2.192 开发机
        port=30241,  # 30041生产机 30241开发机
        user="XHZHOU",
        password="Zhou1234"
    )
    return conn_obj
conn = get_connection()
cursor = conn.cursor()
sql = ''' select zb,erdat,spj from"COMMON"."XFM_MARKT"where zb='M0067855' and erdat between '20190901'and '20190930' '''
cursor.execute(sql)
results = cursor.fetchall()
print(results[0][0])
time.sleep(1)


x=[]
y=[]
for i in range(0,len(results)):
    x.insert(i, results[i][1])
for i in range(0,len(results)):
    y.insert(i, results[i][2])
print(x)
print(y)

plt.figure(num='周浩',figsize=(11,5))
plt.title('原油')  # 添加图形标题

k1=plt.plot(x, y, '-*', linewidth=1, color="red", label = "WTI主力期货日均")

plt.xticks(range(0,31,2), fontsize=7)  # plt.xticks(x, rotation=60, fontsize=7)

plt.xlabel('日期')
plt.ylabel('美元/吨')

# 设置x坐标轴名称
# plt.xticks(['20190902',],
#            [r'$really\ good$',])

plt.legend(handles=[], labels=[], loc="best")  # 显示图例的位置，最佳适应方式
plt.grid(True)  # 增加格点
plt.axis('tight')  # 坐标轴适应数据量 axis 设置坐标轴

# 设置无上右边框
ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# ax.spines['bottom'].set_position(('data',))  # outward axes
ax.spines['left'].set_position(('data',5))
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(10)
    label.set_bbox(dict(facecolor='white',edgecolor='None',alpha=0.7))


plt.show()

# 使用2个 Y轴(左右)fig, ax1 = plt.subplots() ax2 = ax1.twinx()
# 使用两个子图(上下,左右)plt.subplot(211)
# plt.subplot(121)(221) 多张图显示在同一个窗口中
# f,((axl1,axl2),(ax21,ax22)) = plt.subplots(2,2,sharex=True,sharey=True)

# bar 柱状图 scatter 散点图 hist 直方图 boxplot 箱形图  mpf.candlestick 烛柱图
# plt.xlim/ylim 设置x轴和y轴的范围
# 使用plt.xticks/yticks两个方法可以分别设置X和Y轴的坐标点的值是多少 plt.xticks(np.linspace(1,3,11))
# plt.gca()　　这个方法返回一个包含所有坐标轴的对象
# ax = Axes3D(fig)




# cursor.close()
# conn.close()


# #创建待插值的数据
# x = np.linspace(0, 10*np.pi, 20)
# y = np.cos(x)
#
# # 分别用linear和quadratic插值
# fl = interp1d(x, y, kind='linear')
# fq = interp1d(x, y, kind='quadratic')
#
# #设置x的最大值和最小值以防止插值数据越界
# xint = np.linspace(x.min(), x.max(), 1000)
# yintl = fl(xint)
# yintq = fq(xint)
# pl.plot(xint,fl(xint), color="green", label = "Linear")
# pl.plot(xint,fq(xint), color="yellow", label ="Quadratic")
# pl.legend(loc = "best")
# pl.show()
