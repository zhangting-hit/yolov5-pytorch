from PIL import Image, ImageDraw
import random
import os

from PIL import Image, ImageDraw
import random
import os

# 从txt文件中读取文件名和区域信息
def read_files_and_regions(txt_file):
    files_and_regions = []
    with open(txt_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(',')
            file_name = parts[0].strip()  # 文件名
            region_str = ','.join(parts[1:])  # 区域信息的字符串
            # 移除方括号和多余的空格
            region_cleaned = region_str.strip()[1:-1].split(',')
            region = [float(x.strip()) for x in region_cleaned]
            files_and_regions.append((file_name, region))
    return files_and_regions

# 定义形状列表
shapes = ['rectangle', 'ellipse']

def add_random_shapes(image, region):
    draw = ImageDraw.Draw(image)
    # 获取区域的边界
    left, top, right, bottom = region
    # 生成随机数量的形状
    num_shapes = random.randint(1, 3)
    for _ in range(num_shapes):
        # 随机选择形状
        shape = random.choice(shapes)
        # 生成随机位置和大小
        x1 = random.uniform(left, right)
        y1 = random.uniform(top, bottom)
        x2 = random.uniform(left, right)
        y2 = random.uniform(top, bottom)
        # 确保x2 > x1, y2 > y1
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        # 生成随机颜色
        color = tuple(random.choices(range(256), k=3))
        # 绘制形状
        if shape == 'rectangle':
            draw.rectangle([x1, y1, x2, y2], fill=color)
        elif shape == 'ellipse':
            draw.ellipse([x1, y1, x2, y2], fill=color)
    return image

# 创建输出目录
output_dir = '/home/zhangting/yolov5-pytorch/data/added_shapes_idcard_images'
os.makedirs(output_dir, exist_ok=True)

# 从TXT文件中读取文件和区域信息
txt_file = '/home/zhangting/data/id_card_data/result.txt'
files_and_regions = read_files_and_regions(txt_file)

# 处理每个文件
for file_name, region in files_and_regions:
    image = Image.open('/home/zhangting/data/id_card_data/id_card/' + file_name)
    modified_image = add_random_shapes(image, region)
    output_path = os.path.join(output_dir, file_name.replace('.jpg', '_shapes.jpg'))
    modified_image.save(output_path)

print("处理完成！")
