import time
import socket
import cv2
import numpy as np
import sys
from threading import Thread


def get_cam():
    '''这是从电脑摄像机获取视频的函数'''
    capture = cv2.VideoCapture(0)
    while True:
        ret, frames = capture.read()  # ret为返回值，frame为视频的每一帧
        yield frames
        cv2.imshow('the video in local', frames)
        c = cv2.waitKey(50)
    return frames


class Server():
    def __init__(self, frames, name):
        '''初始化函数'''
        super().__init__()
        # 表明该进程的名字
        self.name = name
        # 服务器本地地址
        # 初始化服务器
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.udp_socket = self.udp_socket.bind(addr)
        self.frames = frames

    def post_cam(self, frame, addr):
        '''这是将视频广播出去的函数'''
        frame = cv2.resize(frame, (360, 260))  # 控制画面大小
        img_encode = cv2.imencode('.jpg', frame)[1]
        data_encode = np.array(img_encode)
        data = data_encode.tobytes()
        self.udp_socket.sendto(data, addr)

    def log_save(self):
        '''由客户端得到具体信息，写入日志'''
        data, addr = self.udp_socket.recvfrom(1024)
        Note = open(f'{self.name}.txt', mode='w')
        Note.writelines('ip' + str(addr) + data)

    def run(self):
        addr = {'serv':('192.168.0.108', 8080)}
        for frame in self.frames:
            self.post_cam(frame, addr['serv'])
            # self.post_cam(frame, addr['向'])
            # self.post_cam(frame, addr['杨'])
        print(f'{self.name}的线程成功启动！')

if __name__ == "__main__":
    frames = get_cam()  # 调用本机的摄像机，只需一次，不用写入线程
    S = Server(frames, '123')
    S.run()

