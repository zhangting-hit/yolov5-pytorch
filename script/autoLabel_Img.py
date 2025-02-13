import os
from http import HTTPStatus
import cv2
import dashscope
import xml.etree.ElementTree as ET
import re

# dashscope.api_key = 'sk-b4db6a817cce4cbe9f98088811c08a0b'#xyk
dashscope.api_key = 'sk-e293520a046641c89509dc328569d1c5'#xkx

xml_path = '/home/zhangting/yolov5-pytorch/data/Annotations'

def save_xml_with_boxes(image_path, filename, image_width, image_height, boxes):
    # 构建XML字符串
    xml_output = f'''<annotation>
        <folder>image</folder>
        <filename>{filename}</filename>
        <path>{image_path}</path>
        <source>
            <database>Unknown</database>
        </source>
        <size>
            <width>{image_width}</width>
            <height>{image_height}</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>
    '''
    # 添加帽子位置信息
    for box_index, box in enumerate(boxes):
        xmin, ymin, xmax, ymax = box
        xml_output += f'''
        <object>
            <name>hat</name>
            <pose>Unspecified</pose>
            <truncated>0</truncated>
            <difficult>0</difficult>
            <bndbox>
                <xmin>{int(xmin / 1000 * image_width)}</xmin>
                <ymin>{int(ymin / 1000 * image_height)}</ymin>
                <xmax>{int(xmax / 1000 * image_width)}</xmax>
                <ymax>{int(ymax / 1000 * image_height)}</ymax>
            </bndbox>
        </object>
        '''
    xml_output += "</annotation>"

    # 保存XML文件
    xml_file = os.path.join(xml_path, filename.split('.')[0] + ".xml")
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml_output)
    print(f"XML文件已保存为 {xml_file}")


def simple_multimodal_conversation_call(image_path):
    """Simple single round multimodal conversation call.
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_path},
                {"text": "帮我框图中的帽子"}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                     messages=messages)
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response)
        filepath = messages[0]["content"][0]["image"]
        filename = os.path.basename(filepath)
        print("图片路径：", filepath)
        print("图片文件名：", filename)
        image = cv2.imread(filepath)
        height, width = image.shape[:2]
        # 从模型输出中提取帽子位置信息
        box_infos = response["output"]["choices"][0]["message"]["content"]
        print("帽子位置信息：", box_infos)  # 调试输出帽子位置信息
        if box_infos is None:
            # 未检测到帽子，保存空的XML文件
            save_xml_with_boxes(filepath, filename, width, height, [])
        else:
            boxes = []
            for box_info in box_infos:
                box = re.findall(r"\((\d+),(\d+)\),\((\d+),(\d+)\)", box_info.get("box", ""))
                if box:
                    boxes.append(tuple(map(int, box[0])))
            save_xml_with_boxes(filepath, filename, width, height, boxes)
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.
# def simple_multimodal_conversation_call(image_path):
#     """Simple single round multimodal conversation call.
#     """
#     messages = [
#         {
#             "role": "user",
#             "content": [
#                 {"image": image_path},
#                 {"text": "帮我框图中的帽子"}
#             ]
#         }
#     ]
#     response = dashscope.MultiModalConversation.call(model=dashscope.MultiModalConversation.Models.qwen_vl_chat_v1,
#                                                      messages=messages)
    # # The response status_code is HTTPStatus.OK indicate success,
    # # otherwise indicate request is failed, you can get error code
    # # and message from code and message.
    # if response.status_code == HTTPStatus.OK:
    #     print(response)
    #     filepath = messages[0]["content"][0]["image"]
    #     filename = os.path.basename(filepath)
    #     print("图片路径：", filepath)
    #     print("图片文件名：", filename)
    #     image = cv2.imread(filepath)
    #     height, width = image.shape[:2]
    #     # 从模型输出中提取帽子位置信息
    #     box_infos = response["output"]["choices"][0]["message"]["content"]
    #     print("帽子位置信息：", box_infos)  # 调试输出帽子位置信息
    #     if box_infos is None:
    #         # 未检测到帽子，保存空的XML文件
    #         save_xml_with_boxes(filepath, filename, width, height, [])
    #     else:
    #         boxes = []
    #         for box_info in box_infos:
    #             box_text = re.search(r'<box>\((\d+),(\d+)\),\((\d+),(\d+)\)</box>', box_info).groups()
    #             if box_text:
    #                 box = tuple(map(int, box_text))
    #                 boxes.append(box)
    #         save_xml_with_boxes(filepath, filename, width, height, boxes)
    # else:
    #     print(response.code)  # The error code.
    #     print(response.message)  # The error message.

if __name__ == '__main__':
    # 要处理的文件夹路径
    folder_path = "/home/zhangting/yolov5-pytorch/data/resized_hat_baidu"
    # image_path = os.path.join(folder_path, '2943.jpg')
    # simple_multimodal_conversation_call(image_path)
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        print(file_name)
        if file_name.endswith(".jpg") or file_name.endswith(".png"):  # 只处理图片文件
            image_path = os.path.join(folder_path, file_name)
            simple_multimodal_conversation_call(image_path)