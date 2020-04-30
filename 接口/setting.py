import pymysql
import pyhdb
import cx_Oracle
import poplib  # 读取邮件
import smtplib  # 发送邮件
import base64
import re,time
import datetime # 日期
import pyautogui # 自动点击
import pyperclip

from email.utils import parseaddr, formataddr
from email.header import decode_header
from email.parser import Parser
from email.mime.multipart import MIMEMultipart  # 负责将多个对象集合起来
from email.header import Header
from email.mime.text import MIMEText  # 负责构造文本
from email.mime.image import MIMEImage  # 负责构造图片
from multiprocessing import Pool  #定义进程池

# 数据库连接
class get_connection(object):
    # 定义hana数据库连接
    def hana_connection(self, host='192.168.2.192', port='30241',
                        user='XHZHOU', password='Zhou1234'):
        conn_obj = pyhdb.connect(host=host, port=port, user=user, password=password)
        return conn_obj
    # 定义mysql数据库连接
    def mysql_connection(self, host='192.168.112.28', user='xhzhou', password='Zhou1234',
                         database='test', charset='utf8'):
        conn_obj = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)
        return conn_obj
    # 定义oracle数据库连接
    def oracle_connection(self, host='192.168.2.74', port='1521', user='C##XFM_TARGET',
                          password='Xfm#2020', database='orcl'):
        access = '%s/%s@%s:%s/%s' % (user, password, host, port, database)
        # print(access)
        conn_obj = cx_Oracle.connect(access)
        return conn_obj
    def close_connection(self, conn):
        try:
            conn.close()
        except Exception as e:
            print('-------------------------------已关闭数据库-----------------------')
# 规范化执行sql语句
class sql(object):
    # 定义sql语句，参数为连接数据库，传递参数，以及实际sql语句
    def execute_sql(self, conn_obj, sql_list):
        conn = conn_obj
        cursor = conn.cursor()
        try:
            if re.search('^select', sql_list.strip().lower()):  # 查询语句
                cursor.execute(sql_list)
                result = cursor.fetchall()
                # print(result)
                print('这是查询执行结果：%s' % result)
                result = result != [] and result or None
                return result
            elif re.search('^insert', sql_list.strip().lower()):  # 插入语句
                if sql_list != []:
                    cursor.execute(sql_list)
                    conn.commit()
                    print('\033[37;40m-----------------------------插入操作已执行-----------------------\033[0m')
                else:
                    pass
            elif re.search('^delete', sql_list.strip().lower()):  # 删除语句
                cursor.execute(sql_list)
                conn.commit()
                print('\033[37;40m-----------------------------删除操作已执行-----------------------\033[0m')
            elif re.search('^update', sql_list.strip().lower()):  # 更新语句
                cursor.execute(sql_list)
                conn.commit()
                print('\033[37;40m-----------------------------更新操作已执行-----------------------\033[0m')
            else:
                pass
        except Exception as e:
            a = re.findall('invalid column name', str(e))
            b = re.findall('unique constraint violated', str(e))
            if a:
                print('\033[1;37;41m----查询语句异常：' + str(e) + '----\033[0m')
            elif b:
                print('\033[1;37;41m----表中主键冲突：' + str(e) + '----\033[0m')
            else:
                print(e)
    def sql_req(self, conn_obj, *params, sql):
        sql_list = []
        count = sql.count('%s')
        # 首先判断有无传入参数,然后判断是否有参数为None
        if not params and count == 0:
            sql_list = sql
            result = self.execute_sql(conn_obj, sql_list)
        elif re.search('None', str(params)):
            print('\033[1;37;41m-------------------------------插入值有空，停止插入-----------------------\033[0m')
            result = None
        else:
            if isinstance(params[0], tuple) or isinstance(params[0], list):
                if isinstance(params[0][0], tuple) or isinstance(params[0][0], list):
                    params = params[0]
                    # 取params的tuple深度
                    deep = len(params)
                    deep_item = params
                else:
                    deep = 1
                    deep_item = params[0]
            else:
                deep = len(params)
                deep_item = params
            # 依次取,然后判断,是否为tuple或list
            for i in range(0, deep):
                params = deep_item[i]
                item = deep_item
                while isinstance(params, tuple) or isinstance(params, list):
                    item = params
                    params = params[0]
                lenth = len(item)
                # 传参0个,待传入>=1,缺少传参
                if lenth == 0 and count >= 1:
                    print('\033[1;37;41m-------------------------------缺少传入参数-----------------------\033[0m')
                    return None
                # 传参1个,待传入1个
                elif lenth == 1 and count == 1:
                    sql_list = sql % params
                # 传参1个,待传入超过1个，按照同一参数传入
                elif lenth == 1 and count > 1:
                    _list = []
                    for i in range(0, count):
                        _list.append(params)
                    _list = tuple(_list)
                    sql_list = sql % _list
                # 传参大于1,但小于待传入数量
                elif lenth > 1 and lenth < count:
                    print('\033[1;37;41m-------------------------------传入参数不足-----------------------\033[0m')
                    exit()
                # 其他,传参多与待传入数量
                else:
                    item = tuple(item)
                    a = item[0:count]
                    sql_list = sql % a
                # print('\033[37;40m-------------------------------这是执行语句-----------------------\033[0m')
                # print(sql_list)
                result = self.execute_sql(conn_obj, sql_list)
        return result



