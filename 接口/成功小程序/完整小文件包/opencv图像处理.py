import cv2 as cv
import numpy as np

def video_demo():
    capture = cv.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        frame = cv.flip(frame, 1)
        cv.imshow('video', frame)
        c = cv.waitKey(50)
        if c == 27:
            break


def get_image_info(image):
    print(image.shape)
    print(image.size)
    print(image.dtype)
    pixel_data = np.array(image)
    print(pixel_data)


def access_pixels(image):
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    for row in range(height):
        for col in range(width):
            for c in range(channels):
                pv = image[row, col, c]
                image[row ,col, c] = 255 - pv
    cv.imshow('pixels_demo', image)


def inverse(image):
    dst = cv.bitwise_not(image)
    cv.imshow('inverse demo', dst)


def create_image():
    img = np.zeros([400, 400, 3], np.uint8)
    imgs = np.zeros([2, 2, 3], np.uint8)

    print(img)
    img[:, :, 0] = np.ones([400, 400])*255
    cv.imshow('new image', img)

def color_space_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow('gray', gray)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    cv.imshow('hsv', hsv)
    yuv = cv.cvtColor(image, cv.COLOR_BGR2YUV)
    cv.imshow('yuv', yuv)

def extract_object_demo():
    capture = cv.VideoCapture('')
    while True:
        ret, frame = capture.read()
        if ret == False:
            break
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_hsv = np.array([37, 43, 46])
        upper_hsv = np.array([77, 255, 255])
        mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
        dst = cv.bitwise_and(frame, frame, mask=mask)
        cv.imshow('video', frame)
        cv.imshow('mask', mask)
        c = cv.waitKey(40)
        if c == 27:
            break

def add_demo(m1, m2):
    dst = cv.add(m1, m2)
    dst2 = cv.subtract(m1, m2)
    dst3 = cv.divide(m1, m2)
    dst4 = cv.multiply(m1, m2)
    cv.imshow('add_demo', dst)
    cv.imshow('substract', dst2)
    cv.imshow('divide', dst3)
    cv.imshow('multiply', dst4)

def others(m1, m2):
    M1, dev1 = cv.meanStdDev(m1)  # 方差和标准差
    M2, dev2 = cv.meanStdDev(m2)  # 方差和标准差
    print(M1, dev1)
    print(M2, dev2)

def logic_demo(m1, m2):
    cv.bitwise_and(m1, m2)  # 与
    cv.bitwise_or(m1, m2 )  # 或
    cv.bitwise_not(m1)  # 非

def contrast_brightness_demo(image, c, b):
    h, w, ch = image.shape[:]
    blank = np.zeros([h, w, ch], image.dtype)
    dst = cv.addWeighted(image, c, blank, 1-c, b)
    cv.imshow('con-bri-demo', dst)

def fill_color_demo(image):
    copyImg = image.copy()
    h, w = image[:2]
    mask = np.zeros([h+2, w+2], np.uint8)
    cv.floodFill(copyImg, mask, (30, 30), (0, 255, 255), (100, 100, 100)
                 , (50, 50, 50), cv.FLOODFILL_FIXED_RANGE)


src = cv.imread(r'C:\Users\admin\Desktop\1.jpg')
cv.namedWindow('input image', cv.WINDOW_AUTOSIZE)
cv.imshow('input image', src)
# # 获取图像信息
# get_image_info(src)
# video_demo()
# # 以灰色保存图片
# gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# cv.imwrite(r'C:\Users\admin\Desktop\2.jpg', gray)
# # 获取图片转换图片与时间
# t1 = cv.getTickCount()
# access_pixels(src)
# t2 = cv.getTickCount()
# print('time:%s ms' % ((t2-t1)/cv.getTickFrequency()*1000))
# # 创建图像
# create_image()
# # 各种颜色编码
# color_space_demo(src)
# # 颜色切割与展示
# b, g, r = cv.split(src)
# cv.imshow('blue', b)
# cv.imshow('green', g)
# cv.imshow('red', r)
# src[:, :, 1] = 0
# cv.imshow('changed image', src)

# #  取图片部分并转换灰度图像
# face = src[210:280, 110:150]
# gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
# cv.imshow('gray', gray)
# backface = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
# cv.imshow('backface', backface)
# cv.imshow('face', face)
cv.waitKey(0)
cv.destroyAllWindows()
print('结束')