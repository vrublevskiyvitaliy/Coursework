from point import Point
import ioclass
import tkinter


class EarTriangulation:
    def __init__(self, head=None, size=0):
        self.HEAD = head
        self.SIZE = size

    def clone_linked_list(self):
        cursor = self.HEAD
        
        # make a copy of the head first:
        new_head = Point(cursor.x, cursor.y)
        new_head.ear = cursor.ear
        new_head.name = cursor.name
        
        # use a loop to create clones of the rest of the points:
        cursor = cursor.next
        new_cursor = new_head
        while cursor is not self.HEAD:
            new_point = Point(cursor.x, cursor.y)
            new_point.ear = cursor.ear
            new_point.name = cursor.name
            
            # link the previous point to the new one:
            new_cursor.next = new_point
            new_point.prev = new_cursor
            
            cursor = cursor.next
            new_cursor = new_point           # same as: new_cursor = new_cursor.next

        # finally, link the new head and tail before returning the head:
        new_head.prev = new_cursor
        new_cursor.next = new_head
        return new_head, self.SIZE

    @staticmethod
    def area2(a, b, c):
        return ((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y))

    @staticmethod
    def xor(x, y):
        return x is not y

    @staticmethod
    def area_sign(a, b, c):
        a1 = (b.x - a.x) * 1.0 * (c.y - a.y)
        a2 = (c.x - a.x) * 1.0 * (b.y - a.y)

        area2 = a1 - a2

        if area2 > 0.5:
            return 1
        if area2 < -0.5:
            return -1
        return 0

    @staticmethod
    def left(self, a, b, c):
        return self.area_sign(a, b, c) > 0

    @staticmethod
    def left_on(self, a, b, c):
        return self.area_sign(a, b, c) >= 0

    @staticmethod
    def collinear(self, a, b, c):
        return self.area_sign(a, b, c) == 0

    '''
    Adapted from O'Rourke. Checks if point c is geometrically in between 
    points a and b. In between means either in terms of x or y coordinate 
    ranges.
    '''
    @staticmethod
    def is_between(self, a, b, c):
        if not self.collinear(a, b, c):
            return False

        if a.x != b.x:
            return (a.x <= c.x and c.x <= b.x) or (a.x >= c.x and c.x >= b.x)
        else:
            return (a.y <= c.y and c.y <= b.y) or (a.y >= c.y and c.y >= b.y)

    '''
    Adapted from O'Rourke. Returns true if the line segment a,b intersects the 
    line segment c,d.
    '''
    @staticmethod
    def is_intersect(self, a, b, c, d):
        if self.intersect_prop(a, b, c, d):
            return True
        elif self.is_between(a, b, c) or self.is_between(a, b, d) or self.is_between(c, d, a) or \
                self.is_between(c, d, b):
            return True
        return False

    '''
    Adapted from O'Rourke. Returns true if the line segment a,b is a diagonal 
    of the polygon.
    '''
    @staticmethod
    def is_diagonal(self, a, b, head):
        c = head

        while True:
            c1 = c.next
            if self.xor(c, a) and self.xor(c1, a) and self.xor(c, b) and self.xor(c1, b) \
                    and self.is_intersect(a, b, c, c1):
                return False
            c = c.next
            if c is head:
                break

        return True

    '''
    Adapted from O'Rourke. Returns true if the line segments a,b and c,d 
    intersect "properly." A proper intersection is when the two segments fully 
    cross each other. If one segment's endpoint lies on the other segment, it's 
    not considered a proper intersection.
    '''
    @staticmethod
    def intersect_prop(self, a, b, c, d):
        if self.collinear(a, b, c) or self.collinear(a, b, d) or self.collinear(c, d, a) or self.collinear(c, d, b):
            return False

        return self.xor(self.left(a, b, c), self.left(a, b, d)) and self.xor(self.left(c, d, a), self.left(c, d, b))

    '''
    Adapted from O'Rourke. This function is needed to distinguish internal 
    diagonals from the external ones.
    '''
    @staticmethod
    def is_in_cone(self, a, b):
        a1 = a.next
        a0 = a.prev

        if self.left_on(a, a1, a0):
            return self.left(a, b, a0) and self.left(b, a, a1)
        else:
            return not (self.left_on(a, b, a1) and self.left(b, a, a0))

    '''
    Adapted from O'Rourke. 
    '''
    def diagonal(self, a, b, head):
        return self.is_in_cone(a, b) and self.is_in_cone(b, a) and self.is_diagonal(a, b, head)

    '''
    Adapted from O'Rourke. This function must be called initially before the 
    triangulation is performed, because the ear status of each vertex must be
    initialized before triangulation can take place.
    '''
    def ear_init(self, head):
        v1 = head
        while True:
            v2 = v1.next
            v0 = v1.prev
            v1.ear = self.diagonal(v0, v2, head)
            v1 = v1.next

            if v1 is head:
                break

    '''
    This is the actual triangulation function, which makes use of all the helper
    functions defined above. Note that since the linked list will be
    destroyed during the triangulation process (since the polygon's ears are
    clipped off), a new linked list is created so that the original linked 
    list is preserved.
    
    @return: A list of 3-tuples. Each 3-tuple is of the form [v1, v2, v3], 
            which represents a triangle. All of these tuples, taken together,
            represents the triangulated polygon.
            
    Note that the return value can be modified easily so that some other values 
    of the polygon can be returned instead - for example, the coordinates of 
    the triangles or the Point objects themselves.
    '''
    def triangulate(self):
        return_list = []

        self.ear_init(self.HEAD)
        # Create a clone of the linked list just before starting the
        # triangulation process:
        head, n = self.clone_linked_list()
        
        # Each step of the outer loop clips off one ear
        while n > 3:
            v2 = head
            ear_found = False
            while True:
                if v2.ear:
                    ear_found = True
                    # Ear found
                    v3 = v2.next
                    v4 = v3.next
                    v1 = v2.prev
                    v0 = v1.prev

                    # v1,v3 is a diagonal
                    tri = [v1.name, v2.name, v3.name]
                    return_list.append(tri)

                    # Update the ear status of the diagonal endpoints:
                    v1.ear = self.diagonal(v0, v3, head)
                    v3.ear = self.diagonal(v1, v4, head)

                    # Cut off the ear v2:
                    v1.next = v3
                    v3.prev = v1
                    head = v3
                    n -= 1

                    if n == 3:
                        # the polygon has been reduced down to 3 vertices, so
                        # output that as the last triangulation and return:
                        v2 = head
                        v1 = v2.prev
                        v3 = v2.next
                        tri = [v1.name, v2.name, v3.name]
                        return_list.append(tri)
                        return return_list

                    break
                v2 = v2.next
                if v2 is head:
                    break

            if not ear_found:
                print("Error! Ear not found")
                break
        return return_list

    '''
    This function draws the polygon on a canvas and displays them. This is done 
    by simply drawing lines between consecutive points. Also, small dots are 
    drawn for easy identification of the vertices, and a small text label is
    also drawn next to each vertex (this text is the name of each Point object).
    
    @param canvas: The Tkinter Canvas widget on which to draw the polygon
    '''
    def draw_polygon(self, canvas):
            
        # Draw the polygon as a collection of lines:
        cursor = self.HEAD
        while True:
            x1 = cursor.x
            y1 = cursor.y
            x2 = cursor.next.x
            y2 = cursor.next.y

            # First, draw text labels. Labels will be placed next to each vertex.
            label = tkinter.Label(canvas, text=cursor.name, font="Times 8")
            label.place(x=x1 + 5, y=700 - (y1 + 5))

            # Draw a line from the current vertex to the next vertex:
            canvas.create_line(x1, 700 - y1, x2, 700 - y2, width=2.0, fill='black')

            # Finally, draw a little dot at the vertex:
            canvas.create_oval(x1 - 4, 700 - (y1 - 4), x1 + 4, 700 - (y1 + 4), fill='black')
            
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break

    '''
    This function draws triangles, after a polygon is triangulated.
    
    @param canvas: A Tkinter Canvas widget on which to draw the triangles
    @param triangles: This should be the return value of the 'Triangulate' function
    
    The function draws triangles by simply drawing lines between the 3 points 
    of each triangle.
    '''
    def draw_triangles(self, canvas, triangles):
        # It's convenient to have the points as a list instead of a linked list:
        pointlist = []
        cursor = self.HEAD
        while True:
            pointlist.append(cursor)
            cursor = cursor.next
            if cursor.equals(self.HEAD):
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
                canvas.create_line(p0.x, 700 - p0.y, p1.x, 700 - p1.y, width=1.0, fill='red')
                canvas.create_line(p0.x, 700 - p0.y, p2.x, 700 - p2.y, width=1.0, fill='red')
                canvas.create_line(p2.x, 700 - p2.y, p1.x, 700 - p1.y, width=1.0, fill='red')

    '''
    This method does some translating and scaling so that the polygon is displayed
    nicely on the canvas.
    
    First, all points are translated so that the point with the minimum x-coordinate
    is very close to the y-axis, and the point with the minimum y-coordinate is
    very close to the x-axis (about 10 pixels). No points will have negative
    coordinates after this translation.
    
    What this translation does is make all points very close to the x and y axes
    in the first quadrant of the plane.
    
    Then, each point's x and y values are multiplied by two scaling factors 
    k1 and k2, respectively. These are calculated such that the most extreme
    points will still remain inside the canvas after they're scaled.
    
    
    @param uniform: True if x and y coordinates should be scaled by the same 
    factor. If True, both x and y will be scaled by min(k1, k2).
    '''
    def scale(self, uniform=False):
        x_min = 1000000000  # Initialize to some huge numbers
        y_min = 1000000000
    
        # Traverse the list and find the smallest x and y values:
        cursor = self.HEAD
        while True:
            if cursor.x < x_min:
                x_min = cursor.x
            if cursor.y < y_min:
                y_min = cursor.y
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break

        # The following loop translates all x- and y-values to make them all positive
        # (in order to make them as close to the origin as possible):
        cursor = self.HEAD
        while True:
            cursor.x = cursor.x - x_min + 10
            cursor.y = cursor.y - y_min + 10
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break

        # Find the new x_min and y_min, and also x_max and y_max:
        x_min = 1000000000
        y_min = 1000000000
        x_max = 0
        y_max = 0
        cursor = self.HEAD
        while True:
            if cursor.x < x_min:
                x_min = cursor.x
            if cursor.y < y_min:
                y_min = cursor.y
            if cursor.x > x_max:
                x_max = cursor.x
            if cursor.y > y_max:
                y_max = cursor.y
                
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
            
        # Find the scaling factor:
        # 1250 and 690 are based on the canvas dimensions (1280 x 720)
        k1 = 1250.0 / x_max
        k2 = 690.0 / y_max

        if uniform:
            # Set both k1 and k2 to be min(k1, k2)
            if k1 < k2:
                k2 = k1
            else:
                k1 = k2

        # Multiply each point by the scaling factor:
        cursor = self.HEAD
        while True:
            cursor.scale(k1, k2)
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
