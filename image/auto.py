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
import os, subprocess, time, tempfile, shutil
import os, subprocess, time, io, tempfile, shutil, glob
from PIL import Image


loop=False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "autojump.png")
PNG_SIG = b'\x89PNG\r\n\x1a\n'


def _atomic_write(path: str, data: bytes):
    fd, tmp = tempfile.mkstemp(dir=BASE_DIR, prefix="autojump_", suffix=".png")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    shutil.move(tmp, path)


def _is_valid_png(data: bytes) -> bool:
    return data.startswith(PNG_SIG) and len(data) > 1024


def get_screenshot(retries: int = 3, sleep_sec: float = 0.15, serial: str | None = None) -> str:
    """
    截图到 autojump.png 并返回其绝对路径；失败抛异常（不会返回 None）。
    可选 serial 指定设备：例如 '28946c44'。
    """
    base = ["adb"]
    if serial:
        base += ["-s", serial]

    last_err = ""

    for attempt in range(1, retries + 1):
        # A. 直接用 exec-out 拿字节流
        proc = subprocess.run(base + ["exec-out", "screencap", "-p"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = proc.stdout, proc.stderr
        if proc.returncode == 0 and out:
            data = out.replace(b'\r\r\n', b'\n')
            if _is_valid_png(data):
                _atomic_write(IMG_PATH, data)
                print(f"Saved screenshot: {IMG_PATH}")
                return IMG_PATH
            else:
                # 记录前 120 字节便于判断是不是错误文本
                last_err = f"exec-out returned non-PNG, head={data[:120]!r}"

        # B. 兜底：落盘到 /sdcard 再 pull
        r1 = subprocess.run(base + ["shell", "screencap", "-p", "/sdcard/autojump.png"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        if r1.returncode == 0:
            r2 = subprocess.run(base + ["pull", "/sdcard/autojump.png", IMG_PATH],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            if r2.returncode == 0 and os.path.exists(IMG_PATH):
                with open(IMG_PATH, "rb") as f:
                    data = f.read()
                if _is_valid_png(data):
                    print(f"Saved screenshot: {IMG_PATH}")
                    return IMG_PATH
                else:
                    last_err = f"pulled file is non-PNG, head={data[:120]!r}"
            else:
                last_err = f"adb pull failed: {r2.stderr.decode(errors='ignore')}"
        else:
            last_err = f"screencap to /sdcard failed: {r1.stderr.decode(errors='ignore')}"

        if attempt < retries:
            time.sleep(sleep_sec)

    raise RuntimeError(f"Failed to capture valid PNG. Detail: {last_err}")


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
        board_x_start, board_x_end = w//2,w
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
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
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
