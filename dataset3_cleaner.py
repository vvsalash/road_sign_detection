import os
import random
from glob import glob


dataset_root = "bdd100k/dataset"
labels_root = "bdd100k/labels"
KEEP_RATIO = 0.1


def reduce_dataset(split):
    images_dir = os.path.join(dataset_root, split)
    labels_dir = os.path.join(labels_root, split)

    all_images = sorted(glob(f"{images_dir}/*.jpg"))
    all_labels = sorted(glob(f"{labels_dir}/*.txt"))

    num_keep = int(len(all_images) * KEEP_RATIO)

    keep_images = set(random.sample(all_images, num_keep))
    keep_image_names = {os.path.basename(img).replace(".jpg", ".txt") for img in keep_images}

    images_to_delete = [img for img in all_images if img not in keep_images]
    labels_to_delete = [lbl for lbl in all_labels if os.path.basename(lbl) not in keep_image_names]

    for img in images_to_delete:
        os.remove(img)

    for lbl in labels_to_delete:
        os.remove(lbl)

    print(f"[{split}] Оставлено: {num_keep} изображений, удалено: {len(images_to_delete)} изображений и {len(labels_to_delete)} аннотаций")

for split in ["train", "val"]:
    reduce_dataset(split)
