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

    # Do the triangulation. The return value is a list of 3-tuples, which
    # represent the vertices of each triangle.

    triangles1 = t1.triangulate()

    # Now for the GUI. Both the polygon and its triangulation have been scaled,
    # as specified above. Now we need to draw them on a Tkinter Canvas.
    # Setup and init a canvas:
    if show_decomposition:
        interface.draw_triangles(triangles1)

    # The last step is to output the triangulation of the original, non-scaled
    # polygon to the console:
    ioclass.print_triangles_to_console(triangles1)

    art_gallery_coloring = Coloring()
    art_gallery_coloring.set_triangulation(points, triangles1)
    points, res = art_gallery_coloring.colorize()

    list_res = []
    for p in points:
        cursor = t1.HEAD
        p = p.name
        index = 0
        while index < int(p):
            index += 1
            cursor = cursor.next

        list_res.append([cursor.x, cursor.y])

    interface.draw_result(list_res)
    interface.set_result(res)
