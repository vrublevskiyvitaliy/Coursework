from point import Point
import sys


def remove_duplicates(list_of_points):
    length = len(list_of_points)
    i = 0
    
    while i < length - 1:
        j = i + 1
        while j < length:
            p1 = list_of_points[i]
            p2 = list_of_points[j]
            if p1.equals(p2):
                length -= 1
                list_of_points.remove(p2)
            else:
                j += 1
        i += 1
        

def create_linked_list(filename='input.txt'):
    
    input_file = open(filename, 'r')
    n = int(input_file.readline())

    # Then read all the points and store them in a list:
    list1 = [x for x in input_file.readlines()]
    input_file.close()

    # The size of the list must match the number that was specified:
    if n is not len(list1):
        return None, 0
    
    # Go through the list and check the input for any inconsistencies
    for x in list1:
        if len(x) < 2:
            return None, 0
        x = x.strip()

    points = []
    # Go through the list and remove the '[' and ']' signs, and create Point
    # objects using the x and y coordinates:
    for i in range(n):
        p = list(list1[i])
        p.remove('[')
        p.remove(']')
        p = "".join(p)
        p = p.split(',')
        x = int(p[0])
        y = int(p[1])
        # construct a Point object:
        pt = Point(x, y)
        points.append(pt)

    # Remove any duplicate points from the list:
    remove_duplicates(points)

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

    # Also, give the Points simple names to help out with visualization/debugging:
    for i in range(len(points)):
        points[i].name = str(i + 1)
        
    return first_point, len(points)


def printf(format, *args):
    sys.stdout.write(format % args)


def print_triangles_to_console(triangles):
    printf("%d", len(triangles))
    for i in range(len(triangles)):
        t = triangles[i]
        printf("\n[%s,%s,%s]", t[0], t[1], t[2])
