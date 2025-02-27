import kagglehub
import shutil
import os

path = kagglehub.dataset_download("pkdarabi/cardetection")
custom_path = "dataset2"
os.makedirs(custom_path, exist_ok=True)

for file_name in os.listdir(path):
    shutil.move(os.path.join(path, file_name), os.path.join(custom_path, file_name))



required_folders = {"train", "valid", "test"}
for item in os.listdir(custom_path):
    item_path = os.path.join(custom_path, item)
    
    if item == "car" and os.path.isdir(item_path):
        for subfolder in os.listdir(item_path):
            subfolder_path = os.path.join(item_path, subfolder)
            if subfolder in required_folders and os.path.isdir(subfolder_path):
                shutil.move(subfolder_path, custom_path)
        shutil.rmtree(item_path, ignore_errors=True)
    
    elif item not in required_folders:
        item_path = os.path.join(custom_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path, ignore_errors=True)
        else:
            os.remove(item_path)

print("Dataset downloaded successfully")