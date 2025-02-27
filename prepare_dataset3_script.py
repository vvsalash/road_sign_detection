import os
import json
from glob import glob
import random

annotations = {
    "train": "bdd100k_labels_release/bdd100k/labels/bdd100k_labels_images_train.json",
    "val": "bdd100k_labels_release/bdd100k/labels/bdd100k_labels_images_val.json",
}

dataset_root = "bdd100k/dataset"
labels_root = "bdd100k/labels"

CLASSES = [
    "pedestrian", "rider", "car", "truck", "bus", "train",
    "motorcycle", "bicycle", "traffic light", "traffic sign"
]

TRAFFIC_SIGN_CLASS_ID = CLASSES.index("traffic sign")

IMG_WIDTH, IMG_HEIGHT = 1280, 720

os.makedirs(labels_root, exist_ok=True)

for split, json_path in annotations.items():
    images_dir = os.path.join(dataset_root, split)
    labels_dir = os.path.join(labels_root, split)
    os.makedirs(labels_dir, exist_ok=True)

    with open(json_path, "r") as f:
        data = json.load(f)

    all_images = {os.path.basename(p): p for p in glob(f"{images_dir}/*.jpg", recursive=True)}
    images_without_sign = []

    print(f"Обработка данных для {split} ...")

    for image_data in data:
        image_name = image_data["name"]

        if image_name not in all_images:
            print(f"Изображение {image_name} не найдено в папке {images_dir}")
            continue

        label_path = os.path.join(labels_dir, image_name.replace(".jpg", ".txt"))

        labels = []
        for obj in image_data["labels"]:
            if obj["category"] != "traffic sign":
                continue

            x1, y1, x2, y2 = obj["box2d"]["x1"], obj["box2d"]["y1"], obj["box2d"]["x2"], obj["box2d"]["y2"]
            x_center = ((x1 + x2) / 2) / IMG_WIDTH
            y_center = ((y1 + y2) / 2) / IMG_HEIGHT
            width = (x2 - x1) / IMG_WIDTH
            height = (y2 - y1) / IMG_HEIGHT

            labels.append(f"{TRAFFIC_SIGN_CLASS_ID} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        if not labels:
            images_without_sign.append(image_name)
            with open(label_path, "w") as f:
                f.write("")
        else:
            with open(label_path, "w") as f:
                f.write("\n".join(labels))

    images_with_sign = len([image for image in all_images.keys() if image not in images_without_sign])
    images_to_remove = len(images_without_sign) - images_with_sign

    images_to_delete = []
    if images_to_remove > 0:
        images_to_delete = random.sample(images_without_sign, images_to_remove)

        for image in images_to_delete:
            image_path = os.path.join(images_dir, image)
            os.remove(image_path)
            images_without_sign.remove(image)

    print(f"Удалено изображений без знаков: {len(images_to_delete)}")

images_to_delete = []

for split in ["train", "val"]:
    images_dir = os.path.join(dataset_root, split)
    labels_dir = os.path.join(labels_root, split)

    all_images = {os.path.basename(p): p for p in glob(f"{images_dir}/*.jpg", recursive=True)}
    all_labels = {os.path.basename(p): p for p in glob(f"{labels_dir}/*.txt", recursive=True)}

    for image_name in all_images:
        label_name = image_name.replace(".jpg", ".txt")
        if label_name not in all_labels:
            image_path = os.path.join(images_dir, image_name)
            images_to_delete.append(image_path)
            print(f"Удаляем изображение: {image_path}")

for image_path in images_to_delete:
    os.remove(image_path)

print(f"Удалено {len(images_to_delete)} изображений.")
