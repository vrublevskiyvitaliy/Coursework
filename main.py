from gui import GUI
from ear_trianguation import EarTriangulation
try:
    import tkinter         # May need to change 'Tkinter' to 'tkinter' on Windows
except:
    import Tkinter
import ioclass
from coloring import Coloring
from polygon import Polygon
import ear_art_gallery_problem


def main():
    filename = 'input1.txt'

    '''
    # Open the file from disk, read the points and create a linked-list
    # structure that represents the Polygon:
    headnode1, size1 = ioclass.create_linked_list(filename)

    # Check if the file reading was successful or if there were inconsistencies:
    if not headnode1 or size1 < 3:
        print("No triangulations to output")
        return

    pointlist = []
    cursor = headnode1
    while True:
        pointlist.append(cursor)
        cursor = cursor.next
        if cursor.equals(headnode1):
            break

    # Create a Triangulation object from the linked list:
    t1 = EarTriangulation()
    t1.HEAD = headnode1
    t1.SIZE = size1

    # The scaling is just to make the polygon look better when viewing on a
    # canvas. Doing it multiple times is inefficient but makes the picture
    # better.
    # Do the triangulation. The return value is a list of 3-tuples, which
    # represent the vertices of each triangle.

    triangles1 = t1.triangulate()

    # Now for the GUI. Both the polygon and its triangulation have been scaled,
    # as specified above. Now we need to draw them on a Tkinter Canvas.
    # Setup and init a canvas:

    interface = GUI()

    interface.draw_triangles(t1, triangles1)
    interface.draw_polygon(t1)

    # The last step is to output the triangulation of the original, non-scaled
    # polygon to the console:
    ioclass.print_triangles_to_console(triangles1)

    art_gallery_coloring = Coloring()
    art_gallery_coloring.set_triangulation(pointlist, triangles1)
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
    root = interface.get_root()
    root.mainloop()
    '''
    interface = GUI()

    points = ioclass.read_from_file(filename)
    poly = Polygon()
    poly.set_points(points)

    interface.draw_polygon_points(poly)

    ear_art_gallery_problem.art_gallery_problem(interface, filename)

    root = interface.get_root()
    root.mainloop()

main()
