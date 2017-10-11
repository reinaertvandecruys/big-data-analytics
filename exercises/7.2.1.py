from pprint import pprint


points = [1, 4, 9, 16, 25, 36, 49, 64, 81]

clusters = [(point, ()) for point in points]


while len(clusters) > 1:
    clusters = sorted(clusters)

    closest_pair_indices = (0, 1)
    closest_pair_distance = clusters[1][0] - clusters[0][0]

    for i in range(1, len(clusters) - 1):
        distance = clusters[i + 1][0] - clusters[i][0]

        if distance < closest_pair_distance:
            closest_pair_indices = (i, i + 1)
            closest_pair_distance = distance

    cluster1 = clusters[closest_pair_indices[0]]
    cluster2 = clusters[closest_pair_indices[1]]
    centroid = (cluster1[0] + cluster2[0]) / 2
    del clusters[closest_pair_indices[1]]
    del clusters[closest_pair_indices[0]]
    clusters.append((centroid, (cluster1, cluster2)))


def print_cluster(cluster, depth):
    centroid, points = cluster

    [print('    ', end='') for _ in range(depth)]
    print('%08.5f' % centroid)

    depth += 1

    for cluster in points:
        print_cluster(cluster, depth)


print_cluster(clusters[0], 0)
