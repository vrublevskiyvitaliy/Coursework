from tkinter import *


class GUI:

    def __init__(self):
        self.root = Tk()
        # 1280 x 720
        self.canvas_width = 700
        self.canvas_height = 500
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)

        self.init()

    def close_window(self, ev):
        self.root.destroy()

    def init(self):
        root = self.root
        panel_frame = Frame(root, height=60, bg='gray')

        self.canvas.pack()

        panel_frame.pack(side='top', fill='x')
        self.canvas.pack(side='bottom', fill='both', expand=1)

        quit_btn = Button(panel_frame, text='Quit')

        quit_btn.bind("<Button-1>", self.close_window)

        quit_btn.place(x=10, y=10, width=40, height=40)

        # root.mainloop()

    def get_canvas(self):
        return self.canvas

    def get_root(self):
        return self.root

    '''
    This function draws the polygon on a canvas and displays them. This is done
    by simply drawing lines between consecutive points. Also, small dots are
    drawn for easy identification of the vertices, and a small text label is
    also drawn next to each vertex (this text is the name of each Point object).

    @param canvas: The Tkinter Canvas widget on which to draw the polygon
    '''
    def draw_polygon(self, triangulation):
        canvas = self.canvas
        const_y = 500
        const_x = 500
        # Draw the polygon as a collection of lines:
        cursor = triangulation.HEAD
        while True:
            x1 = cursor.x
            y1 = cursor.y
            x2 = cursor.next.x
            y2 = cursor.next.y

            # First, draw text labels. Labels will be placed next to each vertex.
            label = Label(canvas, text=cursor.name, font="Times 8")

            label.place(x=x1 + 5 + const_x, y=const_y - (y1 + 5))

            # Draw a line from the current vertex to the next vertex:
            canvas.create_line(x1 + const_x, const_y - y1, x2 + const_x, const_y - y2, width=2.0, fill='black')

            # Finally, draw a little dot at the vertex:
            canvas.create_oval(x1 - 4 + const_x, const_y - (y1 - 4), x1 + 4 + const_x, const_y - (y1 + 4), fill='black')

            cursor = cursor.next
            if cursor.equals(triangulation.HEAD):
                break

    '''
    This function draws triangles, after a polygon is triangulated.

    @param canvas: A Tkinter Canvas widget on which to draw the triangles
    @param triangles: This should be the return value of the 'Triangulate' function

    The function draws triangles by simply drawing lines between the 3 points
    of each triangle.
    '''
    def draw_triangles(self, triangulation, triangles):
        const_x = 500
        const_y = 500

        # It's convenient to have the points as a list instead of a linked list:
        pointlist = []
        cursor = triangulation.HEAD
        while True:
            pointlist.append(cursor)
            cursor = cursor.next
            if cursor.equals(triangulation.HEAD):
                break

        # The triangulation output is a list of triangles, where each triangle
        # is specified by the indices of 3 points. Get those 3 points from the
        # 'pointlist' and draw lines between them:
        if len(triangles) > 0:
            for t in triangles:
                # Find the 3 vertices with the matching indices:
                p0 = pointlist[int(t[0]) - 1]
                p1 = pointlist[int(t[1]) - 1]
                p2 = pointlist[int(t[2]) - 1]

                # Draw the 3 lines:
                self.canvas.create_line(const_x + p0.x, const_y - p0.y, const_x + p1.x, const_y - p1.y, width=1.0, fill='red')
                self.canvas.create_line(const_x + p0.x, const_y - p0.y, const_x + p2.x, const_y - p2.y, width=1.0, fill='red')
                self.canvas.create_line(const_x + p2.x, const_y - p2.y, const_x + p1.x, const_y - p1.y, width=1.0, fill='red')
