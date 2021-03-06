from __future__ import print_function
from keras.models import load_model
import cv2
import numpy as np
import os
import time
from PTIT_model import build_ptit
labels = ['background','road','traffic','car']
lr_init = 1e-4
lr_decay = 5e-4
vgg_path = None
model = build_ptit((256, 320, 3), num_classes=len(labels),
                lr_init=lr_init, lr_decay=lr_decay)

model.load_weights('/home/vicker/Downloads/pitmodel-034-0.48831.hdf5')

def result_map_to_img(res_map):
    img = np.zeros((256, 320, 3), dtype=np.uint8)
    res_map = np.squeeze(res_map)

    argmax_idx = np.argmax(res_map, axis=2)

    # For np.where calculation.
    road = (argmax_idx == 1)
    car = (argmax_idx == 2)
    traffic = (argmax_idx == 3)

    img[:, :, 0] = np.where(road, 255, 0)
    img[:, :, 1] = np.where(car, 255, 0)
    img[:, :, 2] = np.where(traffic, 255, 0)

    return img

def visualize(img):
    img = cv2.resize(img,(320,256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, 0)
    img = img / 127.5 - 1

    pred = model.predict(img)
    print(pred.shape)
    res_img = result_map_to_img(pred[0])
    #import ipdb; ipdb.set_trace()
    #out_final = output_path + path[3:-9]
    return res_img
    #cv2.imwrite(os.path.join(out_final + '/27.10/', self.model_name + '_epoch_' + str(self.epoch) + '.png'), res_img)
img = cv2.imread('/home/vicker/Downloads/all_rgb_simulator/sim1_33.jpg')
res = visualize(img)
cv2.imwrite('/home/vicker/Desktop/trash.png',res)