from gui import GUI
from ear_trianguation import EarTriangulation
try:
    import tkinter         # May need to change 'Tkinter' to 'tkinter' on Windows
except:
    import Tkinter
import ioclass
from ioclass import filename
from coloring import Coloring
from polygon import Polygon
import ear_art_gallery_problem
import ear_triang_segment_tree


#filename = 'test.txt'


def main():
    interface = GUI()

    points = ioclass.read_from_file(filename)

    interface.set_points(points)
    '''
    x_max = 0
    y_max = 0

    for point in points:
        if point.x > x_max:
            x_max = point.x
        if point.y > y_max:
            y_max = point.y

    interface.max_point_x = x_max
    interface.max_point_y = y_max
    '''
    poly = Polygon()
    poly.set_points(points)

    #ear_art_gallery_problem.art_gallery_problem(interface, filename)
    ear_triang_segment_tree.ear_segment_art_gallery_problem(interface, filename)
    interface.draw_polygon_points(poly)
    root = interface.get_root()
    root.mainloop()

# def get_points

main()
