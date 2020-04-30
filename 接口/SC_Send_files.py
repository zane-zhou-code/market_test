import os
from 接口.setting import wechat_auto,fixed_params
yesterday = fixed_params().yesterday
filename = ' %s.pdf' % yesterday
chfilename = 'D:\各装置主要生产日指标汇总\各装置主要生产日指标汇总表'
if os.path.exists(chfilename + filename):
    # 参数依次是自己，路径，文件中文字符，文件剩余部分
    wechat_auto().send_file(namenum=0, filenum=0, filenum2=1, filename=filename)
else:
    # 提醒人员处理，参数依次是自己，文本1
    wechat_auto().send_mesg(0, 1)

