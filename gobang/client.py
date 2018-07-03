# encoding = utf-8
from socket import socket
import pygame
import re
from threading import Thread


EMPTY = 0   # 没有棋子的时候
BLACK = 1  # 黑子
WHITE = 2  # 白子
black_color = [0, 0, 0]
white_color = [255, 255, 255]


class GoBang(object):
    """棋盘类"""
    def __init__(self):
        self._board = [[]] * 15
        self.reset()

    def reset(self):
        """重置函数"""
        for row in range(len(self._board)):
            self._board[row] = [EMPTY] * 15

    def draw(self, screen):
        """画棋盘"""
        for i in range(1, 16):
            pygame.draw.line(screen, black_color, [40, i * 40], [600, i * 40], 1)
            pygame.draw.line(screen, black_color, [i * 40, 40], [i * 40, 600], 1)
        pygame.draw.rect(screen, black_color, [36, 36, 568, 568], 4)
        pygame.draw.circle(screen, black_color, [320, 320], 3, 0)  # 画圆， 最后的0代表实心
        pygame.draw.circle(screen, black_color, [480, 160], 3, 0)
        pygame.draw.circle(screen, black_color, [160, 480], 3, 0)
        pygame.draw.circle(screen, black_color, [480, 480], 3, 0)
        pygame.draw.circle(screen, black_color, [160, 160], 3, 0)
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] != EMPTY:
                    c_color = black_color \
                        if self._board[row][col] == BLACK else white_color
                    pos = [40 * (col + 1), 40 * (row + 1)]
                    pygame.draw.circle(screen, c_color, pos, 20, 0)

    @property
    def board(self):
        return self._board

    def move(self, row, col, is_black):
        """下棋"""
        if 0 <= row <= 14 and 0 <= col <= 14:
            if self._board[row][col] == EMPTY:
                self._board[row][col] = BLACK if is_black else WHITE
                return True
            return False
        return False

    def clear(self, screen):
        """清理棋盘"""
        self._board = [[0] * 15 for _ in range(15)]

    def is_win(self, row, col):
        """判断是否胜利"""

        # 列表存储4条线， 2同一线上的不同方向， 2个值代表row 与 col 的增加和减少
        list1 = [
            [[0, -1], [0, 1]],
            [[-1, 0], [1, 0]],
            [[-1, -1], [1, 1]],
            [[-1, 1], [1, -1]]
        ]
        for i in range(4):
            count = 1
            for j in range(2):
                temp1 = row
                temp2 = col
                while True:
                    temp1 += list1[i][j][0]  # 减少之后row的值
                    temp2 += list1[i][j][1]  # 减少之后col的值
                    if 0 <= temp1 <= 14 and 0 <= temp2 <= 14:
                        if self._board[row][col] == \
                                self._board[temp1][temp2]:
                            count += 1 # 与放上去的棋子相邻的且颜色相同，count + 1
                        else:
                            break  # 只要有一个不是，结束while循环，进行，同一条线，另一个方向的判断
                    else:
                        break
            if count >= 5:
                return True
        return False


def main():
    def refresh():
        """刷新界面操作"""
        screen.fill([218, 165, 105])
        go_bang.draw(screen)
        pygame.display.flip()
    
    def start_game(row, col):
        """游戏开始"""
        nonlocal status, is_black, is_recv
        # print(row, col)
        if status == 0:
            if go_bang.move(row, col, is_black):
                refresh()
                if go_bang.is_win(row, col):
                    #print(go_bang.is_win(row, col))
                    my_font = pygame.font.SysFont('arial', 60)
                    # 判断谁胜谁负
                    if is_black:
                        text = my_font.render('b l a c k   i s   w i n !', True, (255, 0, 0))
                    else:
                        text = my_font.render('w h i t e   i s   w i n !', True, (255, 0, 0))
                    screen.blit(text, (120, 280))
                    pygame.display.flip()
                    status = 1
                is_black = not is_black
    
    class ClientRecv(Thread):
        def __init__(self, client):
            super().__init__()
            self._client = client

        def run(self):
            """接收数据线程"""
            nonlocal is_recv
            while True:
                data = self._client.recv(1024)
                text = data.decode('utf-8')
                row, col, num = eval(text) # 将 x, y，num字符串转化成元组
                if num == -1:
                    is_recv = True #确保当前客户端发来的信息不是自己发的
                if(num > 2): # 已经存在的客户端数量大于2
                    print("already exist 2 clients")
                    pygame.quit()
                    break # 结束线程，断开当前客户端
                    # 退出循环，然后当前客户端断开与服务器连接
                elif (row >= 0 and col >= 0) and is_recv:
                    start_game(row, col)

    myclient = socket()
    myclient.connect(('127.0.0.1', 6789))
    status = 0  # 状态类，等于0的时候游戏可以继续，等于1的时候，游戏停止
    pygame.init()
    pygame.display.set_caption('五子棋游戏')
    screen = pygame.display.set_mode([640, 640])  # 设置窗口大小
    screen.fill([218, 165, 105])  # 填充背景颜色
    go_bang = GoBang()
    go_bang.draw(screen)
    pygame.display.flip()  # 刷新界面
    is_black = True  # 判断是否是黑棋
    is_recv = False # 判断是否接收到了数据
    index = 0  # index为0时，表示第一次走棋，此时没有recv
    running = True
    ClientRecv(myclient).start() # 启动接收数据的线程
    myclient.send(('(%d, %d)' % (-1, -1)).encode('utf-8')) # 发送数据, 用字符串的形式发送
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 关闭窗口
                myclient.close()
                running = False
            elif event.type == pygame.KEYDOWN:  # 判断键盘按钮
                if status == 1:
                    status = 0
                    go_bang.clear(screen)  # 清空所有棋子
                    refresh()
                    is_black = True
                    is_recv = False
                    index = 0
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and event.button == 1:  # 鼠标键
                x, y = event.pos
                row = round((y - 40) / 40)
                col = round((x - 40) / 40)
                print(go_bang.board[row][col])
                if (is_recv or index == 0) and go_bang.board[row][col] == 0:
                    start_game(row, col)
                    index = 1
                    myclient.send(('(%d, %d)' % (row, col)).encode('utf-8')) # 发送数据, 用字符串的形式发送
                    is_recv = False 
    pygame.quit()


if __name__ == '__main__':
    main()