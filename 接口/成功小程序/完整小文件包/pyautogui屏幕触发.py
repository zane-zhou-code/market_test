import pyautogui
import pyperclip
import os,time,random

# 查找图片，并双击
def mapping_img(img, click):
    box_location = pyautogui.locateOnScreen(img)
    print(box_location)
    center = pyautogui.center(box_location)
    print(center)
    if click == 'double':
        pyautogui.doubleClick(center)
    else:
        pyautogui.leftClick(center)
# 选择发送用户
def chat_user(user):
    if user !='':
        mapping_img('search.png', 'single')
        pyautogui.typewrite(user)
        time.sleep(1)
        pyautogui.moveRel(xOffset=0, yOffset=80)
        pyautogui.click()
        time.sleep(1)
    else:
        mapping_img('aa.png', 'single')
        mapping_img('bb.png', 'single')
# 读取文本
def read_txt(txt):
    file = open(txt, 'r', encoding='utf-8')
    filecontent = file.readlines()
    number = random.randint(0, len(filecontent)-1)
    pyperclip.copy(filecontent[number])
    pyautogui.hotkey('ctrl', 'v')
    file.close()
# 读图片等文件
def read_image(img_name):
    mapping_img('pic.png', 'single')
    img_path = 'C:\\Users\\admin\\Desktop\\pyauto鼠标点击\\' + img_name
    pyautogui.typewrite(img_path)
    pyautogui.press('enter')

def main():
    # os.chdir(r'C:\Users\admin\Desktop\pyauto鼠标点击')
    # mapping_img('trade.png', 'double')
    im2 = pyautogui.screenshot('my_screenshot.png')
    # pass

if __name__ == '__main__':
    main()