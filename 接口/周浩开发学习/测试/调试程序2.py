# 客户端
import socket
import hashlib

# 声明socket类型，同时生成连接对象
client = socket.socket()
client.connect(('localhost',9999))  # 指接口

while True:
    msg = input(">>:").strip()
    if len(msg) == 0:continue
    client.send(msg.encode())
    data = client.recv(1024)
    print('recv:', data.decode())

client.close()
