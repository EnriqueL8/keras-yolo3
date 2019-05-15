import json
import csv


label_train = "labels/bdd100k_labels_images_train.json"

do_not_include = ["lane", "drivable area"]

dict = {u'bus': 1, u'traffic light': 2, u'traffic sign': 3, u'person': 4, u'bike': 5, u'truck': 6, u'motor': 7, u'car': 8, u'train': 9, u'rider': 10}

rows = []

with open(label_train) as json_file:
    data = json.load(json_file)
    for image in data:
        image_name = image["name"]
        for label in image["labels"]:
            category = label["category"]

            if category in do_not_include:
                continue

            class_id = dict[category]

            box2d = label["box2d"]
            xmin = box2d["x1"]
            xmax = box2d["x2"]
            ymin = box2d["y1"]
            ymax = box2d["y2"]

            row = [image_name, xmin, xmax, ymin, ymax, class_id]
            rows.append(row)

json_file.close()

label_train_csv = "labels/bdd100k_labels_images_train.csv"

with open(label_train_csv, 'w') as csv_file:
    writer = csv.writer(csv_file)
    for row in rows:
        writer.writerow(row)

csv_file.close()
