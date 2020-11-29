# Blico
Blind companion for Lauzhack 2020 - SBB challenge

✅ Check our detection result on unseen images here!
https://drive.google.com/drive/folders/1NkUUpMSchJwBPQ2dK0-cBXS6_qxHkIQo?usp=sharing

# Deep learning 

## Efficient det 
-use 'sbb2coco.py' which add some missing parts to the data (area, isCrowd, imageSize)
- clone and configure Google repository  (https://github.com/google/automl/tree/master/efficientdet)
- produce the tfrecord chunks from the dataset as examplained in tutorial.ipynb
- run training with main.py 
- run inference with inspect.py
 
 
 ## Yolov5
 
 Very good repo because of the autoresizing anchors, capable of detect both small and big objects precisely.
 
- use `sbb2yolo.py` which adapt the folder structure and the annotations (xmin,ymin,w,h) to normalized Yolo coordinates (xmid,ymid,w,h)
- `git clone https://github.com/ultralytics/yolov5.git`
- `cd yolov5/`
- `pip install -r requirements.txt`
- create config.yaml
```
names:
- "Door button"
- "Open door"
- "Door handle"
- "Door"
nc: 4
train: ../dyolo/images/train
val: ../dyolo/images/val
```
- configure `wandb` for logging (it's awesome)
- train mutilple model such as small for edge devices, large and xlarge for best performance 
- in our case we trained
```
train.py --img-size 840 --batch 8 --epochs 20 --data config.yaml --weights yolov5x.pt
train.py --img-size 420 --batch 32 --epochs 30 --data config.yaml --weights yolov5s.pt
train.py --img-size 640 --batch 16 --epochs 20 --data config.yaml --weights yolov5l.pt
```
- export the small model in jit version for android
- evaluate the labels topping accuracy: combine the xlarge and large models (exp6 and exp10 in our case) and use tta (--augment) which further improve performances


```
python detect.py --source ../test/ --weights runs/train/exp6/weights/best.pt runs/train/exp10/weights/best.pt --save-txt --conf-thres 0.4 --save-conf --augment
 ```
 
 examples of sources

```
 0  # webcam
 file.jpg  # image 
 file.mp4  # video
 path/  # directory
 path/*.jpg  # glob
 rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa  # rtsp stream
 rtmp://192.168.1.105/live/test  # rtmp stream
 http://112.50.243.8/PLTV/88888888/224/3221225900/1.m3u8  # http stream
```

## Inference with our pretrained weights

- `git clone https://github.com/ultralytics/yolov5.git`
- `cd yolov5/`
- `pip install -r requirements.txt`
- `wget -P pretrained https://objectstorage.uk-london-1.oraclecloud.com/n/orasealps/b/LauzHack2020-noid/o/yolov5l.pt`
- `wget -P pretrained https://objectstorage.uk-london-1.oraclecloud.com/n/orasealps/b/LauzHack2020-noid/o/yolov5x.pt`
- `python detect.py --source ../test/ --weights pretrained/yolov5l.pt pretrained/yolov5x.pt --save-txt --conf-thres 0.4 --save-conf --augment`

examples of sources

```
 0  # webcam
 file.jpg  # image 
 file.mp4  # video
 path/  # directory
 path/*.jpg  # glob
 rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa  # rtsp stream
 rtmp://192.168.1.105/live/test  # rtmp stream
 http://112.50.243.8/PLTV/88888888/224/3221225900/1.m3u8  # http stream
```

- output will be saved into runs/detect/exp[N]
- further postprocessing step is required to adpat labels to other format, check convert_yolo_output.ipynb

# The companion app

Built with Kotlin (the interface) and Java (the camera and classifier) on Android Studio.

- The interface is inspired from SBB's original app, after all this project has the goal of being implemented in their work.

![Alt text](doc/6ce3fc45-46a5-445a-909a-6615519a606d.jpg)

- The camera is pretty simple in the purpose of assuring the UI/UX fluidity. 

![Alt text](doc/669277df-1148-4d87-b28b-d1a834641fcd.jpg)
Note : This photo is only to show the camera's UI. We tested the pytorch cam on another predective model before impleminting the SBB train, thus the photo.

Implements the AI pytorch model yoloV5s that we trained for this use.

![Alt text](doc/screen.PNG)

To implement the model please unzip the file from Blico/Interface SBB Blico with cam - test -2/app/src/main/assets/last.torchscript.pt.zip

