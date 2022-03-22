import os
import shutil

# 读取annotations中所有文件
# 读取images中所有文件
# 将
anns = os.listdir('annotations')
images = os.listdir('images')

train_file_txt = ''
wd = os.getcwd()

def moverecursively(source_folder, destination_folder):
    basename = os.path.basename(source_folder)
    dest_dir = os.path.join(destination_folder, basename)
    if not os.path.exists(dest_dir):
        shutil.move(source_folder, destination_folder)
    else:
        dst_path = os.path.join(destination_folder, basename)
        for root, dirs, files in os.walk(source_folder):
            for item in files:
                src_path = os.path.join(root, item)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.move(src_path, dst_path)
            for item in dirs:
                src_path = os.path.join(root, item)
                moverecursively(src_path, dst_path)


for ann in anns:
    ann_id = ann[:-4]
    for image in images:
        image_id = image[:-4]
        if ann_id.__eq__(image_id):
            print('ann id: ', ann_id[:-1])
            print('image id: ', image_id[:-1])
            print('match')
            str1 = 'images/' + image_id + '.jpg'
            outpath = wd + '/match'
            moverecursively(str1, outpath)
        else:
            print('dis match')


