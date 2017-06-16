from ...algorithms.cascades.script_cascade_detector import ScriptCascadeDetector
from ...algorithms.cascades.tools import loadScript


SCRIPT_CASCADE_FACE_DETECTOR = "ScriptCascadeDetector::FaceDetection"
SCRIPT_CASCADE_FACE_DETECTOR_LOADED = "ScriptCascadeDetector::FaceDetection::preload_cascade"
DETECTION_SCRIPT = "main_haarcascade_face_size.json"


def create_cascade_detector(preloaded=False):
    return ScriptCascadeDetector(loadScript(DETECTION_SCRIPT, True), preloaded)