# 日期等固定参数
class fixed_params(object):
    today       = datetime.date.today().strftime('%Y%m%d')
    yesterday   = (datetime.datetime.strptime(today, '%Y%m%d') +
                    datetime.timedelta(days=-1)).strftime('%Y%m%d')
    today_l     = datetime.date.today().strftime('%Y-%m-%d')
    yesterday_l = (datetime.datetime.strptime(today, '%Y%m%d') +
                    datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    yesterday_2 = (datetime.datetime.strptime(today, '%Y%m%d') +
                    datetime.timedelta(days=-1)).strftime(
                '%Y年%m月%d日'.encode('unicode_escape').decode('utf8')).encode('utf-8').decode('unicode_escape')
    pass
# 进程池
def parse_concurrent(self, fuc, *params):
    pool = Pool(4)
    # 接受进程池的返回值
    res_list = []
    for func in res_list:
        res = pool.apply_async(func=func, args=(func, *params))
        res_get_list = res.get()
        for i in range(0, len(res_get_list)):
            res_list.append(res_get_list[i])
        print('\033[37;40m-------------------已完成 ', str(func), ' 取数------------------\033[0m')
    pool.close()
    pool.join()
    return res_list

# 邮件读取
class parsing_emails():
    # 定义连接信息 获取msg信息
    def connection(self, email_host='192.168.112.21',
                   email_sender='50031167@xfmgroup.com',
                   email_license='xfm@1234'):
        server = poplib.POP3(email_host)  # 连接POP3服务器
        server.set_debuglevel(1)  # 打开调试信息
        # print(server.getwelcome().decode('gbk'))
        server.user(email_sender)
        server.pass_(email_license)
        # print('Messages: %s. Size: %s' % server.stat())  # 打印邮箱邮件数量和占用空间
        resp, mails, octets = server.list()  # 返回所有邮箱编号 列表类似[b'1 82923', b'2 2184', ...]
        quantity = len(mails)
        return server, mails, quantity

    # 解析邮件
    def parser(self, msg_content):
        msg = Parser().parsestr(msg_content)
        return msg

    def msg_read(self, index):
        server, mails, quantity = self.connection()
        resp, lines, octets = server.retr(index)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 解析出邮件:
        msg = Parser().parsestr(msg_content)
        return msg

    # 定义邮件头解码
    def header_code(self, value):
        value, charset = decode_header(value)[0]  # 若有很多个收件人，默认取第一个
        if charset:
            value = value.decode(charset)  # 以取得的编码方式解码邮件头
        return value

    # 定义邮件体解码
    def body_code(self, msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()  # 取charset=八位后的编码
        return charset

    # 定义打印信息并下载附件
    def print_info(self, msg, root, secdir, indent=0):
        if indent == 0:
            # 邮件的From, To, Subject存在于根对象上:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        # 需要解码Subject字符串:
                        value = self.header_code(value)
                    else:
                        # 需要解码Email地址:
                        hdr, addr = parseaddr(value)
                        name = self.header_code(hdr)
                        value = u'%s <%s>' % (name, addr)
                print('%s%s: %s' % ('  ' * indent, header, value))
        if (msg.is_multipart()):
            # 如果邮件对象是一个MIMEMultipart,
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))
                self.print_info(msg=part, root=root, secdir=secdir, indent=indent + 1)
        else:
            # 邮件对象不是一个MIMEMultipart,
            # 就根据content_type判断:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = self.body_code(msg)
                if charset:
                    content = content.decode(charset)
                print('%sText: %s' % ('  ' * indent, content + '...'))
            else:
                # 不是文本,作为附件处理:
                print('%sAttachment: %s' % ('  ' * indent, content_type))
                for part in msg.walk():
                    fileName = part.get_filename()
                    fileName = self.header_code(fileName)
                    # 保存附件
                    if fileName:
                        with open(root + secdir, 'wb') as download:
                            data = part.get_payload(decode=True)
                            download.write(data)
                            print("附件%s已保存" % fileName)

