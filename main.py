from gui import GUI
from ear_trianguation import EarTriangulation
import tkinter         # May need to change 'Tkinter' to 'tkinter' on Windows
import ioclass


def main():
    filename = 'input1.txt'

    # Open the file from disk, read the points and create a linked-list
    # structure that represents the Polygon:
    headnode1, size1 = ioclass.create_linked_list(filename)

    # Check if the file reading was successful or if there were inconsistencies:
    if not headnode1 or size1 < 3:
        print("No triangulations to output")
        return

    # Create a Triangulation object from the linked list:
    t1 = EarTriangulation()
    t1.HEAD = headnode1
    t1.SIZE = size1

    # Create a copy of the linked list and use that to create a new
    # Triangulation object. This is an identical copy, but it will be scaled
    # and translated in order to be graphed on the canvas.
    headnode2, size2 = t1.clone_linked_list()
    t2 = EarTriangulation()
    t2.HEAD = headnode2
    t2.SIZE = size2
    t2.scale(True)
    t2.scale(True)

    # The scaling is just to make the polygon look better when viewing on a
    # canvas. Doing it multiple times is inefficient but makes the picture
    # better.
    # Do the triangulation. The return value is a list of 3-tuples, which
    # represent the vertices of each triangle.

    triangles1 = t1.triangulate()
    triangles2 = t2.triangulate()

    # Now for the GUI. Both the polygon and its triangulation have been scaled,
    # as specified above. Now we need to draw them on a Tkinter Canvas.
    # Setup and init a canvas:

    interface = GUI()

    canvas = interface.get_canvas()

    interface.draw_triangles(t2, triangles2)
    interface.draw_polygon(t2)

    # The last step is to output the triangulation of the original, non-scaled
    # polygon to the console:
    ioclass.print_triangles_to_console(triangles1)

    root = interface.get_root()
    root.mainloop()

    # Display the canvas:
    # tkinter.mainloop()

main()
