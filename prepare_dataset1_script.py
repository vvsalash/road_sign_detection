import kagglehub
import shutil
import os
import xml.etree.ElementTree as ET


path = kagglehub.dataset_download("andrewmvd/road-sign-detection")
custom_path = "dataset1"
os.makedirs(custom_path, exist_ok=True)

for file_name in os.listdir(path):
    shutil.move(os.path.join(path, file_name), os.path.join(custom_path, file_name))

print("Dataset downloaded successfully")


ANNOTATIONS_DIR = "dataset1/annotations"

CLASSES = {
    "trafficlight": 0,
    "stop": 1,
    "speedlimit": 2,
    "crosswalk": 3
}

for xml_file in os.listdir(ANNOTATIONS_DIR):
    if not xml_file.endswith(".xml"):
        continue
    
    xml_path = os.path.join(ANNOTATIONS_DIR, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size = root.find("size")
    image_w = int(size.find("width").text)
    image_h = int(size.find("height").text)
    
    txt_path = os.path.join(ANNOTATIONS_DIR, xml_file.replace(".xml", ".txt"))
    with open(txt_path, "w") as yolo_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in CLASSES:
                continue
            class_id = CLASSES[class_name]
            
            bbox = obj.find("bndbox")
            x_min = int(bbox.find("xmin").text)
            y_min = int(bbox.find("ymin").text)
            x_max = int(bbox.find("xmax").text)
            y_max = int(bbox.find("ymax").text)
            
            x_center = (x_min + x_max) / 2.0 / image_w
            y_center = (y_min + y_max) / 2.0 / image_h
            width = (x_max - x_min) / image_w
            height = (y_max - y_min) / image_h
            
            yolo_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    os.remove(xml_path)

print("Annotations converted to YOLOv8 format")
