# 客户端
import socket
import hashlib

# 声明socket类型，同时生成连接对象
client = socket.socket()
client.connect(('localhost',6969))  # 指接口

while True:
    msg = input(">>:").strip()
    if msg.startswith('get'):
        client.send(msg.encode())
        file_size = client.recv(1024)
        client.send('开始传输文件'.encode('utf-8'))
        file_size_new = int(file_size.decode())
        recvd_size = 0
        file_name = msg.split()[1]
        m = hashlib.md5()
        with open(file_name, 'wb')as f:
            while recvd_size < file_size_new:
                if file_size_new - recvd_size > 1024:
                    size = 1024
                else:
                    size = file_size_new - recvd_size
                data = client.recv(size)
                recvd_size += len(data.decode())
                m.update(data)
                f.write(data)
            else:
                new_file_md5 = m.hexdigest()
                f.close()
            server_file_md5 = client.recv(1024)
    # client.send(msg.encode('utf-8'))
    # data_size = client.recv(1024)
    # client.send('准备好接收了'.encode('utf-8'))
    # recvd_size = 0
    # while recvd_size < int(data_size.decode()):
    #     data = client.recv(1024)  # 指接收的大小
    #     recvd_size += len(data)
    #     print('recv:', data.decode())

client.close()
