from point import Point
import random

size_n = 100
size_m = 100
max_iterations = 100


def print_matrix(matrix):
    pass
    '''
    for row in matrix:
        for sell in row:
            print (sell, end=" ")
            # print sell,
        print
        # print
    '''


def get_random_next_point_eat(x, y, matrix):
    choices = [
        (x + 1, y, x + 2, y - 1, x + 2, y, x + 2, y + 1),
        (x - 1, y, x - 2, y - 1, x - 2, y, x - 2, y + 1),
        (x, y - 1, x - 1, y - 2, x, y - 2, x + 1, y - 2),
        (x, y + 1, x - 1, y + 2, x, y + 2, x + 1, y + 2)
    ]

    free_choices = []
    for choice in choices:
        if choice[0] < 1 or choice[0] >= size_n:
            continue

        if choice[1] < 1 or choice[1] >= size_m:
            continue

        if matrix[choice[0]][choice[1]] == 0:
            free_choices.append(choice)

    if len(free_choices) == 0:
        return None

    correct_choices = []

    for choice in free_choices:
        if choice[2] >= 1 and choice[2] < size_n:
            if choice[3] >= 1 and choice[3] < size_m:
                if matrix[choice[2]][choice[3]] == 1:
                    continue

        if choice[4] >= 1 and choice[4] < size_n:
            if choice[5] >= 1 and choice[5] < size_m:
                if matrix[choice[4]][choice[5]] == 1:
                    continue

        if choice[6] >= 1 and choice[6] < size_n:
            if choice[7] >= 1 and choice[7] < size_m:
                if matrix[choice[6]][choice[7]] == 1:
                    continue

        correct_choices.append(choice)

    if len(correct_choices) == 0:
        return None

    index = random.randint(0, len(correct_choices) - 1)

    return correct_choices[index][0], correct_choices[index][1]


def get_random_next_point_back(x, y, matrix):
    choices = [
        (x + 1, y),
        (x - 1, y),
        (x, y - 1),
        (x, y + 1)
    ]

    free_choices = []
    for choice in choices:
        if choice[0] < 0 or choice[0] >= size_n:
            continue

        if choice[1] < 0 or choice[1] >= size_m:
            continue

        if matrix[choice[0]][choice[1]] == 1:
            free_choices.append(choice)

    if len(free_choices) == 0:
        return None

    index = random.randint(0, len(free_choices) - 1)

    return free_choices[index][0], free_choices[index][1]


def generate(initial_matrix, iterations=None):

    #if iterations is not None:
    #    max_iterations = iterations

    current_point_x = random.randint(1, size_n-1)
    current_point_y = random.randint(1, size_m-1)

    initial_matrix[current_point_x][current_point_y] = 1

    #print_matrix(initial_matrix)
    #print('************************')

    # number_of_vertixes = 4

    iteration = 0


    # 1 - eat
    # 0 - back
    next_task = 1
    while iteration < max_iterations:
        if next_task == 1:
            point = get_random_next_point_eat(current_point_x, current_point_y, initial_matrix)
            if point is None:
                next_task = 0
            else:
                current_point_x = point[0]
                current_point_y = point[1]
                initial_matrix[current_point_x][current_point_y] = 1

        if next_task == 0:
            point = get_random_next_point_back(current_point_x, current_point_y, initial_matrix)
            current_point_x = point[0]
            current_point_y = point[1]

        next_task = random.randint(0,1)
        iteration += 1
        #print('********************')
        #print_matrix(initial_matrix)

    #print('********************')
    #print_matrix(initial_matrix)
    print("create matrix")


def get_coordinate_of_point(x, y, dx, dy):
    return 2 * x + dx, 2 * y + dy


