import PIL, numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import warnings
warnings.filterwarnings("ignore")
import os
import time
import threading

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
    axes_image.set_array(get_screen_image())
    figure.canvas.draw()
                    
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

def auto_mode():
    global isAuto
    isAuto = True
    print("How many times do you want to jump?")
    print("Press Enter to start!")
    info = input()
    for i in range(int(info)):
        auto.get_screenshot()
        img =PIL.Image.open("autojump.png")
        piece_x, board_x = auto.find_piece_and_board(img)
        press_point =(random.randint(*[815,923]), random.randint(*[1509, 1658]))
        auto.jump(piece_x, board_x, img, press_point)
        update()
        time.sleep(2)
        if (i+1)==int(info):
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
    
    axes_image = plt.imshow(get_screen_image(),animated=True)
    figure.canvas.mpl_connect('button_press_event',on_click)

    plt.show()

    