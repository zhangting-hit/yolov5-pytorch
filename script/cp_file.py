import os
import shutil
from natsort import natsorted

# 源文件夹路径
source_folder = '/home/zhangting/data/id_card_forge/bank_forge'

# 目标文件夹路径
destination_folder = '/home/zhangting/yolov5-pytorch/VOCdevkit/VOC2007/JPEGImages'

# 创建目标文件夹，如果它不存在
os.makedirs(destination_folder, exist_ok=True)

# 获取源文件夹中的所有文件名，并排序
all_files = natsorted(os.listdir(source_folder))

# print(all_files[:100])
# 只选择前6000个文件
files_to_copy = all_files[0:5000]

# 复制文件到目标文件夹
for file_name in files_to_copy:
    source_file = os.path.join(source_folder, file_name)
    destination_file = os.path.join(destination_folder, file_name)
    shutil.copy2(source_file, destination_file)

print(f'Copied {len(files_to_copy)} files to {destination_folder}')
