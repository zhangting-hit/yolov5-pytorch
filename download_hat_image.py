import os
import requests

def download_images(file_path, target_folder):
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 读取文本文件中的图片链接
    with open(file_path, 'r') as file:
        image_urls = file.readlines()

    # 下载每张图片
    for url in image_urls:
        url = url.strip()  # 去除首尾空格和换行符
        filename = os.path.basename(url)  # 提取链接中的文件名
        target_path = os.path.join(target_folder, filename)

        # 下载图片
        response = requests.get(url)
        if response.status_code == 200:
            with open(target_path, 'wb') as image_file:
                image_file.write(response.content)
                print(f"下载成功: {filename}")
        else:
            print(f"下载失败: {filename}")

# 测试示例
file_path = 'data/hat.txt'  # 包含图片链接的文本文件路径
target_folder = 'VOCdevkit/VOC2007/test'  # 图片下载目标文件夹
download_images(file_path, target_folder)
