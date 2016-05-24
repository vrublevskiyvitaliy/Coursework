from point import Point
try:
    from Tkinter import *
except ImportError:
    from tkinter import *


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
            new_cursor = new_point

        # finally, link the new head and tail before returning the head:
        new_head.prev = new_cursor
        new_cursor.next = new_head
        return new_head, self.SIZE

    def area2(self, a, b, c):
        return ((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y))

    def xor(self, x, y):
        return x is not y

    def area_sign(self, a, b, c):
        a1 = (b.x - a.x) * 1.0 * (c.y - a.y)
        a2 = (c.x - a.x) * 1.0 * (b.y - a.y)

        area2 = a1 - a2

        if area2 > 0.5:
            return 1
        if area2 < -0.5:
            return -1
        return 0

    def left(self, a, b, c):
        return self.area_sign(a, b, c) > 0

    def left_on(self, a, b, c):
        return self.area_sign(a, b, c) >= 0

    def collinear(self, a, b, c):
        return self.area_sign(a, b, c) == 0

    # Checks if point c is geometrically in between points a and b.
    def is_between(self, a, b, c):
        if not self.collinear(a, b, c):
            return False

        if a.x != b.x:
            return (a.x <= c.x and c.x <= b.x) or (a.x >= c.x and c.x >= b.x)
        else:
            return (a.y <= c.y and c.y <= b.y) or (a.y >= c.y and c.y >= b.y)

    # Returns true if the line segment a,b intersects the
    def is_intersect(self, a, b, c, d):
        if self.intersect_prop(a, b, c, d):
            return True
        elif self.is_between(a, b, c) or self.is_between(a, b, d) or self.is_between(c, d, a) or \
                self.is_between(c, d, b):
            return True
        return False

    # Returns true if the line segment a,b is a diagonal
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

    # Returns true if the line segments a,b and c,d intersect "properly."
    def intersect_prop(self, a, b, c, d):
        if self.collinear(a, b, c) or self.collinear(a, b, d) or self.collinear(c, d, a) or self.collinear(c, d, b):
            return False

        return self.xor(self.left(a, b, c), self.left(a, b, d)) and self.xor(self.left(c, d, a), self.left(c, d, b))

    # This function is needed to distinguish internal
    def is_in_cone(self, a, b):
        a1 = a.next
        a0 = a.prev

        if self.left_on(a, a1, a0):
            return self.left(a, b, a0) and self.left(b, a, a1)
        else:
            return not (self.left_on(a, b, a1) and self.left(b, a, a0))

    def diagonal(self, a, b, head):
        return self.is_in_cone(a, b) and self.is_in_cone(b, a) and self.is_diagonal(a, b, head)

    def ear_init(self, head):
        v1 = head
        while True:
            v2 = v1.next
            v0 = v1.prev
            v1.ear = self.diagonal(v0, v2, head)
            v1 = v1.next

            if v1 is head:
                break

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
        k1 = 670.0 / x_max
        k2 = 470.0 / y_max

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
