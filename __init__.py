PARALLEL_USAGE = "PARALLEL_USAGE"
SEQUENTIAL_USAGE = "SEQUENTIAL_USAGE"

CURRENT_USAGE = PARALLEL_USAGE


def is_parallel():
    return CURRENT_USAGE == PARALLEL_USAGE


import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
OPENFACE_NN4_MODEL_PATH = os.path.join(scriptDir, "data", "nn4.small2.v1.t7")
OPENFACE_AMF_MODEL_PATH = os.path.join(scriptDir, "data", "94.9-accuracy-model-float.t7")
DLIB_MODEL_PATH = os.path.join(scriptDir, "data", "shape_predictor_68_face_landmarks.dat")

OPENFACE_IMAGE_DIMENSION = 96
