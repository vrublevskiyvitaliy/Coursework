import random

size_n = 10#0
size_m = 10#0


initial_matrix = [[0 for x in range(size_n)] for y in range(size_m)]


def print_matrix(matrix):
    for row in matrix:
        for sell in row:
            # print (sell, end=" ")
            print sell,
        print
        # print


def get_random_next_point_eat(x, y, matrix):
    choices = [
        (x + 1, y, x + 2, y),
        (x - 1, y, x - 1, y),
        (x, y - 1, x, y - 2),
        (x, y + 1, x, y + 2)
    ]

    free_choices = []
    for choice in choices:
        if choice[0] < 0 or choice[0] >= size_n:
            continue

        if choice[1] < 0 or choice[1] >= size_m:
            continue

        if matrix[choice[0]][choice[1]] == 0:
            free_choices.append(choice)

    if len(free_choices) == 0:
        return None

    correct_choices = []

    for choice in free_choices:
        if choice[2] < 0 or choice[2] >= size_n:
            correct_choices.append(choice)
            continue

        if choice[3] < 0 or choice[3] >= size_m:
            correct_choices.append(choice)
            continue

        if matrix[choice[2]][choice[3]] == 0:
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


def generate():
    current_point_x = random.randint(1, size_n-1)
    current_point_y = random.randint(1, size_m-1)



    initial_matrix[current_point_x][current_point_y] = 1

    print_matrix(initial_matrix)
    print('************************')

    # number_of_vertixes = 4

    iteration = 0
    max_iterations = 50

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

    print('********************')
    print_matrix(initial_matrix)






generate()