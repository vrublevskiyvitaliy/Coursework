import ioclass
from ear_trianguation import EarTriangulation
from polygon import Polygon
from ioclass import filename
from SegmentTree import SegmentTree


def convex_art_gallery_problem(interface, points=None, show_decomposition=True):
    if points is None:
        points = ioclass.read_from_file(filename)

    res = convex_partition(points)

    if show_decomposition:
        for i in range(len(res)):
            poly = res[i]
            interface.draw_polygon_as_list_of_points(poly, 'red', 1.0)


    size = len(points)
    segment_tree = SegmentTree(0, size - 1)
    polygons_per_point = dict()
    for polygon in res:
        polygon_int_names = list()
        for p in polygon:
            polygon_int_names.append(int(p.name))

        for p in polygon:
            p_key = int(p.name)
            if p_key not in polygons_per_point.keys():
                polygons_per_point[p_key] = list()

            polygons_per_point[p_key].append(polygon_int_names)

    for point in polygons_per_point:
        segment_tree.add(int(point), int(point), len(polygons_per_point[point]))

    current_max = size
    start = 0
    end = size - 1
    current_max = segment_tree.query_max(start, end)
    current_max_index = segment_tree.query_max_index(start, end)
    res = []
    while current_max > 0:
        res.append(points[current_max_index])
        for polygon in polygons_per_point[current_max_index]:
            for p in polygon:
                segment_tree.add(p, p, -1)

        current_max = segment_tree.query_max(start, end)
        current_max_index = segment_tree.query_max_index(start, end)

    interface.draw_result_points(res)
    interface.set_result(len(res))


def is_reflex(p1, p2, p3):
    tmp = (p3.y - p1.y) * (p2.x - p1.x) - (p3.x - p1.x) * (p2.y - p1.y)
    if tmp < 0:
        return 1
    else:
        return 0


def is_convex(p1, p2, p3):
    tmp = (p3.y - p1.y) * (p2.x - p1.x) - (p3.x - p1.x) * (p2.y - p1.y)
    if tmp >= 0:
        return 1
    else:
        return 0


def convex_partition(points):
    num_reflex = 0

    # triangles
    for i11 in range(len(points)):
        if i11 == 0:
            i12 = len(points) - 1
        else:
            i12 = i11 - 1

        if i11 == (len(points) - 1):
            i13 = 0
        else:
            i13 = i11 + 1
        if is_reflex(points[i12], points[i11], points[i13]):
            num_reflex = 1
            break

    if num_reflex == 0:
        return [points]

    poly = Polygon()
    poly.set_points(points)

    linked_list = poly.get_linked_list()
    headnode = linked_list[0]
    size = len(points)

    # Create a Triangulation object from the linked list:
    t1 = EarTriangulation(headnode, size)

    triangles = t1.triangulate()
    triangles_points = list()

    for tr in triangles:
        p1, p2, p3 = tr[0], tr[1], tr[2]

        p1 = int(p1)
        p2 = int(p2)
        p3 = int(p3)

        p1 = points[p1]
        p2 = points[p2]
        p3 = points[p3]

        p1 = p1.get_clone()
        p2 = p2.get_clone()
        p3 = p3.get_clone()

        triangles_points.append([p1, p2, p3])

    loop_counter = len(triangles_points)
    #for iter1 in range(len(triangles_points)):
    iter1 = 0
    while iter1 < loop_counter:
        poly1 = triangles_points[iter1]
        i11 = 0
        loop_counter_poly1 = len(poly1)
        while i11 < loop_counter_poly1:
            d1 = poly1[i11]
            i12 = (i11 + 1) % len(poly1)
            d2 = poly1[i12]

            isdiagonal = False
            for iter2 in range(iter1, len(triangles_points)):
                if iter1 == iter2:
                    continue
                poly2 = triangles_points[iter2]

                for i21 in range(len(poly2)):
                    if d2.x != poly2[i21].x or d2.y != poly2[i21].y:
                        continue
                    i22 = (i21 + 1) % len(poly2)
                    if d1.x != poly2[i22].x or d1.y != poly2[i22].y:
                        continue
                    isdiagonal = True
                    break

                if isdiagonal:
                    break

            if not isdiagonal:
                i11 += 1
                continue

            p2 = poly1[i11]
            if i11 == 0:
                i13 = len(poly1) - 1
            else:
                i13 = i11 - 1
            p1 = poly1[i13]

            if i22 == (len(poly2) - 1):
                i23 = 0
            else:
                i23 = i22 + 1
            p3 = poly2[i23]

            if not is_convex(p1, p2, p3):
                i11 += 1
                continue

            p2 = poly1[i12]
            if i12 == (len(poly1) - 1):
                i13 = 0
            else:
                i13 = i12 + 1

            p3 = poly1[i13]
            if i21 == 0:
                i23 = len(poly2) - 1
            else:
                i23 = i21 - 1
            p1 = poly2[i23]

            if not is_convex(p1, p2, p3):
                i11 += 1
                continue

            newpoly = list()  # .Init(poly1->GetNumPoints()+poly2->GetNumPoints()-2);
            for i in range(len(poly1) + len(poly2) - 2):
                newpoly.append(0)
            k = 0
            j = i12
            while j != i11:
                newpoly[k] = poly1[j].get_clone()
                k += 1
                j = (j + 1) % len(poly1)

            j = i22
            while j != i21:
                newpoly[k] = poly2[j].get_clone()
                k += 1
                j = (j + 1) % len(poly2)

            triangles_points.pop(iter2)
            triangles_points[iter1] = newpoly
            poly1 = newpoly
            # *iter1 = newpoly;
            #poly1 = &(*iter1);
            i11 = 0
            loop_counter_poly1 = len(newpoly)
            loop_counter = len(triangles_points)
            print("one more split")
            continue
        iter1 += 1

    break_point = 1
    return triangles_points

