import json

label_train = "labels/bdd100k_labels_images_train.json"

do_not_include = ["lane", "drivable area"]
dict = {}

with open(label_train) as json_file:
    data = json.load(json_file)
    for image in data:
        for label in image["labels"]:
	    category = label["category"]

	    if category in do_not_include:
		continue

	    if category not in dict:
	        dict[category] = 1
	    else:
		dict[category] += 1

    print("Classes: ", dict)
    print("Number of Classes: ", len(dict))
