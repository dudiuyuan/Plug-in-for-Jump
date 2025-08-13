import PIL, numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import warnings
warnings.filterwarnings("ignore")
import os
import subprocess
import random
import time
import threading

loop=False
def get_screenshot():
    process = subprocess.Popen('adb shell screencap -p', 
                               shell =True,stdout=subprocess.PIPE)
    if  process != None:
        screenshot = process.stdout.read()
        binary_screenshot = screenshot.replace(b'\r\r\n', b'\n')
        with open('autojump.png', 'wb') as f:
            f.write(binary_screenshot)
            print("Save the screenshot and then put it in the same directory!")

def find_piece_and_board(img):
    w, h= img.size
    piece_y_max = 0
    scan_x_side=int(w/8)
    scan_start_y=0
    img_pixel =img.load()
    if not loop:
        if sum(img_pixel[5,5][:-1])<150:
            stop()
    for i in range(int(h/3),int(h*2/3),50):
        first_pixel = img_pixel[0, i]
        for j in range(1,w):
            pixel = img_pixel[j, i]
            if pixel[0] != first_pixel[0] or pixel[1] != first_pixel[1] or pixel[2] != first_pixel[2]:
                scan_start_y =i-50
                break
        if scan_start_y:
            break    
    left=0
    right=0
    for i in range (scan_start_y, int(h*2/3)):
        flag =True
        for j in range (scan_x_side, w-scan_x_side):
            pixel = img_pixel[j, i]
            if (50 < pixel[0] < 60 )and(53<pixel[1]<63) and (95<pixel[2]<110):
                if flag:
                    left = j
                    flag = False
                right = j
                piece_y_max=max(i,piece_y_max)
    if not all((left, right)):
        return 0,0,0,0
    piece_x = (left + right) // 2
    board_x=0
    if piece_x < w / 2:
        board_x_start, board_x_end = w//2,2
    else:
        board_x_start, board_x_end = 0, w//2

    board_x_set=[]
    for by in range((h-w)//2,(h+w)//2,4):
        bg_pixel= img_pixel[0, by]
        for bx in range(board_x_start, board_x_end):
            pixel = img_pixel[bx, by]
            if (abs(pixel[0] - bg_pixel[0])+
                    abs(pixel[1] - bg_pixel[1])+
                    abs(pixel[2] - bg_pixel[2]) > 10):
                board_x_set.append(bx)
                

        if len(board_x_set) > 10:
            board_x = sum(board_x_set) / len(board_x_set)
            break
    print("Read the image and obtain the horizontal center coordinates of the chess pieces and board positions")
    return piece_x, board_x

def jump(piece_x, board_x,im,point):
    distanceX=abs(board_x - piece_x)
    shortEdge=min(im.size)
    jumpPercent=distanceX/shortEdge
    jumpFullWidth=1700
    press_time = round(jumpFullWidth * jumpPercent)
    press_time = 0 if not press_time else max(press_time, 200)
    cmd = 'adb shell input swipe {x1}{y1}{x2}{y2}{duration}'.format(
        x1=point[0], 
        y1=point[1],
        x2=point[0]+random.randint(0,3),
        y2=point[1]+random.randint(0,3),
        duration=press_time
    )
    os.system(cmd)
    print("Generate a compression command,jump!")
def stop():
    exit("Stop!")
  

        