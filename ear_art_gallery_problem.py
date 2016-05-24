import ioclass
from ioclass import filename
from ear_trianguation import EarTriangulation
from coloring import Coloring
from polygon import Polygon


def art_gallery_problem(interface, points=None, show_decomposition=True):
    if points is None:
        points = ioclass.read_from_file(filename)
    poly = Polygon()

    poly.set_points(points)

    linked_list = poly.get_linked_list()
    headnode = linked_list[0]
    size = len(points)

    # Check if the file reading was successful or if there were inconsistencies:
    if not headnode or size < 3:
        print("No triangulations to output")
        return

    # Create a Triangulation object from the linked list:
    t1 = EarTriangulation(headnode, size)
    # Do the triangulation.
    triangles1 = t1.triangulate()

    if show_decomposition:
        interface.draw_triangles(triangles1)

    art_gallery_coloring = Coloring()
    art_gallery_coloring.set_triangulation(points, triangles1)
    points_str, res = art_gallery_coloring.colorize()

    list_res = []
    for p in points_str:
        p = p.name
        list_res.append([points[int(p)].x, points[int(p)].y])

    interface.draw_result(list_res)
    interface.set_result(res)
    return res
