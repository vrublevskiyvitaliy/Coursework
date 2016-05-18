from generator import get_random_polygon
from gui import GUI
import ear_art_gallery_problem
import ear_triang_segment_tree
import convex
import seidel_art_gallery_segment


def get_stat():
    interface = GUI()
    f = open('stat12.txt', 'w')
    for i in range(781, 1000):
        points = get_random_polygon(i)
        interface.set_points(points)
        ear_color_res = ear_art_gallery_problem.art_gallery_problem(interface, points, False)
        ear_segment_res = ear_triang_segment_tree.ear_segment_art_gallery_problem(interface, points, False)
        convex_res = convex.convex_art_gallery_problem(interface, points, False)
        seidel_res = seidel_art_gallery_segment.seidel_segment_art_gallery_problem(interface, points, False)
        f.write(str(len(points)) + ' ' + str(ear_color_res) + ' ' + str(ear_segment_res)
                + ' ' + str(convex_res) + ' ' + str(seidel_res) + '\n')
        print('*****')
        print(i)
        print(len(points))
        print(ear_color_res)
        print(ear_segment_res)
        print(convex_res)
        print(seidel_res)
        print('*****')
        # print(i)
        # print(len(points))
    f.close()


get_stat()