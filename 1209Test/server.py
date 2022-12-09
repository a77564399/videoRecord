import socket
import cv2
import sys
import time
import datetime
import getpass
import numpy as np


class Individual():
    def __init__(self, addr):
        '''初始化函数'''
        self.address = addr

    def log(self):
        '''创建日志'''
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        user = getpass.getuser()  # 获取连接者的用户名
        now_time = datetime.datetime.now().strftime('%F %T')
        data = f'user{user} in {now_time}use the monitor'
        # s.sendto(data.encode("utf-8"),addr)
        Note = open(f'{user}.txt', mode='w')
        Note.writelines('ip' + str(self.address) + data)

    def receive_save(self):
        '''接受发送的视频，并且保存到本地'''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(self.address)
        # 下面这部分是发送日志内容
        # user = getpass.getuser()  #获取连接者的用户名
        # now_time = datetime.datetime.now().strftime('%F %T')
        # data = f'用户{user}在{now_time}调用了监控'
        # s.sendto(data.encode("utf-8"),addr)
        # 下面开始视频展示
        imgs = []
        while True:
            data, addr = s.recvfrom(400000)
            nparr = np.frombuffer(data, np.uint8)
            img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.startWindowThread()
            cv2.imshow('receive', img_decode)  # 视频展示
            c = cv2.waitKey(50)
            if c == 27:  # 按了esc候可以退出
                break
            # 一帧一帧保存图片成视频
            imgs.append(img_decode)
            v = cv2.VideoWriter(f'D:/cam.avi', \
                                cv2.VideoWriter_fourcc(*'MJPG'), 5, (360, 300))
            for i in imgs:
                i = cv2.resize(i, (360, 300))
                v.write(i)

    def run(self):
        self.log()
        self.receive_save()


if __name__ == '__main__':
    addr = (sys.argv[1], int(sys.argv[2]))
    use = Individual(addr)
    use.run()