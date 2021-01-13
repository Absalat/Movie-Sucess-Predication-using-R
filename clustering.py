def distance(p1, p2): # distance between points
    return abs(p1 - p2)

def calc_centroid(points):
    return (sum(points) / len(points)) if len(points) > 0 else None


def kmeans(points, k):
    centroids = points[:k]  # initial centroids, could be random.

    while True:
        clusters = [[] for _ in range(k)]
        resultClusters = []

        # the clustering phase
        for point in points:
            dist = []
            for centroid in centroids:
                d = distance(point, centroid)
                dist.append(d)
            min_dist = min(dist)  # choose the minimum distance
            index = dist.index(min_dist)  # target cluster index.

            # add the point to the cluster whose mean (centroid) minimized the distance.
            clusters[index].append(point)
            resultClusters.append(index)

        # calculating the new centroids
        new_centroids = []
        for i in range(len(clusters)):
            cluster = clusters[i]
            centr = calc_centroid(cluster)
            new_centroids.append(centroids[i] if centr == None else centr)

        # clustering complete. same centroids as before.
        if centroids == new_centroids: # if no change from previous round
            return centroids, resultClusters

        centroids = new_centroids
