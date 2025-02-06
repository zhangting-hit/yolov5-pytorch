import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from PIL import Image
import ast

# 定义 Pascal VOC XML 文件结构
def create_pascal_voc_xml(filename, width, height, depth, objects):
    annotation = ET.Element("annotation")

    folder = ET.SubElement(annotation, "folder")
    folder.text = "data"

    file = ET.SubElement(annotation, "filename")
    file.text = filename

    path = ET.SubElement(annotation, "path")
    path.text = "data/" + filename

    size = ET.SubElement(annotation, "size")
    width_elem = ET.SubElement(size, "width")
    width_elem.text = str(width)
    height_elem = ET.SubElement(size, "height")
    height_elem.text = str(height)
    depth_elem = ET.SubElement(size, "depth")
    depth_elem.text = str(depth)

    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"

    for obj in objects:
        object_elem = ET.SubElement(annotation, "object")
        name = ET.SubElement(object_elem, "name")
        name.text = "id_card"
        pose = ET.SubElement(object_elem, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object_elem, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object_elem, "difficult")
        difficult.text = "0"
        bndbox = ET.SubElement(object_elem, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(obj['xmin'])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(obj['ymin'])
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(obj['xmax'])
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(obj['ymax'])

    return annotation

# 格式化 XML 并写入文件
def write_pretty_xml(element, output_path):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)

# 读取 result.txt 文件并生成对应的 XML 文件
def convert_to_xml(txt_file_path, image_dir, output_dir):
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',', 1)
            if len(parts) != 2:
                continue

            filename = parts[0].strip()
            bbox_str = parts[1].strip()
            bbox = ast.literal_eval(bbox_str)
            xmin, ymin, xmax, ymax = map(float, bbox)

            # 获取图片尺寸
            image_path = os.path.join(image_dir, filename)
            with Image.open(image_path) as img:
                width, height = img.size
                depth = len(img.getbands())  # 获取图像的通道数

            objects = [{'xmin': int(xmin), 'ymin': int(ymin), 'xmax': int(xmax), 'ymax': int(ymax)}]
            annotation = create_pascal_voc_xml(filename, width, height, depth, objects)

            xml_filename = os.path.splitext(filename)[0] + ".xml"
            output_path = os.path.join(output_dir, xml_filename)
            write_pretty_xml(annotation, output_path)

# 主函数
def main():
    txt_file_path = "/home/zhangting/data/id_card_data/result.txt"  # 修改为实际路径
    image_dir = "/home/zhangting/data/id_card_data/id_card"  # 图片文件夹路径
    output_dir = "/home/zhangting/yolov5-pytorch/VOCdevkit/VOC2007/Annotations"  # 输出目录
    os.makedirs(output_dir, exist_ok=True)
    convert_to_xml(txt_file_path, image_dir, output_dir)

if __name__ == "__main__":
    main()
