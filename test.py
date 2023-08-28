import pandas as pd
import cv2 as cv

# data = pd.read_csv('./data/data.csv')
# print(data.head(0))

p1 = './data/aabb.jpg'
p2 = './data/djz.jpg'

# img = cv.imread(p2)

# # 打印出图片尺寸
# print(img.shape)
# # 将图片高和宽分别赋值给x，y
# x, y = img.shape[0:2]
 
# # 显示原图
# cv.imshow('OriginalPicture', img)
 
# # 缩放到原来的二分之一，输出尺寸格式为（宽，高）
# img_test1 = cv.resize(img, (int(y / 2), int(x / 2)))
# cv.imshow('resize0', img_test1)
# cv.waitKey()
 
# 最近邻插值法缩放
# 缩放到原来的四分之一
# print(img.shape)

# img_test2 = cv.resize(img, (0, 0), fx=0.25, fy=0.25, interpolation=cv.INTER_NEAREST)
# cv.imshow('resize1', img_test2)
# cv.waitKey()
# cv.destroyAllWindows()


# info_data = pd.read_csv('./data/info_data.csv')
# print(info_data)

# name = info_data[(info_data.num == 12)]
# print(name)
# print(name.shape)
# print(name.values[0][1])

# data = pd.read_csv('./data/record_data.csv')
# print(data.head())

# t = data.values
# print(t.shape)
# print(t)

# print(t[0][0])
# print(t[0][1])
# print(t[0][2])


print('P1和P2的距离： 0.13')
print('P3和P4的距离： 2.72')
print('P3和P5的距离： 1.07')