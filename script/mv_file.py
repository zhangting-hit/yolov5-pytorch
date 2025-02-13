import os
import shutil

# 源文件夹路径和目标文件夹路径
source_folder = '/home/zhangting/yolov5-pytorch/data/added_shapes_idcard_images'
target_folder = '/home/zhangting/yolov5-pytorch/VOCdevkit/VOC2007/JPEGImages'

# 遍历源文件夹中的所有文件和文件夹
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # 构造文件的完整路径
        source_file_path = os.path.join(root, file)
        # 构造文件在目标文件夹中的完整路径
        target_file_path = os.path.join(target_folder, file)
        # 移动文件
        shutil.copy(source_file_path, target_file_path)

print("所有文件已移动到目标文件夹中。")
