import os
import cv2
import xml.etree.ElementTree as ET
from os import listdir, getcwd

# 设置类别，三类：‘strawberry’草莓 ‘immature strawberry’未成熟草莓 ‘flower’草莓花
classes = ['strawberry', 'immature', 'flower']

wd = os.getcwd()


# 定义坐标转换函数
def convert(size, box):
    # box里保存的是ROI感兴趣区域的坐标（x，y的最大值和最小值）
    # 返回值为ROI中心点相对于图片大小的比例坐标，和ROI的w、h相对于图片大小的比例
    # size[width, height]
    # box[xmin, ymin, xmax, yamx]
    dw = 1./(size[0])
    dh = 1./(size[1])
    # x: 归一化后的中心点x坐标
    # y: 归一化后的中心点y坐标
    # w: 归一化后的目标框宽度w
    # h: 归一化后的目标框高度h
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


# 读取图片文件名，写成列表存入image_ids
anns = os.listdir('annotations')

# 根据需求修改写入文件名
train_file = 'train.txt'
train_file_txt = ''

if not os.path.exists('labels'):
    os.makedirs('labels')


# 循环，批量操作
for ann in anns:
    image_id = ann[:-4]
    in_file = open('annotations/%s.xml' % image_id)
    out_file = open('labels/%s.txt' % image_id, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()

    # 获取图片信息（高和宽）
    # 假如xml文件中有图片信息，则直接找到那一行调用数值即可，就不用读图了
    img = cv2.imread('images/%s.jpg' % image_id)
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    # print("width is", w)
    # print("height is", h)
    # 判断所寻找类别在xml文件中存不存在
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue

        cls_id = classes.index(cls)
        # 如果存在类名，则继续找到bndbox里的内容
        xmlbox = obj.find('bndbox')

        box = (float(xmlbox.find('xmin').text),
               float(xmlbox.find('ymin').text),
               float(xmlbox.find('xmax').text),
               float(xmlbox.find('ymax').text))
        # print("box0 is", box[0])
        # print("box1 is", box[1])
        # print("box2 is", box[2])
        # print("box3 is", box[3])
        # 调用转换函数完成坐标转换
        bb = convert((w, h), box)
        # 将新坐标输出到txt文件中
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    train_file_txt = train_file_txt + wd + '/images/' + ann[:-3] + 'jpg\n'

with open(train_file, 'w') as outfile:
    outfile.write(train_file_txt)
    print("Finished")
