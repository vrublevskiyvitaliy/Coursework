import ioclass
from ioclass import filename
from ear_trianguation import EarTriangulation
from coloring import Coloring
from polygon import Polygon
import seidel


def art_gallery_problem(interface, points=None, show_decomposition=True):
    if points is None:
        points = ioclass.read_from_file(filename)

    poly = Polygon()
    poly.set_points(points)

    size = len(points)

    list_points = []
    for p in points:
        list_points.append([p.x, p.y])

    seidel_triangalator = seidel.Triangulator(list_points)
    triangles1 = seidel_triangalator.triangles()

    # Now for the GUI. Both the polygon and its triangulation have been scaled,
    # as specified above. Now we need to draw them on a Tkinter Canvas.
    # Setup and init a canvas:
    if show_decomposition:
        interface.draw_triangles(triangles1)

    # The last step is to output the triangulation of the original, non-scaled
    # polygon to the console:
    # ioclass.print_triangles_to_console(triangles1)

    art_gallery_coloring = Coloring()
    art_gallery_coloring.set_triangulation(points, triangles1)
    points_str, res = art_gallery_coloring.colorize()

    list_res = []
    for p in points_str:
        p = p.name
        list_res.append([points[int(p)].x, points[int(p)].y])

    interface.draw_result(list_res)
    interface.set_result(res)
