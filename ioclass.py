from point import Point
from polygon import Polygon
import sys

filename = 'test.txt'


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


def read_from_file(filename='input.txt'):
    input_file = open(filename, 'r')
    n = int(input_file.readline())

    # Then read all the points and store them in a list:
    list1 = [x for x in input_file.readlines()]
    input_file.close()

    # The size of the list must match the number that was specified:
    if n != len(list1):
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

    for i in range(len(points)):
        points[i].name = str(i)


    return points


def create_linked_list(filename='input.txt'):
    
    points = read_from_file(filename)

    poly = Polygon()
    poly.set_points(points)

    points = poly.get_linked_list()
        
    return points[0], len(points)


def printf(format, *args):
    sys.stdout.write(format % args)


def print_triangles_to_console(triangles):
    printf("%d", len(triangles))
    for i in range(len(triangles)):
        t = triangles[i]
        printf("\n[%s,%s,%s]", t[0], t[1], t[2])
