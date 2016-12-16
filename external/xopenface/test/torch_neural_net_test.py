from ..torch_neural_net import TorchNeuralNet
import cv2
import os


scriptDir = os.path.dirname(os.path.realpath(__file__))
TEST_IMAGE_PATH = os.path.join(scriptDir, "test_data", "DI0101.png")
OPENFACE_MODEL_PATH = os.path.join(scriptDir, "..", "..", "..", "data", "nn4.small2.v1.t7")
OPENFACE_IMGDIM = 96


def torch_neural_net_test():
    assert os.path.exists(TEST_IMAGE_PATH), "Test image doesn't found."
    assert os.path.exists(OPENFACE_MODEL_PATH), "Test OpenFace pre-trained model doesn't found."
    net = TorchNeuralNet(model=OPENFACE_MODEL_PATH, imgDim=OPENFACE_IMGDIM)
    img = cv2.imread(TEST_IMAGE_PATH)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rep = net.forward(img)
    assert rep is not None and rep.shape == (128,)
