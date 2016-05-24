
class Polygon:
    def __init__(self):
        self.points = None

    def get_linked_list(self):

        # create clone
        points = []
        for p in self.points:
            points.append(p.get_clone())

        # This list is now treated as the points that comprise the polygon, in
        # counterclockwise order. Use this to create the linked-list structure:
        first_point = points[0]
        last_point = points[len(points) - 1]

        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]

            # Link them together:
            p1.next = p2
            p2.prev = p1

        # To complete the structure, link the first and last vertices together to
        # create a circular linked-list:
        first_point.prev = last_point
        last_point.next = first_point

        return points

    def set_points(self, points):
        self.points = points
        self.remove_duplicates()

    def remove_duplicates(self):
        length = len(self.points)
        i = 0

        while i < length - 1:
            j = i + 1
            while j < length:
                p1 = self.points[i]
                p2 = self.points[j]
                if p1.equals(p2):
                    length -= 1
                    self.points.remove(p2)
                else:
                    j += 1
            i += 1

