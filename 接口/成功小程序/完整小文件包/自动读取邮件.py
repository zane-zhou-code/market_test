from 接口.setting import parsing_emails,fixed_params
def main():
    # 邮箱可变信息
    email_host = '192.168.112.21'
    email_license = '50031167@xfmgroup.com'
    email_sender = 'xfm@1234'

    # 定义服务器连接 获取服务和所有邮箱编号
    server, mails, quantity = parsing_emails().connection()
    index = quantity
    while index:
        msg = parsing_emails().msg_read(index)
        value = msg.get('Subject', '')
        value = parsing_emails().header_code(value)
        print(value)
        index = index - 1
        if value == "各装置主要生产日指标汇总表":
            today = fixed_params().today
            yesterday = fixed_params().yesterday
            root = "C:\\Users\\admin\\Desktop\\各装置主要生产日指标汇总表\\"
            secdir = value +' %s.pdf' % yesterday
            print(secdir)
            parsing_emails().print_info(msg=msg, root=root, secdir=secdir)
            exit()
    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()
if __name__ == '__main__':
    main()