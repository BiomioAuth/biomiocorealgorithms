from tools import distance, mass_center, sort_clusters
import random
import sys

# TODO: KMeans standard
def KMeans(items, cluster_count, init_centers=[], max_distance=0):
    clusters = []
    cents = []
    currs = []
    get_random = True
    count = cluster_count
    if len(init_centers) > 0:
        count = len(init_centers)
        get_random = False
    for i in range(0, count, 1):
        val = []
        if get_random:
            center = random.randint(0, len(items) - 1)
            while val.__contains__(center):
                center = random.randint(0, len(items) - 1)
            val.append(center)
            item = items[center]
            currs.append(item.pt)
            cluster = dict()
            cluster['center'] = item.pt
            cluster['items'] = []
            cluster['id'] = i
            clusters.append(cluster)
        else:
            item = init_centers[i]
            currs.append(item)
            cluster = dict()
            cluster['center'] = item
            cluster['items'] = []
            cluster['id'] = i
            clusters.append(cluster)

    while cents != currs:
        cents = currs
        news = []
        for cluster in clusters:
            cluster['items'] = []
            news.append(cluster)
        clusters = news
        for item in items:
            # TODO: What about this? Here I finds cluster with minimal distance to item.pt
            min_dis = sys.float_info.max
            cl = dict()
            for cluster in clusters:
                c_dis = distance(item.pt, cluster['center'])
                if c_dis < min_dis:
                    min_dis = c_dis
                    cl = cluster
            clusters.remove(cl)
            elements = cl['items']
            elements.append(item)
            cl['items'] = elements
            clusters.append(cl)
        news = []
        currs = []
        for cluster in clusters:
            if len(cluster['items']) > 0:
                c = mass_center(cluster['items'])
                if (max_distance > 0) and (distance(c, cluster['center']) < max_distance):
                    currs.append(c)
                    cluster['center'] = c
                    news.append(cluster)
                else:
                    currs.append(cluster['center'])
                    news.append(cluster)
            else:
                currs.append(cluster['center'])
                news.append(cluster)
        clusters = news
    return sort_clusters(clusters)
