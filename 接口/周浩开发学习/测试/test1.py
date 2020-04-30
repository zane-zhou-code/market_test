# import numpy
# a = numpy.array([[1, 2, 3], [4, 2, 6], [7, 8, 9]])
# a = a.astype(float)
# print(a)
# print(a.dtype)
# b = (a[:, 0] == 4)  # [False False False]]
# print(a[b, :])
import datetime


def logo(list):
    a = []
    for i in range(0, len(list)):
        new_date =  datetime.datetime.strptime(list[i], '%Y-%m-%d')
        if new_date.day >= 26 and new_date.day <= 31:
            c = str(new_date.year) + str(new_date.month + 1)
        elif new_date.day < 26:
            c = str(new_date.year) + str(new_date.month)
        a.append(c)
    return a


a = logo(['2020-03-25','2020-03-28','2020-04-01','2020-04-25','2020-04-26','2020-04-28','2020-04-29','2020-05-10'])
print(a)
print('这是一个测试数据')

