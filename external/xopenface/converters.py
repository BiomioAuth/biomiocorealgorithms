import numpy as np
import cv2


def toNumpyArray(tensor, dtype=np.float32):
    """
    Convert Torch tensor to numpy.ndarray of dtype type.

    :param tensor: Torch Tensor
    :param dtype: numpy.dtype
    :return: numpy.ndarray
    """
    return tensor.asNumpyArray().astype(dtype)


def toCVShape(img, fromTensor=False):
    """
    Convert shape of the input img from Torch shape (channel, width, height)
    to OpenCV Image shape (width, height, channel). If fromTensor is True,
    img converts from Torch tensor to numpy.ndarray and then converted its
    shape.

    :param img: Torch Tensor or numpy.ndarray
    :param fromTensor: bool
    :return: numpy.ndarray
    """
    np_img = img
    if fromTensor:
        np_img = toNumpyArray(img)
    sh = np_img.shape
    resImg = np.ndarray(shape=(sh[1], sh[2], sh[0]), dtype=np.float32)
    resImg.fill(0)
    for inx in range(0, sh[0], 1):
        resImg[:, :, inx] = np_img[inx, :, :]
    return resImg


def toCV2Image(torch_img, fromTensor=False):
    """
    Convert from Torch.image (in tensor or numpy.ndarray formats)
    to OpenCV numpy.ndarray Image format.
    Conversion:
        Torch.image                  -> OpenCV Image
        [                            -> [
         channel{R, G, B}[0..1],     ->  width,
         width,                      ->  height,
         height                      ->  channel{B, G, R}[0..255]
        ]                            -> ]

    :param torch_img: Torch Tensor or numpy.ndarray
    :param fromTensor: bool
    :return: numpy.ndarray
    """
    cv_shape = toCVShape(torch_img, fromTensor)
    return cv2.cvtColor(np.array(cv_shape * 255, dtype=np.uint8), cv2.COLOR_RGB2BGR)


def toTorchShape(img):
    """
    Convert shape of the input img from OpenCV Image shape (width, height, channel)
    to Torch shape (channel, width, height).

    :param img: numpy.ndarray
    :return: numpy.ndarray
    """
    sh = img.shape
    resImg = np.ndarray(shape=(sh[2], sh[0], sh[1]), dtype=np.float64)
    resImg.fill(0)
    for inx in range(0, sh[2], 1):
        resImg[inx, :, :] = img[:, :, inx]
    return resImg


def toTorchImage(cv_rgb_img):
    """
    Convert from OpenCV numpy.ndarray Image format to
    Torch.image (in numpy.ndarray format).
    Conversion:
        OpenCV Image                 -> Torch.image
        [                            -> [
         width,                      ->  channel{R, G, B}[0..1],
         height,                     ->  width,
         channel{B, G, R}[0..255]    ->  height
        ]                            -> ]
    :param cv_rgb_img: numpy.ndarray
    :return: numpy.ndarray
    """
    n_img = np.array(cv_rgb_img, dtype=np.float64) / 255.0
    return toTorchShape(n_img)
