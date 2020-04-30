import socketserver
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data.decode())
            self.request.sendall(self.data.upper())
        except ConnectionResetError as e:
            print('err:', e)
            exit()

if __name__ == "__main__":
    HOST, POST = "localhost", 9999
    server = socketserver.ThreadingTCPServer((HOST, POST), MyTCPHandler)
    server.serve_forever()
