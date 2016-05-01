import seidel
import ioclass
from ear_trianguation import EarTriangulation
from polygon import Polygon
from SegmentTree import SegmentTree
from ioclass import filename


def seidel_segment_art_gallery_problem(interface, points=None, show_decomposition=True):
    if points is None:
        points = ioclass.read_from_file(filename)
    poly = Polygon()
    poly.set_points(points)
    size = len(points)

    list_points = []
    for p in points:
        list_points.append([p.x, p.y])

    #test = [[0, 0], [1, 0], [1, 1], [0, 1]]
    seidel_1 = seidel.Triangulator(list_points)

    triangles1 = seidel_1.triangles()

    if show_decomposition:
        interface.draw_triangles(triangles1)

    triangles_per_point = dict()
    segment_tree = SegmentTree(0, size - 1)

    for triangle in triangles1:
        p1, p2, p3 = triangle[0], triangle[1], triangle[2]

        if p1 not in triangles_per_point.keys():
            triangles_per_point[p1] = list()
        if p2 not in triangles_per_point.keys():
            triangles_per_point[p2] = list()
        if p3 not in triangles_per_point.keys():
            triangles_per_point[p3] = list()

        triangles_per_point[p1].append([p1, p2, p3])
        triangles_per_point[p2].append([p1, p2, p3])
        triangles_per_point[p3].append([p1, p2, p3])

    for point in triangles_per_point:

        segment_tree.add(int(point), int(point), len(triangles_per_point[point]))

    current_max = size
    start = 0
    end = size - 1
    current_max = segment_tree.query_max(start, end)
    current_max_index = segment_tree.query_max_index(start, end)
    res = []
    while current_max > 0:
        res.append(points[current_max_index])
        for triangle in triangles_per_point[current_max_index]:
            p1, p2, p3 = triangle[0], triangle[1], triangle[2]

            p1 = int(p1)
            p2 = int(p2)
            p3 = int(p3)

            segment_tree.add(p1, p1, -1)
            segment_tree.add(p2, p2, -1)
            segment_tree.add(p3, p3, -1)

        current_max = segment_tree.query_max(start, end)
        current_max_index = segment_tree.query_max_index(start, end)

    interface.draw_result_points(res)
    interface.set_result(len(res))

#test = [[0, 0], [1, 0], [1, 1], [0, 1]]
#seidel_1 = seidel.Triangulator(test)

#triangles = seidel_1.triangles()