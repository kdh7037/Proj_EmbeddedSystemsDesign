# -*- coding: utf-8 -*-
import socket
import sys
import os
import numpy as np
import pdb
import serial

import cv2
import time
import math
from Image import *
from Utils import *
from picamera import PiCamera
from time import sleep

def write_serial(msg):
    print("My cmd is %s" % msg)
    ser.write(msg)
    ser.flush()


cnt = 0
width = 480 # 사진 가로 크기
height = 360 # 사진 세로 크기

try:
    ser = serial.Serial('/dev/ttyUSB0',9600) # USB 포트
except: # 0번이 없을 경우
    ser = serial.Serial('/dev/ttyUSB1',9600) # USB 포트
while True:
    try:
        camera = PiCamera() # PiCamera
        camera.resolution = (width, height) # 사진 크기 480 * 360으로 변경
        cnt += 1 # 사진 카운트
        camera.capture("/home/pi/Desktop/image/route" + str(cnt) + ".jpeg", use_video_port = True) # 사진 저장
        camera.close() # 카메라 끄기


        font = cv2.FONT_HERSHEY_SIMPLEX
        direction = 0

        #N_SLICES만큼 이미지를 조각내서 Images[] 배열에 담는다
        Images=[]
        N_SLICES = 3

        for q in range(N_SLICES):
            Images.append(Image())

        img = cv2.imread('/home/pi/Desktop/image/route' + str(cnt) + '.jpeg') # 사진 파일 읽어오기

        if img is not None:
            #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
            Points = SlicePart(img, Images, N_SLICES)

            #N_SLICES 개의 무게중심 점을 x좌표, y좌표끼리 나눈다
            x = []
            base = 255
            
            print(str(cnt) + "turn")
            for i in Points:
                x.append(i[0])
                print(i[0])
                
            print("\n")
            #
            if x[0] == None or x[0] < 5 or x[0] > (width-20): # 만약, x[0]가 읽히지 않거나 양쪽 끝에 치우쳐져 있다면
                if x[1] == None or x[1] < 5 or x[1] > (width-20): # 만약, x[1]이 읽히지 않거나 양쪽 끝에 치우쳐져 있다면
                    if x[2] == None or x[2] < 5 or x[2] > (width-20): # 만약, x[2]가 읽히지 않거나 양쪽 끝에 치우쳐져 있다면
                        cmd = ("H%d\n" % 200).encode('ascii') # 후진
                    elif x[2] > (width/2): # 만약, x[2]가 오른쪽이라면
                        cmd = ("B%d\n" % base).encode('ascii') # 극 우회전
                    else: # 만약, x[2]가 왼쪽이라면
                        cmd = ("A%d\n" % base).encode('ascii') # 극 좌회전
                elif x[1] > (width/2): # 만약, x[1]가 오른쪽이라면
                    cmd = ("B%d\n" % base).encode('ascii') # 극 우회전
                elif x[1] < (width/2): # 만약, x[2]가 왼쪽이라면
                    cmd = ("A%d\n" % base).encode('ascii') # 극 좌회전
            elif x[0] > (width * (2/3)) and x[1] > (width * (2/3)): # 만약, x[0]과 x[1]이 모두 오른쪽 1/3부근이라면
                cmd = ("L%d\n" % base).encode('ascii') # 우회전
            elif x[0] < (width/3) and x[1] < (width/3): # 만약, x[0]과 x[1]이 모두 왼쪽 1/3부근이라면
                cmd = ("R%d\n" % base).encode('ascii') # 좌회전
            elif abs(x[0] - x[1]) < (50 * width / 1920): # 만약, x[0] - x[1]의 절대값이. 일정 값 이하라면, 
                cmd = ("F%d\n" % 200).encode('ascii') # 직진
            else:
                gradient = 1.0 / (x[0] - x[1]) # gradient 계산
                #print(gradient * 1000)
                if gradient > 0: # x[0]이 x[1]보다 크다면
                    cmd = ("L%d\n" % base).encode('ascii') # 우회전
                else: # x[0]이 x[1]보다 작다면
                    cmd = ("R%d\n" % base).encode('ascii') # 좌회전

            write_serial(cmd) # 시리얼 통신
            ser.readLine() # 대기
        else:
            print('not even processed')
    except:
        continue



