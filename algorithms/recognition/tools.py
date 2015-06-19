import itertools

def minDistance(matches):
    return min(itertools.chain(*matches), key=lambda p: p.distance).distance


def maxDistance(matches):
    return max(itertools.chain(*matches), key=lambda p: p.distance).distance


def meanDistance(matches):
    dist = [m.distance for m in itertools.chain(*matches)]
    return sum(dist) / len(dist)


def medianDistance(matches):
    dist = [m.distance for m in itertools.chain(*matches)]
    dist.sort()
    return dist[int(len(dist) / 2)]
