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
            max(res_dict[n_vertex]['ears_coloring'])# / len(res_dict[n_vertex]['ears_coloring'])
        res_dict[n_vertex]['e_s_n'] = \
            max(res_dict[n_vertex]['ears_segment']) #/ len(res_dict[n_vertex]['ears_segment'])
        res_dict[n_vertex]['s_s_n'] = \
            max(res_dict[n_vertex]['seidel_segment']) #/ len(res_dict[n_vertex]['seidel_segment'])
        res_dict[n_vertex]['c_s_n'] = \
            max(res_dict[n_vertex]['convex_segment']) #/ len(res_dict[n_vertex]['convex_segment'])



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
                loc = 'best'
                )


    plt.grid()
    plt.savefig('one_max.png', format = 'png')

run()


'''



# Значения по оси X

X = [20.0, 40.0, 60.0, 80.0, 100.0]

# Набор значений по оси Y

Y_10 = [0.97252, 0.94238, 0.89927, 0.85197, 0.79784]
Y_20 = [0.96864, 0.93518, 0.89113, 0.84344, 0.78934]
Y_30 = [0.96395, 0.92770, 0.88278, 0.83473, 0.78075]

# Строим диаграмму

# Задаем исходные данные для каждой линии диаграммы, внешний вид линий и маркеров.
# Функция plot() возвращает кортеж ссылок на объекты класса matplotlib.lines.Line2D

line_10, line_20, line_30 = plt.plot(X, Y_10, 'bD:', X, Y_20, 'r^:', X, Y_30, 'go:')

# Задаем интервалы значений по осям X и Y

plt.axis([15.0, 105.0, 0.75, 1.0])

# Задаем заголовок диаграммы

#plt.title(u'Зависимость плотности водных растворов этилового спирта от температуры')

# Задаем подписи к осям X и Y

#plt.xlabel(u'Массовая доля этилового спирта, %')
#plt.ylabel(u'Плотность, г/мл')

# Задаем исходные данные для легенды и ее размещение

plt.legend( (line_10, line_20, line_30), (u'Температура 10 \u00b0C', u'Температура 20 \u00b0C', u'Температура 30 \u00b0C'), loc = 'best')

# Включаем сетку

plt.grid()

# Сохраняем построенную диаграмму в файл

# Задаем имя файла и его тип

plt.savefig('spirit.png', format = 'png')

'''