

import time

start = time.time()

import argparse
import cv2
import itertools
import os

import numpy as np
np.set_printoptions(precision=2)

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

parser = argparse.ArgumentParser()

parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()

if args.verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
if args.verbose:
    print("Loading the dlib and OpenFace models took {} seconds.".format(
        time.time() - start))





import scipy.spatial.distance as distance
train_set = []
test_set = []
start = time.time()
for inx, img in enumerate(args.imgs):
    use_set = train_set if inx < 10 else test_set
    use_set.append({'image': img, 'rep': getRep(img)})
print("Total time: {} seconds.".format(time.time() - start))
res = [[c / 100.0, 0] for c in range(0, 101, 10)]
for item in test_set:
    avg = 0
    for data in train_set:
        avg += distance.euclidean(data['rep'], item['rep'])
    avg /= len(train_set)
    print("Verification {}: {}".format(item['image'], avg))
    if res[len(res) - 1][0] <= avg:
        res[len(res) - 1][1] += 1
    else:
        for pair in res:
            if pair[0] + 0.10 > avg:
                pair[1] += 1
                break
print "------------------------------------------------------------"
print(len(test_set))
print "distance\tcount\tprobability"
for inx, pair in enumerate(res):
    dist_str = str(pair[0])
    if inx == len(res) - 1:
        dist_str += ">"
    else:
        dist_str += "-" + str(pair[0] + 0.10)
    print(dist_str + "\t" + str(pair[1]) + "\t" + str(pair[1] / (1.0 * len(test_set))))
