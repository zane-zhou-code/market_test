from 接口.setting import send_emails,fixed_params

def main():
    # 日期
    yesterday = fixed_params().yesterday_2  # 年月日格式
    yesterday1 = fixed_params().yesterday  # 纯洁字符串格式
    # 邮件地址
    email_host = "192.168.112.21"
    email_license = "xfm@1234"
    # 邮件头
    email_sender = "50031167@xfmgroup.com"
    email_receiver = ["<50019936@xfmgroup.com>", "<50005218@xfmgroup.com>", "<50027862@xfmgroup.com>"]

    subject_content = """%s 各装置主要生产日指标汇总""" % yesterday
    # 邮件体
    body_content = "你好，这是%s各装置主要生产日指标报表，请注意查收" % yesterday
    # 邮件附件
    dir = 'D:\各装置主要生产日指标汇总\各装置主要生产日指标汇总表 %s.pdf' % yesterday1
    attachment_root = dir
    attachment_name = '各装置主要生产日指标报表 %s.pdf' % yesterday1

    # 邮件主要行项目
    header = ('周浩<>', ['钱朋超<50019936@xfmgroup.com>', "俞芬菊<50005218@xfmgroup.com>", '严晓康<50027862@xfmgroup.com>'], subject_content)
    body = (body_content)
    attachment = (attachment_root, attachment_name)
    # 连接
    conn = (email_host, email_license, email_sender, email_receiver)

    # 给邮件增加 头，体，附件等并发送
    send_emails().header(header)
    send_emails().add_body(body)
    send_emails().add_attachment(attachment)
    send_emails().conn_send(conn, level=0)

if __name__ == '__main__':
    main()
