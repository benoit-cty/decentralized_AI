#!/usr/bin/python3
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import urllib.request

# Force no GPU
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco

#%matplotlib inline

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


# Start by reading file : no need to continue if input are incorrect
if len(sys.argv) > 1:
    print("# Load image from url in command line")
    #input_file = "/iexec/input.img"
    #urllib.request.urlretrieve(str(sys.argv[1]), input_file)
    input_file, headers = urllib.request.urlretrieve(str(sys.argv[1]))
else:
    print("# ERROR : You need to provide an image URL as a parameter !")
    quit(-1)

image = skimage.io.imread(os.path.join(IMAGE_DIR, input_file))


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
#config.display()

print("# Create model object in inference mode.")
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

print("# Load weights trained on MS-COCO")
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

print("# Run detection")
results = model.detect([image], verbose=1)

print("Visualize results")
r = results[0]

visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                class_names, r['scores'])
output_file = "{}/{}.png".format("/iexec", datetime.now().strftime('%Y%m%d_%H%M%S'))
print("Save results to ", output_file)
plt.savefig(output_file, bbox_inches='tight', pad_inches='-0.1')
print('# Save /iexec/consensus.iexec for the PoCo verification')
consensus_file = "/iexec/consensus.iexec"
boxes = r['rois']
masks = r['masks']
class_ids = r['class_ids']
consensus = ""
N = r['rois'].shape[0]
for i in range(N):
        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox
            continue
        y1, x1, y2, x2 = boxes[i]
        rectangle = "  Box = " + x1 +"x"+ y1 + " " + x2 + "x" + y2 

        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            x = random.randint(x1, (x1 + x2) // 2)
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        consensus += caption + rectangle


print("r['masks']:", r['masks'])
print("r['scores']:", r['scores'])
print("r['rois']:", r['rois'])
print("r['class_ids']:", r['class_ids'])
print(consensus)
with open(consensus_file, 'w') as fp:
	fp.write(consensus)
	fp.close()
