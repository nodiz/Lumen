# Lumen
Blind companion model created on the occasion of Lauzhack 2020 - Winner of the [SBB challenge](https://devpost.com/software/blinddetector)

✅ Check our detection result on unseen images [here](https://drive.google.com/drive/folders/1NkUUpMSchJwBPQ2dK0-cBXS6_qxHkIQo?usp=sharing)! ([YouTube video](https://www.youtube.com/watch?v=M2HeJXddtcc))

<img src="Blico-min.gif" alt="Blico-min" style="width: 640px;"/>

# Deep learning 

Our Deep model has been designed with the following object detector frameworks.


## Efficient det 
- Use 'sbb2coco.py' which adds some missing parts to the data (area, isCrowd, imageSize)
- Clone and configure Google repository (https://github.com/google/automl/tree/master/efficientdet)
- Produce the tfrecord chunks from the dataset as examplained in tutorial.ipynb
- Run training with main.py 
- Run inference with inspect.py
 
 
## Yolov5
 
Yolov5 is an interesting repository because of the autoresizing anchors, capable of detecting both small (like buttons) and big objects (like doors) precisely. 
 
### Train your model
 
- Use `sbb2yolo.py` which adapts the folder structure and the annotations (xmin,ymin,w,h) to normalized Yolo coordinates (xmid,ymid,w,h)
- `git clone https://github.com/ultralytics/yolov5.git`
- `cd yolov5/`
- `pip install -r requirements.txt`
- Create config.yaml
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
- Configure `wandb` for logging (it's awesome)
- Train mutilple model such as small for edge devices, large and xlarge for best performance 
- In our case we trained
```
 train.py --img-size 840 --batch 8 --epochs 20 --data config.yaml --weights yolov5x.pt
 train.py --img-size 420 --batch 32 --epochs 30 --data config.yaml --weights yolov5s.pt
 train.py --img-size 640 --batch 16 --epochs 20 --data config.yaml --weights yolov5l.pt
```
- Export the small model in jit version for android
- Evaluate the labels topping accuracy: combine the xlarge and large models (exp6 and exp10 in our case) and use tta (--augment) which further improve performances


```
python detect.py --source ../test/ --weights runs/train/exp6/weights/best.pt runs/train/exp10/weights/best.pt --save-txt --conf-thres 0.4 --save-conf --augment
```
 
Sources examples:

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

Sources examples

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

- Output will be saved into `runs/detect/exp[N]`
- Further postprocessing step is required to adpat labels to other format, check `convert_yolo_output.ipynb`

# The companion app (OBSOLETE, old prototype built fort Lauzhack 2020)

Built with Kotlin (the interface) and Java (the camera and classifier) on Android Studio.

- The interface is inspired from SBB's original app.

- The camera is pretty simple in the purpose of assuring the UI/UX fluidity.

- Implements the AI pytorch model yoloV5s that we trained for this use.
 

To implement the model please unzip the file from Blico/Interface SBB Blico with cam - test -2/app/src/main/assets/last.torchscript.pt.zip
