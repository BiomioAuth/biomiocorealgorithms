from ..general.base import IAlgorithm
from ...logger import logger
import time
import cv2


class ResizeImageAlgorithm(IAlgorithm):
    """
    Settings:
    {
        'imgDim': image dimension
    }
    Input:
    {
        'img': numpy.ndarray of the image file,
        'path': abstract path to the image file
    }
    Output:
    {
        'img': numpy.ndarray of the image file
    }
    """
    def __init__(self, settings):
        self._imgDim = settings.get('imgDim', 96)
        self._error_handler = settings.get('error_handler', None)

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("ResizeImageAlgorithm::apply")
        logger.debug(data)
        logger.debug("===================================")
        start = time.time()
        img = data.get('img')
        if img is not None:
            if self._imgDim is not None and self._imgDim > 0:
                img = cv2.resize(img, (self._imgDim, self._imgDim), interpolation=cv2.INTER_LANCZOS4)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            return self._process_error(data, "Unable to resize an image: {}".format(data.get('path')))
        logger.debug("Image resizing for {} took {} seconds.".format(data.get('path'), time.time() - start))
        data.update({'img': img})
        return data

    def _process_error(self, data, message):
        if self._error_handler is not None:
            self._error_handler({
                'path': data['path'],
                'message': message
            })
        data.update({'img': None})
        return data
