import os
import shutil
import xml.etree.ElementTree as ET

# 定义源文件夹路径
xml_folder = "/home/zhangting/yolov5-pytorch/data/Annotations"
image_folder = "/home/zhangting/yolov5-pytorch/data/resized_hat_baidu"
destination_folder = "/home/zhangting/yolov5-pytorch/data/labeled_img"

# 遍历XML文件夹中的每个XML文件
for xml_file in os.listdir(xml_folder):
    if xml_file.endswith('.xml'):
        # 构建对应的图片文件名
        image_filename = xml_file.replace('.xml', '.jpg')  # 假设图片文件的扩展名为.jpg
        
        # 构建图片文件的完整路径
        image_path = os.path.join(image_folder, image_filename)
        
        # 检查图片文件是否存在
        if os.path.exists(image_path):
            # 移动图片文件到目标文件夹
            shutil.move(image_path, destination_folder)
            print(f"Moved {image_filename} to {destination_folder}")
        else:
            print(f"Image file {image_filename} not found in {image_folder}")