'''
int TPPLPartition::ConvexPartition_HM(TPPLPoly *poly, list<TPPLPoly> *parts) {
	list<TPPLPoly> triangles;
	list<TPPLPoly>::iterator iter1,iter2;
	TPPLPoly *poly1,*poly2;
	TPPLPoly newpoly;
	TPPLPoint d1,d2,p1,p2,p3;
	long i11,i12,i21,i22,i13,i23,j,k;
	bool isdiagonal;
	long numreflex;

	//check if the poly is already convex
	numreflex = 0;
	for(i11=0;i11<poly->GetNumPoints();i11++) {
		if(i11==0) i12 = poly->GetNumPoints()-1;
		else i12=i11-1;
		if(i11==(poly->GetNumPoints()-1)) i13=0;
		else i13=i11+1;
		if(IsReflex(poly->GetPoint(i12),poly->GetPoint(i11),poly->GetPoint(i13))) {
			numreflex = 1;
			break;
		}
	}
	if(numreflex == 0) {
		parts->push_back(*poly);
		return 1;
	}

	if(!Triangulate_EC(poly,&triangles)) return 0;

	for(iter1 = triangles.begin(); iter1 != triangles.end(); iter1++) {
		poly1 = &(*iter1);
		for(i11=0;i11<poly1->GetNumPoints();i11++) {
			d1 = poly1->GetPoint(i11);
			i12 = (i11+1)%(poly1->GetNumPoints());
			d2 = poly1->GetPoint(i12);

			isdiagonal = false;
			for(iter2 = iter1; iter2 != triangles.end(); iter2++) {
				if(iter1 == iter2) continue;
				poly2 = &(*iter2);

				for(i21=0;i21<poly2->GetNumPoints();i21++) {
					if((d2.x != poly2->GetPoint(i21).x)||(d2.y != poly2->GetPoint(i21).y)) continue;
					i22 = (i21+1)%(poly2->GetNumPoints());
					if((d1.x != poly2->GetPoint(i22).x)||(d1.y != poly2->GetPoint(i22).y)) continue;
					isdiagonal = true;
					break;
				}
				if(isdiagonal) break;
			}

			if(!isdiagonal) continue;

			p2 = poly1->GetPoint(i11);
			if(i11 == 0) i13 = poly1->GetNumPoints()-1;
			else i13 = i11-1;
			p1 = poly1->GetPoint(i13);
			if(i22 == (poly2->GetNumPoints()-1)) i23 = 0;
			else i23 = i22+1;
			p3 = poly2->GetPoint(i23);

			if(!IsConvex(p1,p2,p3)) continue;

			p2 = poly1->GetPoint(i12);
			if(i12 == (poly1->GetNumPoints()-1)) i13 = 0;
			else i13 = i12+1;
			p3 = poly1->GetPoint(i13);
			if(i21 == 0) i23 = poly2->GetNumPoints()-1;
			else i23 = i21-1;
			p1 = poly2->GetPoint(i23);

			if(!IsConvex(p1,p2,p3)) continue;

			newpoly.Init(poly1->GetNumPoints()+poly2->GetNumPoints()-2);
			k = 0;
			for(j=i12;j!=i11;j=(j+1)%(poly1->GetNumPoints())) {
				newpoly[k] = poly1->GetPoint(j);
				k++;
			}
			for(j=i22;j!=i21;j=(j+1)%(poly2->GetNumPoints())) {
				newpoly[k] = poly2->GetPoint(j);
				k++;
			}

			triangles.erase(iter2);
			*iter1 = newpoly;
			poly1 = &(*iter1);
			i11 = -1;

			continue;
		}
	}

	for(iter1 = triangles.begin(); iter1 != triangles.end(); iter1++) {
		parts->push_back(*iter1);
	}

	return 1;
}

'''