from collections import namedtuple
from math import sqrt
import random
try:
    import Image
except ImportError:
    from PIL import Image

#Create two named tuples for a cluster and a point
Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

#Gets all the points in the image and their colour values
def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=5):
    #open image, resize
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    #Get all the points
    points = get_points(img)
    #Get clusters using kmeans function
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return rgbs

#Euclidean distance that we're trying to minimize
def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

#Returns the point at the center of a group of points
def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

#kmeans algorithm
def kmeans(points, k, min_diff):
    #random.sample returns k length list of unique elements from points
    #This generates random clusters of points
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    #Every point in the dataset is assigned to its nearest centroid
    #If k = 3 , there are three centroids
    while 1:
        plists = [[] for i in range(k)]
        #Find nearest centroid for each point
        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        #The position of each centroid is updated by the means of the data get_points
        #that were assigned to that cluster.
        #Each center is recalculated with the new points
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        #This algorithm will repeat until the difference is less than 1
        if diff < min_diff:
            break

    return clusters
