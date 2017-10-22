from itertools import combinations
from math import sqrt
from pprint import pprint


points = [
    (4, 10),
    (7, 10),
    (4, 8),
    (6, 8),
    (12, 6),
    (10, 5),
    (3, 4),
    (11, 4),
    (9, 3),
    (12, 3),
    (2, 2),
    (5, 2),
]


def cluster(points, get_distance):
    clusters = list(points)

    while len(clusters) > 1:
        cluster1, cluster2 = get_closest_clusters(clusters, get_distance)

        clusters.remove(cluster1)
        clusters.remove(cluster2)

        clusters.append((cluster1, cluster2))
    
    return clusters[0]


def get_closest_clusters(clusters, get_distance):
    first_pair = True
    closest_clusters = None
    closest_clusters_distance = None

    for pair in combinations(clusters, 2):
        distance = get_distance(pair[0], pair[1])

        if first_pair or distance < closest_clusters_distance:
            closest_clusters = pair
            closest_clusters_distance = distance
            first_pair = False
    
    return closest_clusters


def get_points(cluster):
    points = []
    put_points(cluster, points)
    return points


def put_points(cluster, points):
    for subcluster in cluster:
        if isinstance(subcluster, tuple):
            put_points(subcluster, points)
        else:
            points.append(subcluster)


def print_cluster(cluster, depth=0):
    if isinstance(cluster, tuple):
        [print_cluster(subcluster, depth + 1) for subcluster in cluster]
    else:
        [print('    ', end='') for _ in range(depth)]
        print(cluster)   


print('\n(a) The minimum of the distances between any two points, one from each cluster.\n')

def get_distance(cluster1, cluster2):
    return 1

print_cluster(cluster(points, get_distance))


print('\n(b) The average of the distances between pairs of points, one from each of the two clusters.\n')

def get_distance(cluster1, cluster2):
    return 1

print_cluster(cluster(points, get_distance))
