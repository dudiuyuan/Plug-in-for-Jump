# Plug-in-for-Jump
这是针对微信小程序：跳一跳的一个开挂python文件，侵权删
声明：仅用作个人学习，无商业用途，最终解释权归本账号实体所有人所有
如果觉得做的还ok的话，多多点star噢！
PS：跳一跳只有国内才有吧，那我就不写英文啦

需要的包：
import PIL
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import warnings
warnings.filterwarnings("ignore")
import os
import time
import threading
import auto
import numpy as np
import random
import io
import subprocess
import tempfile, shutil, glob
from PIL import Image
（大概需要下载的是pygame嘿嘿）

怎么使用？
1.克隆仓库
2.改目录名为Jump（应该包含copy和image文件夹）
3.更改路径（这边建议放在D:/Jump,不然就要自己改代码咯）
4.在D:/Jump下run d:/Jump/image/jump.py
5.打开开发者模式确保adb能运行（这样就限制于安卓咯）
6.点击自动，输入你想要循环的次数，回车
7.如果顺利（


1.0版本（2025/8/13）
基本可以运行，最高跑过1005分（时间还不够多，甚至比不上人手哈哈哈）
有时候会报错"SyntaxError: broken PNG file (chunk b'AT\x8a\x97')"
本人认为是手机端缓存过多，导致目标文件损坏，只能传输一半的屏幕截图
每一跳间隔时间较长：刚好能吃到一些等待奖励。
copy文件夹内是一些过往代码，值得研究（
