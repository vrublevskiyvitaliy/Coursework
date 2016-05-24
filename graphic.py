# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt


def run():
    filename = 'stat.txt'
    input_file = open(filename, 'r')
    n = int(input_file.readline())
    list_1 = [x for x in input_file.readlines()]
    input_file.close()


    res_dict = {}
    for i in range(n):
        p = list(list_1[i])
        p = "".join(p)
        p = p.split(' ')
        n_vertex = int(p[0])
        if n_vertex not in res_dict.keys():
            res_dict[n_vertex] = dict()
            res_dict[n_vertex]['ears_coloring'] = list()
            res_dict[n_vertex]['ears_segment'] = list()
            res_dict[n_vertex]['seidel_segment'] = list()
            res_dict[n_vertex]['convex_segment'] = list()

        res_dict[n_vertex]['ears_coloring'].append(int(p[1]))
        res_dict[n_vertex]['ears_segment'].append(int(p[2]))
        res_dict[n_vertex]['seidel_segment'].append(int(p[4]))
        res_dict[n_vertex]['convex_segment'].append(int(p[3]))

    for n_vertex in res_dict:
        res_dict[n_vertex]['e_c_n'] = \
            sum(res_dict[n_vertex]['ears_coloring']) / len(res_dict[n_vertex]['ears_coloring'])
        res_dict[n_vertex]['e_s_n'] = \
            sum(res_dict[n_vertex]['ears_segment']) / len(res_dict[n_vertex]['ears_segment'])
        res_dict[n_vertex]['s_s_n'] = \
            sum(res_dict[n_vertex]['seidel_segment']) / len(res_dict[n_vertex]['seidel_segment'])
        res_dict[n_vertex]['c_s_n'] = \
            sum(res_dict[n_vertex]['convex_segment']) / len(res_dict[n_vertex]['convex_segment'])

    keylist = res_dict.keys()
    keylist = sorted(keylist)
    x_a = list()
    y_e_c = list()
    y_e_s = list()
    y_s_s = list()
    y_c_s = list()

    for key in keylist:
        x_a.append(key)
        y_e_c.append(res_dict[key]['e_c_n'])
        y_e_s.append(res_dict[key]['e_s_n'])
        y_s_s.append(res_dict[key]['s_s_n'])
        y_c_s.append(res_dict[key]['c_s_n'])

    n_3 = [x / 3 for x in x_a]
    n_4 = [x / 4 for x in x_a]
    n_5 = [x / 5 for x in x_a]

    line_1, line_2, line_3, line_4, line_5, line_6, line_7 = plt.plot(
            x_a, y_e_c,
            x_a, y_e_s,
            x_a, y_s_s,
            x_a, y_c_s,
            x_a, n_3,
            x_a, n_4,
            x_a, n_5
    )

    plt.xlabel(u'Number of vertexes')
    plt.ylabel(u'Result')

    plt.legend( (line_1, line_2, line_3, line_4, line_5, line_6, line_7),
                (u'Ear triangulation | Coloring',
                 u'Ear triangulation | Greedy',
                 u'Seidel triangulation | Greedy',
                 u'Convex decomposition |  Greedy',
                 u'y = x / 3 ',
                 u'y = x / 4 ',
                 u'y = x / 5',
                 ),
                loc='best'
                )

    plt.grid()
    plt.savefig('graph.png', format='png')

run()
