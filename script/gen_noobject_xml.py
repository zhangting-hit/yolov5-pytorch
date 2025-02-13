import os
from PIL import Image
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

def create_xml(image_name, folder, path, width, height, depth=3):
    annotation = Element('annotation')

    folder_elem = SubElement(annotation, 'folder')
    folder_elem.text = folder

    filename_elem = SubElement(annotation, 'filename')
    filename_elem.text = image_name

    path_elem = SubElement(annotation, 'path')
    path_elem.text = path

    source_elem = SubElement(annotation, 'source')
    database_elem = SubElement(source_elem, 'database')
    database_elem.text = 'Unknown'

    size_elem = SubElement(annotation, 'size')
    width_elem = SubElement(size_elem, 'width')
    width_elem.text = str(width)
    height_elem = SubElement(size_elem, 'height')
    height_elem.text = str(height)
    depth_elem = SubElement(size_elem, 'depth')
    depth_elem.text = str(depth)

    segmented_elem = SubElement(annotation, 'segmented')
    segmented_elem.text = '0'

    # Create a pretty-printed XML string
    xml_string = xml.dom.minidom.parseString(tostring(annotation)).toprettyxml(indent="  ")
    return xml_string

def save_xml(xml_string, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_string)

def generate_xml_for_images(image_folder, xml_folder):
    if not os.path.exists(xml_folder):
        os.makedirs(xml_folder)

    image_list = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_name in image_list:
        image_path = os.path.join(image_folder, image_name)
        xml_name = os.path.splitext(image_name)[0] + '.xml'
        xml_path = os.path.join(xml_folder, xml_name)

        # Open the image to get its size
        with Image.open(image_path) as img:
            image_width, image_height = img.size

        xml_content = create_xml(image_name, os.path.basename(image_folder), image_path, image_width, image_height)
        save_xml(xml_content, xml_path)

        print(f'XML file saved to {xml_path}')

# Example usage
image_folder = '/home/zhangting/yolov5-pytorch/data/added_shapes_idcard_images'
xml_folder = '/home/zhangting/yolov5-pytorch/VOCdevkit/VOC2007/Annotations'

generate_xml_for_images(image_folder, xml_folder)
