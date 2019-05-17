import json
import csv
import sys

label_type=sys.argv[1]
label_file = ""
path = ""
output_file = ""
if label_type is "train":
    label_file = "labels/bdd100k_labels_images_train.json"
    path = "bdd100k/images/100k/train/"
    output_file = "labels/bdd100k_labels_images_train_yolo_format.txt"
elif label_type is "val":
    label_file = "labels/bdd100k_labels_images_val.json"
    path = "bdd100k/images/100k/val/"
    output_file = "labels/bdd100k_labels_images_val_yolo_format.txt"
else:
    print("Please specifiy a label type either train or val!")

# We do not want to include lane and drivable area information
do_not_include = ["lane", "drivable area"]

# Map the object class to a label id
classToId = {u'bus': 1, u'traffic light': 2, u'traffic sign': 3, u'person': 4, u'bike': 5, u'truck': 6, u'motor': 7, u'car': 8, u'train': 9, u'rider': 10}

with open(label_file) as json_file, open(output_file, 'w') as f:
    data = json.load(json_file)
    for image in data:
        image_name = image["name"]
        f.write(path + image_name)
        for label in image["labels"]:
            category = label["category"]

            if category in do_not_include:
                continue

            class_id = classToId[category]
            box2d = label["box2d"]
            xmin = box2d["x1"]
            xmax = box2d["x2"]
            ymin = box2d["y1"]
            ymax = box2d["y2"]

            box_info = " %d,%d,%d,%d,%d" % (xmin, ymin, xmax, ymax, class_id)
            f.write(box_info)
        f.write('\n')