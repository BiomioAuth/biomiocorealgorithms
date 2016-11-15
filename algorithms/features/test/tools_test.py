from ..tools import minDistance, maxDistance, meanDistance, medianDistance
import cv2


def minDistance_test():
    matches = []
    for inx in range(0, 5, 1):
        match = cv2.DMatch()
        match.distance = 0.1 * inx
        matches.append([match])
    assert minDistance(matches) == 0.0


def maxDistance_test():
    matches = []
    for inx in range(0, 5, 1):
        match = cv2.DMatch()
        match.distance = 1.0 * inx
        matches.append([match])
    assert maxDistance(matches) == 4.0


def meanDistance_test():
    matches = []
    for inx in range(0, 5, 1):
        match = cv2.DMatch()
        match.distance = 1.0 * inx
        matches.append([match])
    assert meanDistance(matches) == 2.0


def medianDistance_test():
    matches = []
    for inx in range(0, 5, 1):
        match = cv2.DMatch()
        match.distance = 1.0 * inx
        matches.append([match])
    assert medianDistance(matches) == 2.0
