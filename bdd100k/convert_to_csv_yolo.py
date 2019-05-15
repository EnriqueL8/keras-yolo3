import json
import csv


label_train = "labels/bdd100k_labels_images_train.json"

do_not_include = ["lane", "drivable area", "train", "bus", "motor", "rider", "truck"]

path = "/scratch/el00244/bdd100k/images/100k/train/"

#dict = {u'bus': 1, u'traffic light': 2, u'traffic sign': 3, u'person': 4, u'bike': 5, u'truck': 6, u'motor': 7, u'car': 8, u'train': 9, u'rider': 10}

dict = {u'traffic light': 0, u'traffic sign': 1, u'person': 2, u'bike': 3, u'car': 4}
nDict = {u'traffic light': 0, u'traffic sign': 0, u'person': 0, u'bike': 0, u'car': 0}

f = open('labels/bdd100k_labels_images_train_yolo_format_float_only_5.txt', 'w')

with open(label_train) as json_file:
    data = json.load(json_file)
    for image in data:
        image_name = image["name"]
        f.write(path + image_name)
        for label in image["labels"]:
            category = label["category"]

            if category in do_not_include:
                continue

            class_id = dict[category]
            nDict[category] += 1

            box2d = label["box2d"]
            xmin = box2d["x1"]
            xmax = box2d["x2"]
            ymin = box2d["y1"]
            ymax = box2d["y2"]

            box_info = " %d,%d,%d,%d,%d" % (xmin, ymin, xmax, ymax, class_id)
            f.write(box_info)
        f.write('\n')

print(nDict)
f.close()
json_file.close()
