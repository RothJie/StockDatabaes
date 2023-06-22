import time
import pyautogui   # 需要pip install Pillow和pip install opencv-python 配合使用
import pyperclip   # 用来复制
import re
import datetime

pyautogui.PAUSE = 2  # 设置箭头大小为2
pyautogui.FAILSAFE = True  # 设置安全函数


pyautogui.hotkey('win', 'd')


# 获取截图位置
def ToPngLocation(pn: str):
    pos = pyautogui.locateOnScreen(pn, confidence=0.8)
    pos1 = pyautogui.locateCenterOnScreen(pn, confidence=0.8)
    return pos, pos1


time.sleep(2)


def EnterAPP():
    pyautogui.moveTo(ToPngLocation('dongcaiapp.png')[1])
    pyautogui.doubleClick()
    time.sleep(8)
    pyautogui.hotkey('esc')


# 点击加号，进行自选操作
def Sp():
    pyautogui.moveTo(ToPngLocation('003.png')[1])
    pyautogui.click()


EnterAPP()
pyautogui.moveTo(ToPngLocation('002.png')[1])
pyautogui.click()
Sp()


# 输入股票代码将股票添加到自选
def InData(d: list):
    for code in d:
        pyautogui.click(993, 404)
        pyautogui.click(1204, 358)
        pyperclip.copy(code)   # 复制代码到粘贴板上
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')


# 建立分组函数
def BuiltGroup(name: str):
    pyautogui.click(768, 403)
    time.sleep(0.5)
    pyautogui.typewrite(name)
    pyautogui.press('enter')
    # time.sleep(0.5)
    # pyautogui.press('enter')


with open(file=r'..\GetScore\成交量异常放大.txt', encoding='utf8', mode='r') as f:
    info = f.read()

with open(file=r'..\SuccesionBoardStock\上板日志.txt', encoding='utf8', mode='r') as f1:
    info1 = f1.read()

obj = re.compile(r"[06][0-9]{5,}")
lis1 = obj.findall(info)
lis2 = obj.findall(info1)

InData(lis1)  # 添加到低位

BuiltGroup(f"{datetime.datetime.today().strftime('%Y%m%d')}")  # 以日期为自选名字
Sp()
InData(lis2)
pyautogui.moveTo(ToPngLocation('004.png')[1])
pyautogui.click()


