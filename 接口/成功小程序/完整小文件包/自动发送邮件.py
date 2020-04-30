from 接口.setting import send_emails

def main():
    # 邮件地址
    email_host = "192.168.112.21" # "smtp.163.com"
    email_license = "xfm@1234"  # "Zhou0512"
    # 邮件头
    email_sender = "50031167@xfmgroup.com"  # "xhzhouqi@163.com"
    email_receiver = ["50031167@xfmgroup.com"]
    subject_content = """Python邮箱测试"""
    # 邮件体
    body_content = "你好，这是一个测试邮件！"
    # 邮件图片
    image_root = "C:\\Users\\admin\\Desktop\\ddd.jpg"
    image_name = '图片.jpg'
    # 邮件附件
    attachment_root1 = "C:\\Users\\admin\\Desktop\\市场指标看板-2019.11.05.docx"
    attachment_name1 = '市场指标看板-2019.11.05.docx'
    attachment_root2 = "C:\\Users\\admin\\Desktop\\各装置主要生产日指标汇总表\\各装置主要生产日指标汇总表 20191207.pdf"
    attachment_name2 = '各装置主要生产日指标汇总表 20191207.pdf'

    # 字段
    header = (email_sender, email_receiver, subject_content)
    body = (body_content)
    image = (image_root, image_name)
    attachment1 = (attachment_root1, attachment_name1)
    attachment2 = (attachment_root2, attachment_name2)
    conn = (email_host, email_license, email_sender, email_receiver)
    print(header)
    # 给邮件增加 头，体，附件等并发送
    send_emails().header(header)
    send_emails().add_body(body)
    send_emails().add_image(image)
    send_emails().add_attachment(attachment1)
    send_emails().add_attachment(attachment2)
    send_emails().conn_send(conn)

if __name__ == '__main__':
    main()
