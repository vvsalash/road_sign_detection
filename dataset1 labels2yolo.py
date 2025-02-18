import os
import xml.etree.ElementTree as ET


ANNOTATIONS_DIR = "dataset1/annotations"   
OUTPUT_DIR = "dataset1/labels"  


CLASS_MAPPING = {
    "trafficlight": 0,
    "stop": 1,
    "speedlimit": 2
}


os.makedirs(OUTPUT_DIR, exist_ok=True)


for xml_file in os.listdir(ANNOTATIONS_DIR):
    if not xml_file.endswith(".xml"):
        continue
    
    tree = ET.parse(os.path.join(ANNOTATIONS_DIR, xml_file))
    root = tree.getroot()
    

    size = root.find("size")
    image_w = int(size.find("width").text)
    image_h = int(size.find("height").text)
    

    yolo_filename = os.path.join(OUTPUT_DIR, xml_file.replace(".xml", ".txt"))
    with open(yolo_filename, "w") as yolo_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in CLASS_MAPPING:
                continue
            class_id = CLASS_MAPPING[class_name]
            
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

print("Done")
