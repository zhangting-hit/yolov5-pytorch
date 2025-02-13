import os   
from PIL import Image

# 定义源文件夹路径  
image_folder = "/home/zhangting/yolov5-pytorch/data/hat_selected"
destination_folder = "/home/zhangting/yolov5-pytorch/data/resized_image"
#保持原始长宽比，将长的一边resize成640，短的一边等比例缩放

# 遍历文件夹中的所有文件
for file_name in os.listdir(image_folder):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):  # 只处理图片文件
        image_path = os.path.join(image_folder, file_name)
        # 打开图片文件
        image = Image.open(image_path)
        # 如果图片为RGBA或P模式，转换为RGB模式
        if image.mode in ["RGBA", "P"]:
            image = image.convert("RGB")
        
        # 获取原始图像的宽和高
        width, height = image.size
        
        # 计算调整大小后的宽和高
        if width >= height:
            # 如果宽度大于等于高度，以宽度为基准，缩放宽度为640，高度按比例缩放
            new_width = 640
            new_height = int(height * (640 / width))
        else:
            # 如果宽度小于高度，以高度为基准，缩放高度为640，宽度按比例缩放
            new_height = 640
            new_width = int(width * (640 / height))
        
        # 调整图片大小并保持长宽比
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        
        # 保存调整大小后的图片
        resized_image.save(os.path.join(destination_folder, file_name))
        print(f"Resized {file_name} to {destination_folder}")
