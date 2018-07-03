# encoding = utf-8
from socket import socket
from threading import Thread


def main():
    
    class ClientHandler(Thread):

        def __init__(self, client):
            super().__init__()
            self._client = client

        def run(self):
            nonlocal clients
            while True:
                try:
                    # 接收数据
                    data = self._client.recv(1024)
                    # 移出掉发送数据的客户端
                    clients.remove(self._client)
                    text = data.decode("utf-8")
                    #  decode send data
                    print(addr, '客户端发来消息！' + text)
                    # 发送给其他客户端
                    row, col = eval(text)
                    send_data = (("%d,%d,%d")%(row,col, -1)).encode("utf-8")
                    # add client number is negative one, the client won't quit
                    if row >= 0 and col >= 0:
                        for client in clients:
                            client.send(send_data)
                        # 进行完上面的操作后，再把删掉的客户端重新添加进去
                    self_send_data = (("%d,%d,%d")%(-1,-1,len(clients)+1)).encode("utf-8")
                    self._client.send(self_send_data)
                    clients.append(self._client)
                except ConnectionResetError:
                    if self._client in clients:
                        # 当有客户端断开链接的时候，移除掉该客户端
                        clients.remove(self._client)
                        print('有客户端断开连接:', self._client)
    
    # 创建一个套接字
    server = socket()
    try:
        # 建立连接
        server.bind(('127.0.0.1', 6789))
        # 开始监听
        server.listen(512)
        print('服务器已经启动！正在监听...')
        clients = []
        while True:
            # 当前连接上的客户端
            curr_client, addr = server.accept()
            clients.append(curr_client)
            print(addr[0], '连接到服务器！目前有%d个客户端连接着服务器' % len(clients))
            # 启动数据接收发送线程
            ClientHandler(curr_client).start()
    except OSError:
        print('请关闭相关程序或者重启服务器！')


if __name__ == '__main__':
    main()