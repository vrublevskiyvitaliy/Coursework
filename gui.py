try:
    from Tkinter import *
    import Tkinter.ttk as ttk
except ImportError:
    from tkinter import *
    import tkinter.ttk as ttk

from generator import generate_polygon, get_random_polygon
from polygon import Polygon
import ioclass
from ioclass import filename
import ear_art_gallery_problem
import ear_triang_segment_tree
import seidel_art_gallery_segment
import seidel_art_gallery_color


class GUI:

    def __init__(self):
        self.root = Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.attributes("-fullscreen", True)
        self.full_w, self.full_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        self.canvas_width = self.full_w
        self.canvas_height = 0.9 * self.full_h

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.res_text = StringVar()
        self.all_points_text = StringVar()

        self.method_combo = None
        self.generate_button = None
        # label = Label( root, textvariable=var, relief=RAISED )

        self.max_point_x = None
        self.max_point_y = None
        self.result_label = None
        self.all_points_label = None
        self.points = None
        self.show_decomposition_checkbox = None
        self.init()

    def set_points(self, points):
        self.points = points

        x_max = 0
        y_max = 0

        for point in points:
            if point.x > x_max:
                x_max = point.x
            if point.y > y_max:
                y_max = point.y

        self.max_point_x = x_max
        self.max_point_y = y_max
        self.set_all_points(len(points))

    def close_window(self, ev):
        self.root.destroy()

    def change_solution_method(self, ev):
        # 0 - ear - coloring
        # 1 - ear - segment - tree
        self.canvas.delete("all")
        points = self.points
        poly = Polygon()
        poly.set_points(points)
        self.draw_polygon_points(poly)
        show_decomposition = self.show_decomposition_checkbox.var.get() == 1
        mode = self.method_combo.current()
        if mode == 0:
            ear_art_gallery_problem.art_gallery_problem(interface=self, points=points,
                                                        show_decomposition=show_decomposition)
        elif mode == 1:
            ear_triang_segment_tree.ear_segment_art_gallery_problem(interface=self, points=points,
                                                                    show_decomposition=show_decomposition)
        elif mode == 2:
            seidel_art_gallery_segment.seidel_segment_art_gallery_problem(interface=self, points=points,
                                                                          show_decomposition=show_decomposition)
        elif mode == 3:
            seidel_art_gallery_color.art_gallery_problem(interface=self, points=points,
                                                         show_decomposition=show_decomposition)

    def generate_new_poly(self, ev):
        points = get_random_polygon()
        self.set_points(points)
        poly = Polygon()
        poly.set_points(points)
        self.canvas.delete("all")
        self.draw_polygon_points(poly)
        self.set_result(0)

    def init(self):
        root = self.root
        panel_frame = Frame(root, height=0.1 * self.full_h, bg='gray')
        panel_frame.pack(side='top', fill='x')

        self.canvas.pack()
        self.canvas.pack(side='bottom', fill='both', expand=1)

        quit_btn = Button(panel_frame, text='Quit')

        self.result_label = Label(panel_frame, textvariable=self.res_text, text='Result')
        self.all_points_label = Label(panel_frame, textvariable=self.all_points_text, text='Points:')

        quit_btn.bind("<Button-1>", self.close_window)

        quit_btn.place(
            x=0.01 * self.full_w,
            y=0.01 * self.full_h,
            width=0.07 * self.full_w,
            height=0.06 * self.full_h
        )

        self.result_label.place(
            x=0.11 * self.full_w,
            y=0.01 * self.full_h,
            width=0.07 * self.full_w,
            height=0.06 * self.full_h
        )

        list1 = ["Ear/Coloring", "Ear/Segment", "Seidel/Segment"]#, "Seidel/Color"]
        self.method_combo = ttk.Combobox(
            panel_frame,
            values=list1,
            style='Kim.TButton',
            justify='center',
            foreground='#FF0000',
            state='readonly'
        )

        self.method_combo.place(
            x=0.21 * self.full_w,
            y=0.01 * self.full_h,
            width=0.07 * self.full_w,
            height=0.04 * self.full_h
        )

        self.method_combo.bind('<<ComboboxSelected>>', self.change_solution_method)

        self.generate_button = Button(
            panel_frame,
            text='Generate'
        )

        self.generate_button.bind("<Button-1>", self.generate_new_poly)

        self.generate_button.place(
            x=0.31 * self.full_w,
            y=0.01 * self.full_h,
            width=0.07 * self.full_w,
            height=0.06 * self.full_h
        )

        self.all_points_label.place(
            x=0.41 * self.full_w,
            y=0.01 * self.full_h,
            width=0.07 * self.full_w,
            height=0.06 * self.full_h
        )

        var = IntVar()
        self.show_decomposition_checkbox = ttk.Checkbutton(
            panel_frame,
            text='Show decomposition',
            variable=var
        )
        self.show_decomposition_checkbox.var = var

        self.show_decomposition_checkbox.place(
            x=0.51 * self.full_w,
            y=0.01 * self.full_h,
            width=0.10 * self.full_w,
            height=0.06 * self.full_h
        )

    def get_canvas(self):
        return self.canvas

    def get_root(self):
        return self.root

    def set_result(self, number):
        self.res_text.set("Result: " + str(number))

    def set_all_points(self, number):
        self.all_points_text.set("Points: " + str(number))
    '''
    This function draws the polygon on a canvas and displays them. This is done
    by simply drawing lines between consecutive points. Also, small dots are
    drawn for easy identification of the vertices, and a small text label is
    also drawn next to each vertex (this text is the name of each Point object).

    @param canvas: The Tkinter Canvas widget on which to draw the polygon
    '''
    def draw_polygon(self, triangulation):
        canvas = self.canvas
        # Draw the polygon as a collection of lines:
        cursor = triangulation.HEAD
        while True:
            x1 = cursor.x
            y1 = cursor.y
            x2 = cursor.next.x
            y2 = cursor.next.y

            # First, draw text labels. Labels will be placed next to each vertex.
            self.draw_label(
                text=cursor.name,
                font="Times 8",
                x=x1,
                y=y1
            )
            # Draw a line from the current vertex to the next vertex:
            self.draw_line(
                p0_x=x1,
                p0_y=y1,
                p1_x=x2,
                p1_y=y2,
                width=2.0,
                color='black'
            )
            # Finally, draw a little dot at the vertex:
            self.draw_point(
                x=x1,
                y=y1,
                radius=4,
                color='black'
            )
            cursor = cursor.next
            if cursor.equals(triangulation.HEAD):
                break

    def draw_polygon_points(self, polygon):
        linked_list = polygon.get_linked_list()
        # Draw the polygon as a collection of lines:
        cursor = linked_list[0]
        while True:
            x1 = cursor.x
            y1 = cursor.y
            x2 = cursor.next.x
            y2 = cursor.next.y

            # First, draw text labels. Labels will be placed next to each vertex.
            self.draw_label(
                text=cursor.name,
                font="Times 8",
                x=x1,
                y=y1
            )
            # Draw a line from the current vertex to the next vertex:
            self.draw_line(
                p0_x=x1,
                p0_y=y1,
                p1_x=x2,
                p1_y=y2,
                width=2.0,
                color='black'
            )
            # Finally, draw a little dot at the vertex:
            self.draw_point(
                x=x1,
                y=y1,
                radius=2,
                color='black'
            )
            cursor = cursor.next
            if cursor.equals(linked_list[0]):
                break
    '''
    This function draws triangles, after a polygon is triangulated.

    @param canvas: A Tkinter Canvas widget on which to draw the triangles
    @param triangles: This should be the return value of the 'Triangulate' function

    The function draws triangles by simply drawing lines between the 3 points
    of each triangle.
    '''
    def draw_triangles(self, triangles):
        pointlist = self.points
        # The triangulation output is a list of triangles, where each triangle
        # is specified by the indices of 3 points. Get those 3 points from the
        # 'pointlist' and draw lines between them:
        if len(triangles) > 0:
            for t in triangles:
                # Find the 3 vertices with the matching indices:
                p0 = pointlist[int(t[0])]
                p1 = pointlist[int(t[1])]
                p2 = pointlist[int(t[2])]

                # Draw the 3 lines:
                self.draw_line(
                    p0_x=p0.x,
                    p0_y=p0.y,
                    p1_x=p1.x,
                    p1_y=p1.y,
                    width=1.0,
                    color='red'
                )
                self.draw_line(
                    p0_x=p0.x,
                    p0_y=p0.y,
                    p1_x=p2.x,
                    p1_y=p2.y,
                    width=1.0,
                    color='red'
                )
                self.draw_line(
                    p0_x=p2.x,
                    p0_y=p2.y,
                    p1_x=p1.x,
                    p1_y=p1.y,
                    width=1.0,
                    color='red'
                )

    def draw_result(self, points):
        for point in points:
            self.draw_point(x=point[0], y=point[1], color='red', radius=5)

    def draw_result_points(self, points):
        for point in points:
            self.draw_point(x=point.x, y=point.y, color='red', radius=5)

    def draw_point(self, x, y, color, radius):
        x, y = self.transform_point_for_drawing(x, y)
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def draw_line(self, p0_x, p0_y, p1_x, p1_y, color, width):
        p0_x, p0_y = self.transform_point_for_drawing(p0_x, p0_y)
        p1_x, p1_y = self.transform_point_for_drawing(p1_x, p1_y)

        self.canvas.create_line(p0_x, p0_y, p1_x, p1_y, width=width, fill=color)

    def draw_label(self, text, font, x, y):
        label = Label(self.canvas, text=text, font=font)
        #x, y = self.transform_point_for_drawing(x, y)
        #label.place(x=x+5, y=y+5)

    def transform_point_for_drawing(self, x, y):
        # size_x = 0.8 * self.full_w # max size for x
        # size_y = 0.7 * self.full_h # max size for y
        size_x = 0.8 * self.canvas_width
        size_y = 0.8 * self.canvas_height

        # scale
        koef_x = (size_x * 1.) / (self.max_point_x * 1.)
        koef_y = (size_y * 1.) / (self.max_point_y * 1.)

        # scale uniformly
        if koef_x > koef_y:
            koef = koef_y
        else:
            koef = koef_x

        new_x = koef * x
        new_y = koef * y

        new_x += 0.1 * self.canvas_width
        new_y = 0.9 * self.canvas_height - new_y

        return new_x, new_y

        pass