import os

LABELS_DIR = "dataset2/labels"


CLASS_MAPPING = {
    0: 0,  # trafficlight
    1: 0, 
    2: 2,  # speedlimit
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 2,
    13: 2,
    14: 1 # stop

}


for filename in os.listdir(LABELS_DIR):
    if not filename.endswith(".txt"):
        continue
    
    file_path = os.path.join(LABELS_DIR, filename)
    
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        
        class_id = int(parts[0])
        if class_id in CLASS_MAPPING:
            parts[0] = str(CLASS_MAPPING[class_id])
        
        new_lines.append(" ".join(parts))
    
    with open(file_path, "w") as file:
        file.write("\n".join(new_lines) + "\n")

print("Done")