# 服务器端
import socket
import os,hashlib

server = socket.socket()
server.bind(('localhost',6969))  # 指接口
server.listen()  # 监听
# conn 客户端在服务器端生成的连接实例
while True:
    conn, addr = server.accept()  # 接受
    while True:
        data = conn.recv(1024)  # 指接收的大小
        if not data:
            print('未收到信息，断开')
            break
        cmd,filename = data.decode().split('')
        print('文件名称:',filename)
        if os.path.isfile(filename):
            f = open(filename, 'rb')
            m = hashlib.md5()
            file_size = os.stat(filename).st_size
            conn.send(str(file_size).encode())
            conn.recv(1024)  # 等到client确认
            for line in f:
                m.update(line)
                conn.send(line)
            print('file md5', m.hexdigest())
            f.close()
            conn.send(m.hexdigest().encode())

        print('send done')



        # msg = data.upper()
        # print('recv:', msg.decode())
        # conn.send( str(len(msg.decode())).encode('utf-8') )  # 先把大小发给客户端
        # client_ack = conn.recv(1024)  # 等到client确认
        conn.send(data)

server.close()