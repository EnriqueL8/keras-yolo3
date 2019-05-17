# keras-yolo3 for Berkeley Deep Drive 100K

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

## Introduction
This is an adaptation  a Keras implementation of YOLOv3 (Tensorflow backend) from  https://github.com/qqwweee/keras-yolo3 to train on Berkeley Deep Drive 100K dataset.

---

## Quick Start

You can run interference with our trained models as such:
```
python yolo_video.py [OPTIONS...] --image, for image detection mode, OR
python yolo_video.py [video_path] [output_path (optional)]
```

The trained model to be used is set in `yolo.py`. You can change the model in that file or pass it as an argument `--model` to `yolo_video.py`.

You can find the models trained in the `logs` folder

### Usage
Use --help to see usage of yolo_video.py:
```
usage: yolo_video.py [-h] [--model MODEL] [--anchors ANCHORS]
                     [--classes CLASSES] [--gpu_num GPU_NUM] [--image]
                     [--input] [--output]

positional arguments:
  --input        Video input path
  --output       Video output path

optional arguments:
  -h, --help         show this help message and exit
  --model MODEL      path to model weight file, default model_data/yolo.h5
  --anchors ANCHORS  path to anchor definitions, default
                     model_data/yolo_anchors.txt
  --classes CLASSES  path to class definitions, default
                     model_data/coco_classes.txt
  --gpu_num GPU_NUM  Number of GPU to use, default 1
  --image            Image detection mode, will ignore all positional arguments
```
---

MultiGPU usage: use `--gpu_num N` to use N GPUs. It is passed to the [Keras multi_gpu_model()](https://keras.io/utils/#multi_gpu_model).

## Training
We have choosen to train on the [Berkeley Deep Drive Dataset](https://bdd-data.berkeley.edu/) where you will need to sign up and download the 100K images. You will also need to download the labels and unzip them


1. Make sure you install the required packages. This project uses Python 3.5.2.

We suggest you create a virtual environment as such:
```[bash]
    virtualenv env
    source env/bin/activate
    pip3 install -r requirements.txt
```


We have written some scripts to convert the BDD100K labels into the YOLO labels. 

2. Make sure the unzip labels are stored in the folder `bdd100k/labels` and the images in `bdd100k/images/`, then run:
```[python]
    # To convert the train labels
    python convert_to_csv_yolo.py train

    # To convert the validation labels
    python convert_to_csv_yolo.py val
```



3. Modify train.py by changing the input image size, learning rate and location of training and validation labels. The classes path and anchors path has been set.
   
   To start training run: 
    `python train.py`

    Use your trained weights or checkpoint weights with command line option `--model model_file` when using yolo_video.py
    Remember to modify class path or anchor path, with `--classes class_file` and `--anchors anchor_file`.

If you want to use original pretrained weights for YOLOv3:  
    1. `wget https://pjreddie.com/media/files/darknet53.conv.74`  
    2. rename it as darknet53.weights  
    3. `python convert.py -w darknet53.cfg darknet53.weights model_data/darknet53_weights.h5`  
    4. use model_data/darknet53_weights.h5 in train.py

4. To visualise the testing and validation loss run tensorboard in the logs diretory as such:
 ```
 # From the keras-yolo3 folder
 tensorboard --logdir=logs/
 ``` 
 This will open the tensorboard and load all the training data for all the models trained.
 In the case where you only want the information for one model run:
 ```
 # From the keras-yolo3 folder 
 tensorboard --logdir=logs/<model-directory-here>/
 ```
---

## Evaluation
For the purpose of evaluation, we split the training dataset into a 90% training subset and 10% validation subset and use the original validation set as our local testing set.

To create a json with our model predictions against the validation set we run: 
```
python predict.py --folder <PATH-TO-TEST-IMAGE> --output_file bdd100k/predictions_validation.json
```
In this case the `<PATH-TO-TEST-IMAGE>`, is `bdd100k/images/100k/val/`.

For evaluation we use the [bdd-data](https://github.com/ucbdrive/bdd-data) github repository.
Clone this into the main folder. 

We convert the ground-truth labels to the evaluation format by running:

```
    python bdd_data/label2det.py bdd100k/labels/bdd100k_labels_images_validation.json \
    bdd100k/detection_validation.json
```

To evaluate the predictionss of our model agains the validation set, we run:
```
    python bdd_data/evaluate.py  --task det --gt bdd100k/detection_validation.json \ 
    --result bdd100k/predictions_validation.json
```

---
## Some issues to know

1. The test environment is
    - Python 3.5.2
    - Keras 2.1.5
    - tensorflow 1.6.0

2. Default anchors are used. If you use your own anchors, probably some changes are needed.

3. The inference result is not totally the same as Darknet but the difference is small.

4. The speed is slower than Darknet. Replacing PIL with opencv may help a little.

5. Always load pretrained weights and freeze layers in the first stage of training. Or try Darknet training. It's OK if there is a mismatch warning.

6. The training strategy is for reference only. Adjust it according to your dataset and your goal. And add further strategy if needed.

7. For speeding up the training process with frozen layers train_bottleneck.py can be used. It will compute the bottleneck features of the frozen model first and then only trains the last layers. This makes training on CPU possible in a reasonable time. See [this](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html) for more information on bottleneck features.
