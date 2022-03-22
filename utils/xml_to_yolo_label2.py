import shutil
import xml.etree.ElementTree as ET
import os
from os import getcwd

# ------------------------------ 修改内容 ----------------------------------
labelsfilepath = r'F:\目标检测\strawberry\new2\train\annotations'  # xml文件的地址，根据自己的数据进行修改 xml一般存放在Annotations下
txtsavepath = r'F:\目标检测\strawberry\new2\train'  # 数据集的划分，地址选择自己数据下的ImageSets/Main
labelspath = r'F:\目标检测\strawberry\new2\train\annotations\labels'
sets = ['train', 'val', 'test']
classes = ['strawberry', 'immature', 'flower']  # 改成自己的类别
# -------------------------------------------------------------------------
abs_path = os.getcwd()
print(abs_path)


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open(os.path.join(labelsfilepath, '%s.xml' % image_id), encoding='UTF-8')
    out_file = open(os.path.join(labelspath, '%s.txt' % image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        # difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

if os.path.exists(labelspath):
    shutil.rmtree(labelspath)
os.makedirs(labelspath)

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

for image_set in sets:
    image_ids = open(os.path.join(txtsavepath, '%s.txt' % (image_set))).read().strip().split()
    list_file = open(os.path.join(labelsfilepath, '../%s.txt' % (image_set)), 'w')
    for image_id in image_ids:
        list_file.write(os.path.join(labelsfilepath, '../images/%s.jpg\n' % (image_id)))
        convert_annotation(image_id)
    list_file.close()
