from ..matchers import MatcherCreator, FlannMatcher, BruteForceMatcher, defaultFlannBasedLSHIndexParams, \
    defaultFlannBasedKDTreeIndexParams, Matcher, LowesMatchingScheme, CrossMatching, SelfMatching, \
    SelfGraph, SubsetsCalculation
from ..defines import FLANN_INDEX_LSH, FLANN_INDEX_KDTREE
import random
import numpy
import cv2


def MatcherCreator_test():
    matcher = MatcherCreator('BruteForce-Hamming')
    assert matcher is not None


def FlannMatcher_test():
    matcher = FlannMatcher()
    assert matcher is not None


def BruteForceMatcher_test():
    matcher = BruteForceMatcher()
    assert matcher is not None
    assert isinstance(matcher, type(cv2.BFMatcher()))


def defaultFlannBasedLSHIndexParams_test():
    default_param = {'algorithm': FLANN_INDEX_LSH, 'table_number': 12, 'key_size': 20, 'multi_probe_level': 2}
    assert defaultFlannBasedLSHIndexParams() == default_param


def defaultFlannBasedKDTreeIndexParams_test():
    default_param = {'algorithm': FLANN_INDEX_KDTREE, 'trees': 5}
    assert defaultFlannBasedKDTreeIndexParams() == default_param


def Matcher_test():
    matcher = Matcher()
    assert matcher is not None
    assert isinstance(matcher, type(cv2.BFMatcher()))


def LowesMatchingScheme_test():
    match1 = cv2.DMatch()
    match1.distance = 100
    match2 = cv2.DMatch()
    match2.distance = 150
    match3 = cv2.DMatch()
    match3.distance = 300
    assert not LowesMatchingScheme(match1, match2)
    assert LowesMatchingScheme(match1, match3)


def CrossMatching_test():
    desc1 = numpy.asarray(numpy.random.rand(5, 64), numpy.float32)
    desc2 = numpy.asarray(numpy.random.rand(5, 64), numpy.float32)
    res = CrossMatching(desc1, desc2, FlannMatcher(), 3)
    assert res is not None
    assert isinstance(res[0], type(cv2.DMatch()))


def SelfMatching_test():
    desc1 = numpy.asarray(numpy.random.rand(5, 64), numpy.float32)
    res = SelfMatching(desc1, FlannMatcher(), numpy.float32, 3)
    assert res is not None
    for r in res:
        assert r is not None
        assert isinstance(r[0], numpy.ndarray)
        assert isinstance(r[1], numpy.ndarray)
        assert isinstance(r[2], float)


def SelfGraph_test():
    keypoints = []
    for inx in range(0, 5, 1):
        keypoints.append(cv2.KeyPoint(10 * random.random(), 10 * random.random(), 5 * random.random(),
                                      0, random.random()))
    res = SelfGraph(keypoints, 5)
    assert res is not None
    for r in res:
        assert isinstance(r[0], type(cv2.KeyPoint()))
        assert r[1] is None
        assert isinstance(r[2], type(cv2.KeyPoint()))
        assert r[3] is None
        assert isinstance(r[4], float)


def SubsetsCalculation_test():
    matches = []
    for inx in range(0, 5, 1):
        match = cv2.DMatch()
        match.distance = random.random()
        match.queryIdx = inx
        match.trainIdx = 5 - inx
        matches.append(match)
    res = SubsetsCalculation(matches)
    assert res is not None
    for r in res:
        assert isinstance(r, type(cv2.DMatch()))
