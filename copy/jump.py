import PIL, numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import warnings
warnings.filterwarnings("ignore")
import os
import time
import threading
import auto
import numpy as np

coor=[]
ax=None
isAuto=False

def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')
    os.system('adb pull /sdcard/screen.png d:/Jump/screen.png')
    return numpy.array(PIL.Image.open("screen.png"))

def on_click(event):
    if isAuto == False:
        if event.xdata !=None and event.ydata !=None:
            x=float(event.xdata)
            y=float(event.ydata)
            if x>70 and y>70:
                coor.append((x,y))
                if len(coor) == 1:
                    print("checked starting point")
                else:
                    print("checked ending point")
                global ax
                ax =figure.add_subplot(1,1,1)
                ax.plot(x,y,'r*')
                figure.canvas.draw()
                if len(coor) == 2:
                    jump_to_next(coor.pop(), coor.pop())
                    ax.lines.clear()
                    th=threading.Thread(target=update)
                    th.start()
    else:
        print("Auto mode is enabled!")

def jump_to_next(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance= ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    os.system('adb shell input swipe 550 1550 550 1550 {}'.format(int(distance * 1.35)))
    print("Jump!")

def update():
    time.sleep(0.8)
    print("Updating screen...")
    pil_img = auto.get_screenshot_image()
    axes_image.set_array(np.array(pil_img))
    figure.canvas.draw_idle()
                    
def button_click(event):
    if len(coor) < 2 and ax != None:
        coor.clear()
        ax.lines.clear()
        figure.canvas.draw()

def auto_click(event):
    th = threading.Thread(target=auto_mode)
    th.start()
import auto    
import random

# def auto_mode():
#     global isAuto
#     isAuto = True
#     print("How many times do you want to jump?")
#     print("Press Enter to start!")
#     info = input()
#     for i in range(int(info)):
        
#         # img =PIL.Image.open("autojump.png")#(1)
#         # img =PIL.Image.open(auto.get_screenshot())#2
#         # piece_x, board_x = auto.find_piece_and_board(img)
#         try:
#             img_path = auto.get_screenshot()   # 一定返回字符串路径
#             # img = PIL.Image.open(img_path)     # 用路径打开
#             with PIL.Image.open(img_path) as im:
#                 img = im.convert("RGB").copy()
#         except Exception as e:
#             print(f"[AUTO] Screenshot failed: {e}")
#             return  # 或者 break / continue，看你的逻辑

#         piece_x, board_x = auto.find_piece_and_board(img)
#         press_point =(random.randint(*[815,923]), random.randint(*[1509, 1658]))
#         auto.jump(piece_x, board_x, img, press_point)
#         update()
#         time.sleep(2)
#         if (i+1)==int(info):
#             isAuto = False
#             print("Jump completed!")
         
# def countdown(n=3):
#     for k in range(n, 0, -1):
#         print(f"{k}…")
#         time.sleep(1)

# def auto_mode():
#     global isAuto
#     if isAuto:
#         print("Auto already running…"); return
#     isAuto = True
#     try:
#         print("How many times do you want to jump?")
#         print("Press Enter to start!")
#         times = int(input())

#         for i in range(times):
#             # 读秒，给画面稳定的时间（也可放在 jump() 之后）
#             countdown(3)   # 想更稳可用 3

#             try:
#                 # 直接内存截图，save_debug_every=10 表示每 10 次留一张文件
#                 pil_img = auto.get_screenshot_image(save_debug_every=10)
#             except Exception as e:
#                 print(f"[AUTO] Screenshot failed: {e}")
#                 break

#             # 交给你的检测函数（它接收 PIL.Image）
#             piece_x, board_x = auto.find_piece_and_board(pil_img)

#             # 随机按压点
#             press_point = (random.randint(815, 923), random.randint(1509, 1658))
#             auto.jump(piece_x, board_x, pil_img, press_point)

#             # 更新可视化（把 PIL 转 ndarray）
#             axes_image.set_array(np.array(pil_img))
#             figure.canvas.draw_idle()

#             # 等棋子落稳再下一轮
#             time.sleep(1.0)

#             # 定期清理旧的调试图
#             if (i + 1) % 20 == 0:
#                 auto.cleanup_debug_images(keep=10)

#         print("Jump completed!")
#     finally:
#         isAuto = False

def auto_mode():
    global isAuto
    isAuto = True
    print("How many times do you want to jump?")
    print("Press Enter to start!")
    info = input()
    for i in range(int(info)):
        try:
            img_path = auto.get_screenshot()      # 只调用一次
            img = PIL.Image.open(img_path)
        except Exception as e:
            print(f"[AUTO] Screenshot failed: {e}")
            return

        piece_x, board_x = auto.find_piece_and_board(img)
        press_point = (random.randint(815, 923), random.randint(1509, 1658))
        auto.jump(piece_x, board_x, img, press_point)
        update()
        time.sleep(2)
        if (i + 1) == int(info):
            isAuto = False
            print("Jump completed!")

if __name__ == "__main__":
    figure = plt.figure()
    reelect_button_position = plt.axes([0.79, 0.8, 0.1,0.08])
    m = numpy.array(PIL.Image.open("image/bt.png"))

    reelect_button = Button(reelect_button_position, label="",image=m)
    m1 = numpy.array(PIL.Image.open("image/bt1.png"))
    auto_button_position = plt.axes([0.79, 0.65, 0.1,0.08])
    reelect_button.on_clicked(button_click)

    auto_button = Button(auto_button_position, label="", image=m1)
    auto_button.on_clicked(auto_click)
    ax_img = plt.axes([0.05, 0.05, 0.7, 0.9])
    axes_image = plt.imshow(get_screen_image(),animated=True)
    figure.canvas.mpl_connect('button_press_event',on_click)

    plt.show()

    