# 邮件发送
class send_emails():
    _mm = MIMEMultipart('related')
    # 处理邮件地址
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    # 设置邮件内容
    def header(self, *params, charset='utf-8'):
        item = params
        while isinstance(params, tuple) or isinstance(params, list):
            item = params
            params = params[0]
        email_sender = item[0]
        email_receiver =  item[1]
        subject_content = item[2]
        self._mm['From'] = self._format_addr(email_sender)
        for i in range(0, len(email_receiver)):
            email_receiver[i] = self._format_addr(email_receiver[i])
        self._mm['To'] = ",".join(email_receiver)
        self._mm['Subject'] = Header(subject_content, charset)

    # 添加正文文本
    def add_body(self, *params, charset='utf-8'):
        item = params
        while isinstance(params, tuple) or isinstance(params, list):
            item = params
            params = params[0]
        body_content = item[0]
        message_text = MIMEText(body_content, "plain", charset)
        self._mm.attach(message_text)

    # 添加图片
    def add_image(self, *params, charset='utf-8'):
        item = params
        while isinstance(params, tuple) or isinstance(params, list):
            item = params
            params = params[0]
        root = item[0]
        filename = item[1]
        message_image = MIMEImage(open(root, 'rb').read())
        bs_filename = base64.b64encode(filename.encode(charset))
        message_image.add_header('Content-Disposition', 'attachment',
                                 filename='=?utf-8?b?' + bs_filename.decode() + '?=')
        open(root, 'rb').close()
        self._mm.attach(message_image)

    # 添加附件
    def add_attachment(self, *params, charset='utf-8'):
        item = params
        while isinstance(params, tuple) or isinstance(params, list):
            item = params
            params = params[0]
        root = item[0]
        filename = item[1]
        atta = MIMEText(open(root, 'rb').read(), 'base64', charset)
        bs_filename = base64.b64encode(filename.encode(charset))
        atta["Content-Type"] = "app;ocation/octet-stream"
        atta.add_header('Content-Disposition', 'attachment', filename='=?utf-8?b?' + bs_filename.decode() + '?=')
        self._mm.attach(atta)

    # 连接邮箱并发送
    def conn_send(self, *params, port=25, level=1):
        item = params
        while isinstance(params, tuple) or isinstance(params, list):
            item = params
            params = params[0]
        email_host = item[0]
        email_license = item[1]
        email_sender = item[2]
        email_receiver = item[3]
        server = smtplib.SMTP()
        server.connect(email_host, port)
        server.set_debuglevel(level)  # 开启监听模式
        server.login(email_sender, email_license)
        server.sendmail(email_sender, email_receiver, self._mm.as_string())
        print('邮件发送成功')

# 微信自动读取
class wechat_auto():
    # 查找图片，并点击
    def mapping_img(self, img, click):
        box_location = pyautogui.locateOnScreen(img)
        center = pyautogui.center(box_location)
        if click == 'double':
            pyautogui.doubleClick(center)
        else:
            pyautogui.leftClick(center)
    # 读取文本
    def read_txt(self, txt, number):
        file = open(txt, 'r', encoding='ANSI')
        filecontent = file.readlines()
        pyperclip.copy(filecontent[number].strip('\n'))
        pyautogui.hotkey('ctrl', 'v')
        file.close()
    # 读取文件
    def read_file(self, filenum, filenum2, filename):
        self.mapping_img(r'D:\wechat--auto\image\file-send.png', 'single')
        time.sleep(1)
        self.read_txt('D:\wechat--auto\word\path.txt', filenum)
        pyautogui.press('enter')
        time.sleep(1)
        self.read_txt('D:\wechat--auto\word\path.txt', filenum2)
        time.sleep(1)
        pyautogui.typewrite(filename, interval=0.5)
        time.sleep(1)
        pyautogui.press('enter')
    # 热键
    def hotkey(self, left, right):
        pyautogui.hotkey(left, right)
    # 微信发送文本
    def send_mesg(self, namenum, situationnum):
        self.hotkey('winleft', 'd')
        time.sleep(1)
        try:
            self.mapping_img('D:\wechat--auto\image\wechat.png', 'double')
        except:
            self.mapping_img('D:\wechat--auto\image\wechat-click.png', 'double')
        time.sleep(1)
        self.mapping_img('D:\wechat--auto\image\search.png', 'double')
        time.sleep(1)
        self.read_txt(r'D:\wechat--auto\word\name.txt', namenum)
        pyautogui.press('enter')
        time.sleep(1)
        self.read_txt(r'D:\wechat--auto\word\situation.txt', situationnum)
        pyautogui.press('enter')
        time.sleep(1)
        self.mapping_img('D:\wechat--auto\image\quit.png', 'double')
    # 微信发送文件
    def send_file(self, namenum, filenum, filenum2, filename):
        self.hotkey('winleft', 'd')
        time.sleep(1)
        try:
            self.mapping_img('D:\wechat--auto\image\wechat.png', 'double')
        except:
            self.mapping_img('D:\wechat--auto\image\wechat-click.png', 'double')
        time.sleep(1)
        self.mapping_img('D:\wechat--auto\image\search.png', 'double')
        time.sleep(1)
        self.read_txt(r'D:\wechat--auto\word\name.txt', namenum)
        pyautogui.press('enter')
        time.sleep(1)
        self.read_file(filenum, filenum2, filename)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        self.mapping_img('D:\wechat--auto\image\quit.png', 'double')

# 工作台与日志输出
import sys


class print_and_save(object):
    def __init__(self, filepath):
        self.file = open(filepath, 'a')
        self.old = sys.stdout  # 将当前系统输出储存到临时变量
        sys.stdout = self

    def __enter__(self):
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            frs = func(*args, **kwargs)
            self._exit()
            return frs

        return wrapper

    def write(self, message):
        self.old.write(message)
        self.file.write(message)

    def flush(self):
        self.old.flush()
        self.file.flush()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exit()

    def _exit(self):
        self.file.flush()
        self.file.close()
        sys.stdout = self.old


