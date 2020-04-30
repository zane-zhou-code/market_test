# import sys
#
# # 记录起始打印台，即python控制台
# stdout_backup = sys.stdout
# # 打开日志文件
# log_file = open("C:\\Users\\admin\\Desktop\\b.txt", "w")
# # 定位到日志文件的打印台
# sys.stdout = log_file
# print("Now all print info will be written to message.log")
# print('你是个傻子')
# # 关闭定位
# log_file.close()
# # 重新定位到python控制台
# sys.stdout = stdout_backup
# print("Now this will be presented on screen")
# f = open("C:\\Users\\admin\\Desktop\\b.txt")
# for eachline in f:
#     print('------------------------这是一个分割线')
#     print(eachline);
#------------------------------------------------------------------------另一个代码

import sys
from docx import Document
document = Document()
# 记录起始打印台，即python控制台
stdout_backup = sys.stdout
# 打开日志文件
log_file = open("C:\\Users\\admin\\Desktop\\b.docx",'w')
# 定位到日志文件的打印台
sys.stdout = log_file
print("Now all print info will be written to message.log")
print('你是个傻子')
# 关闭定位
log_file.close()
# 重新定位到python控制台
sys.stdout = stdout_backup
print("Now this will be presented on screen")
f = open("C:\\Users\\admin\\Desktop\\b.txt")
for eachline in f:
    print('------------------------这是一个分割线')
    print(eachline);




