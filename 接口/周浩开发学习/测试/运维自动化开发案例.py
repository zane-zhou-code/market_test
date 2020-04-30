import paramiko

while 1 == 2:
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='192.168.112.28', port=3389, username='administrator', password='Xfm@2019')
    stdin, stdout, stderr = ssh.exec_command('df')
    print(stdout.read().decode('utf-8'))    # 以utf-8编码对结果进行解码
    ssh.close()

import threading

class MyThread(threading.Thread):
    def __init__(self, n):
        super(MyThread, self).__init__()
        self.n = n
    def run(self):
        print('running task', self.n)

# chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
# WebDriverWait(chrome_driver, 20, 0.5).until(EC.presence_of_all_elements_located(By.CLASS_NAME,'')
import select
import socket
import queue

server = socket.socket()
server.bind(('localhost', 9000))
server.listen(1000)

server.setblocking(False)  #  不阻塞

msg_dic = {}
inputs = [server,]
outputs = []
while 1 == 2:  #  while True:
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)
    for r in readable:
        if r is server: # 来了个新链接
            conn, addr = server.accept()
            inputs.append(conn)
            msg_dic[conn] = queue.Queue()  # 初始化一个队列，存要返回给客户端的数据
        else:
            data = r.recv(1024)
            msg_dic[r].put(data)
            outputs.append(r)  # 放入返回的链接队列
    for w in writeable:  # 要返回的数据
        data_to_client = msg_dic[w].get()
        w.send(data_to_client)  # 返回给客户端数据
        outputs.remove(w) #确保下次循环的时候writeable不返回这个处理完的数据

    #  异常删除客户端和队列
    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)
        del msg_dic[e]





if __name__ == '__main__':
    pass


