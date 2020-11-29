## annotations converter to obtain json compatible with tensorflow automl/efficientdet
## adapted from a jupyter notebook

## need to split 80% train 20% val
## need to add height and width to images, area and isCrowd to annotations

import json
from random import random
import imagesize
import os.path as path

base = "export_coco/"  # path for sbb dataset
fname = path.join(base, "coco.json")  # coco.json path
j = json.load(open(fname))
print(j.keys())

j_train = {}
j_val = {}
p = 0.8  # train/all ratio

## prepare new jsons
cloneable = ['info', 'licenses', 'categories']
not_cloneable = ['images', 'annotations']

for c in cloneable:
    j_train[c] = j[c]
    j_val[c] = j[c]
for c in not_cloneable:
    j_train[c] = []
    j_val[c] = []

## build annotation dict
img_ann = {img['id']: [] for img in j['images']}
for ann in j['annotations']:
    ann['iscrowd'] = False
    ann['area'] = ann['bbox'][2] * ann['bbox'][3]
    img_ann[ann['image_id']].append(ann)

for im in j['images']:
    if random() < p:
        j_train['images'].append(im)
        j_train['annotations'].extend([ann for ann in img_ann[im['id']]])
        width, height = imagesize.get(path.join('export_coco', im['file_name']))  # this should be 10x
        j_train['images'][-1]['width'] = width
        j_train['images'][-1]['height'] = height
    
    else:
        j_val['images'].append(im)
        j_val['annotations'].extend([ann for ann in img_ann[im['id']]])
        width, height = imagesize.get(path.join('export_coco', im['file_name']))  # this should be 10x
        j_val['images'][-1]['width'] = width
        j_val['images'][-1]['height'] = height

## write to file

with open(path.join(path.join(base, 'train.json')), 'w') as f:
    json.dump(j_train, f)
with open(path.join(path.join(base, 'val.json')), 'w') as f:
    json.dump(j_val, f)

## Finally check everything is alright

print(len(j_train['images']))
print(len(j_val['images']))

print(j['images'][0])
print(j_train['images'][0])
print(j_val['images'][0])

print(j['annotations'][0])
print(j_train['annotations'][0])
print(j_val['annotations'][0])
