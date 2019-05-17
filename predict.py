import sys
import collections
import os
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import glob
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.8f')

def detect_img(yolo, img):
    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
    
    predictions = yolo.get_predictions(image)
    return predictions

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--folder', type=str,
        help='path to folder containing the test images file, default ' + ""
    )

    parser.add_argument(
        '--output_file', type=str,
        help='path to output predictions json, default ' + ""
    )

    parser.add_argument(
        '--dataset', type=str,
        help='Dataset used only support bdd100K or kitti, default ' + "bdd100k"
    )

    FLAGS = parser.parse_args()

    kitti_classes = ['car', 'person', 'bike']
    if FLAGS.folder is None:
        print("Must specify path to folder containing the test images file.  See usage with --help.")
    elif FLAGS.output_file is None:
        print("Must specify path to output predictions json. See usage with --help.")
    elif FLAGS.folder and FLAGS.output_file:
        print("Evaluating Model")
        yolo = YOLO(**vars(FLAGS))

        predictions = []
        counter = 0

        images = glob.glob(FLAGS.folder + '*.jpg')
        for filename in images:
            counter += 1
            print("Processed image: ", counter, "of", len(images))
            image_predictions = detect_img(yolo, filename)
            head, tail = os.path.split(filename)            
            for predicted_class, box, score in image_predictions:
                d = collections.OrderedDict()
                d["name"] = tail
                d["timestamp"] = 10000
                d["category"] = predicted_class
                if FLAGS.dataset is 'kitti' and predicted_class not in kitti_classes:
                    continue
                d["bbox"] = [float(box[1]), float(box[0]), float(box[3]), float(box[2])]
                d["score"] = float(score)
                predictions.append(d)
        yolo.close_session()

        with open(FLAGS.output_file, 'w') as outfile:
            json.dump(predictions, outfile, indent=2)
    