def is_there_wall(x1, y1, x2, y2, initial_matrix):
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    if x == x1 and x == x2:
        y1 = y / 2
        y2 = y / 2

        x1 = (x - 1) / 2
        x2 = (x + 1) / 2
    else:
        x1 = x / 2
        x2 = x / 2

        y1 = (y - 1) / 2
        y2 = (y + 1) / 2

    y1 = y1 - 1
    y2 = y2 - 1
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    one = initial_matrix[x1][y1]
    two = initial_matrix[x2][y2]

    initial_matrix[x1][y1] = 2
    initial_matrix[x2][y2] = 2

    #print ('****************')
    #print(str(x1) + ' - ' +str())
    #print_matrix(initial_matrix)
    #print ('****************')

    initial_matrix[x1][y1] = one
    initial_matrix[x2][y2] = two
    if (initial_matrix[x1][y1] + initial_matrix[x2][y2]) % 2 == 0:
        return False
    else:
        return True


def transform_matrix_to_coordinates(matrix):
    write_to_file = True
    start_x = -1
    start_y = -1

    for i in range(1, size_n + 1):
        for j in range(1, size_m + 1):
            if matrix[i][j] == 1:
                start_x = i
                start_y = j
                break
        if start_x != -1:
            break

    points = list()
    # points.append(get_coordinate_of_point(start_x, start_y, -1, +1))
    points.append(get_coordinate_of_point(start_x, start_y, -1, +1))

    # curent_point = get_coordinate_of_point(start_x, start_y, +1, +1)
    curent_point = (points[0][0], points[0][1] + 2)
    while curent_point != points[0]:
        points.append(curent_point)
        posible_next_points = list()

        posible_next_points.append((curent_point[0] - 2, curent_point[1])) # up
        posible_next_points.append((curent_point[0], curent_point[1] + 2)) # right
        posible_next_points.append((curent_point[0] + 2, curent_point[1])) # down
        posible_next_points.append((curent_point[0], curent_point[1] - 2)) # left

        is_exist = False
        for point in posible_next_points:
            if point == points[len(points) - 2]:
                # it is the previous
                continue
            if is_there_wall(curent_point[0], curent_point[1], point[0], point[1], matrix):
                # points.append(point)
                curent_point = point
                is_exist = True
                break
        if not is_exist:
            #print 'Error'
            #print(points)
            break


    # print points
    correct_points = list()
    x_min = 10000000
    y_min = 10000000

    for point in points:
        correct_points.append((point[1], point[0]))
        if point[1] < x_min:
            x_min = point[1]
        if point[0] < y_min:
            y_min = point[0]

    points = list()
    for point in correct_points:
        points.append((point[0] - x_min, point[1] - y_min))
    #'''
    correct_points = list()
    # correct_points.append(points[0])
    for point in points:
        if len(correct_points) < 2:
            correct_points.append(point)
            continue

        low = correct_points[len(correct_points) - 2]
        middle = correct_points[len(correct_points) - 1]
        if low[0] == point[0] and low[0] == middle[0] or\
            low[1] == point[1] and low[1] == middle[1]:
            del correct_points[len(correct_points) - 1]
        correct_points.append(point)

    low = correct_points[len(correct_points) - 2]
    middle = correct_points[len(correct_points) - 1]
    point = correct_points[0]
    if low[0] == point[0] and low[0] == middle[0] or\
            low[1] == point[1] and low[1] == middle[1]:
            del correct_points[len(correct_points) - 1]


    points = correct_points
    if write_to_file:
        #'''
        f = open('test.txt', 'w')
        f.write(str(len(points)) + '\n')

        for point in points:
            f.write('[' + str(point[0]) + ', ' + str(point[1]) + ']' + '\n')
        f.close()
    print("create poly")
    return points


def generate_polygon():
    initial_matrix = [[0 for x in range(-1, size_n + 1)] for y in range(-1, size_m + 1)]
    generate(initial_matrix)
    transform_matrix_to_coordinates(initial_matrix)


def get_random_polygon(iterations=None):
    initial_matrix = [[0 for x in range(-1, size_n + 1)] for y in range(-1, size_m + 1)]
    generate(initial_matrix, iterations)
    points = transform_matrix_to_coordinates(initial_matrix)
    c_points = []
    for p in points:
        pt = Point(p[0], p[1])
        c_points.append(pt)

    for i in range(len(c_points)):
        c_points[i].name = str(i)
    return c_points

#generate_polygon()
#generate()
#transform_matrix_to_coordinates(initial_matrix)