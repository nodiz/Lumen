#### yolo the labels

## need to split 80% train 20% val
## need to create new folders to match yolo structure
## need to adapt labels
## adapted from a jupyter notebook, people using this might need to hardcode some paths
## yaml writing need to manually fixed because german non-ascii characters in label names
## we provide a yaml to copy to the yolo folder in this directory

from random import random
import imagesize
import os.path as path
import yaml
import shutil

base = "export_coco/"  # path for sbb dataset
fname = path.join(base, "coco.json")  # coco.json path
j = json.load(open(fname))
print(j.keys())

p = 0.8

## build yaml  train: folder val: folder nc:4 classes: names

os.mkdir('dyolo')
os.mkdir('dyolo/images/')
os.mkdir('dyolo/labels/')
os.mkdir('dyolo/images/train')
os.mkdir('dyolo/images/val')
os.mkdir('dyolo/labels/train')
os.mkdir('dyolo/labels/val')


def yp(s):
    return path.join('dyolo', s)


# dump yaml
yam = {}
yam['train'] = '../dyolo/images/train'
yam['val'] = '../dyolo/val'
yam['nc'] = len(j['categories'])
names = [c['name'] for c in j['categories']]
yam['names'] = names
with open(yp('sbb.yaml'), 'w') as sbb:
    sbb.write(yaml.safe_dump(yam))

# build annotation dict
img_ann = {img['id']: [] for img in j['images']}
for ann in j['annotations']:
    img_ann[ann['image_id']].append(ann)

# process
for im in j['images']:
    im_anns = img_ann[im['id']]
    outFolder = 'train' if random() < p else 'val'
    shutil.copyfile(path.join('export_coco', im['file_name']),
                    path.join(yp(path.join('images', outFolder)), im['file_name']))
    with open(path.join(yp(path.join('labels', outFolder)), im['file_name'].split('.')[-2] + '.txt'), 'w') as gt:
        width, height = imagesize.get(path.join('export_coco', im['file_name']))
        for ann in img_ann[im['id']]:
            box = ann['bbox']
            yolo_bbox = box.copy()
            yolo_bbox[0] = box[0] + box[2] / 2
            yolo_bbox[1] = box[1] + box[3] / 2
            yolo_bbox[0] /= width
            yolo_bbox[2] /= width
            yolo_bbox[1] /= height
            yolo_bbox[3] /= height
            yolo_ann = [ann['category_id'] - 1]
            yolo_ann.extend(yolo_bbox)
            yolo_ann = [str(y) for y in yolo_ann]
            gt.write(" ".join(yolo_ann) + "\n")
