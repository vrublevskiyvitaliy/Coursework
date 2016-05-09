TPPL_CCW = 1
TPPL_CW = -1
TPPL_VERTEXTYPE_REGULAR = 0
TPPL_VERTEXTYPE_START = 1
TPPL_VERTEXTYPE_END = 2
TPPL_VERTEXTYPE_SPLIT = 3
TPPL_VERTEXTYPE_MERGE = 4

class TPPLPoint():

    def __init__(self):
        self.x = None
        self.y = None

    def __add__(self, p):
        r = TPPLPoint()
        r.x = self.x + p.x
        r.y = self.y + p.y
        return r

    def __sub__(self, p):
        r = TPPLPoint()
        r.x = self.x - p.x
        r.y = self.y - p.y
        return r

    def __mul__(self, f):
        r = TPPLPoint()
        r.x = self.x*f
        r.y = self.y*f
        return r

    def __divmod__(self, f):
        r = TPPLPoint()
        r.x = self.x/f
        r.y = self.y/f
        return r

    def __eq__(self, p):
        if self.x == p.x and self.y == p.y:
            return True
        else:
            return False

    def __ne__(self, p):
        if self.x == p.x and self.y == p.y:
            return False
        else:
            return True


class MonotoneVertex():
    def __init__(self):
        self.p = TPPLPoint()
        self.previous = None
        self.nex = None


class TPPLPoly():
    def __init__(self):
        self.points = list()

    def clear(self):
        self.points = list()

    def number_of_points(self):
        return len(self.points)

    def locate_memory(self, n):
        self.points = list()
        for i in range(n):
            self.points.append(0)

    def triangle(self, p1, p2, p3):
        self.locate_memory(3)
        self.points[0] = p1
        self.points[1] = p2
        self.points[2] = p3

    def copy_from_TPPLPoly(self, poly):
        if not isinstance(poly, TPPLPoly):
            raise Exception("Wrong type!")
        self.points = list()
        self.locate_memory(poly.number_of_points())
        for i in range(poly.number_of_points()):
            p = TPPLPoint()
            p.x = poly.points[i].x
            p.y = poly.points[i].y
            self.points[i] = p

    def get_orientation(self):
        area = 0
        for i1 in range(self.number_of_points()):
            i2 = i1+1
            if i2 == self.number_of_points():
                i2 = 0
            area += self.points[i1].x * self.points[i2].y - self.points[i1].y * self.points[i2].x

        if area > 0:
            return TPPL_CCW
        if area < 0:
            return TPPL_CW
        return 0

    def invert(self):
        inv_points = list()

        numpoints = self.number_of_points()
        for i in range(numpoints):
            inv_points.append(self.points[numpoints-i-1])
        self.points = inv_points

    def set_orientation(self, orientation):
        poly_orientation = self.get_orientation()
        if poly_orientation != 0 and poly_orientation != orientation:
            self.invert()


class ScanLineEdge():
    def __init__(self):
        self.index = None
        self.p1 = TPPLPoint()
        self.p2 = TPPLPoint()
    # determines if the edge is to the left of another edge

    def is_less(self, other):
        if other.p1.y == other.p2.y:
            if self.p1.y == self.p2.y:
                if self.p1.y < other.p1.y:
                    return True
                else:
                    return False
            if is_convex(self.p1, self.p2, other.p1):
                return True
            else:
                return False

        elif self.p1.y == self.p2.y:
            if is_convex(other.p1, other.p2, self.p1):
                return False
            else:
                return True

        elif self.p1.y < other.p1.y:
            if is_convex(other.p1, other.p2, self.p1):
                return False
            else:
                return True
        else:
            if is_convex(self.p1, self.p2, other.p1):
                return True
            else:
                return False

    def is_convex(self, p1, p2, p3):
        tmp = (p3.y - p1.y) * (p2.x - p1.x) - (p3.x - p1.x) * (p2.y - p1.y)
        if tmp > 0:
            return 1
        else:
            return 0


def below(p1, p2):
    if p1.y < p2.y:
        return True
    elif p1.y == p2.y and p1.x < p2.x:
        return True
    return False


def is_convex(p1, p2, p3):
    tmp = (p3.y - p1.y) * (p2.x - p1.x) - (p3.x - p1.x) * (p2.y - p1.y)
    if tmp > 0:
        return 1
    else:
        return 0


def vertex_sorter(x, y):
    vertices = vertex_sorter.array

    if vertices[x].p.y == vertices[y].p.y and vertices[x].p.x == vertices[y].p.x:
        return 0

    if vertices[x].p.y > vertices[y].p.y:
        return 1
    elif vertices[x].p.y == vertices[y].p.y and vertices[x].p.x > vertices[y].p.x:
        return 1

    return -1


'''
int TPPLPartition::Triangulate_MONO(list<TPPLPoly> *inpolys, list<TPPLPoly> *triangles) {
	list<TPPLPoly> monotone;
	list<TPPLPoly>::iterator iter;

	if(!MonotonePartition(inpolys,&monotone)) return 0;
	for(iter = monotone.begin(); iter!=monotone.end();iter++) {
		if(!TriangulateMonotone(&(*iter),triangles)) return 0;
	}
	return 1;
}

'''
def Triangulate_MONO(inpolys, triangles):
    monotone = list()

    if !monotone_partition(inpolys, monotone):
        return 0
    '''
    for(iter = monotone.begin(); iter!=monotone.end();iter++) {
		if(!TriangulateMonotone(&(*iter),triangles)) return 0;
	}'''
    return 1


# triangulates a set of polygons by first partitioning them into monotone polygons
# O(n*log(n)) time complexity, O(n) space complexity
# the algorithm used here is outlined in the book
# "Computational Geometry: Algorithms and Applications"
# by Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars
def monotone_partition(inpolys, monotonePolys):
    if not isinstance(inpolys, TPPLPoly):
        raise Exception("Error!")

    # list<TPPLPoly>::iterator iter;
    # #MonotoneVertex *vertices;
    vertices = list()
    # long i,numvertices,vindex,vindex2,newnumvertices,maxnumvertices;
    # long polystartindex, polyendindex
    # TPPLPoly *poly;
    poly = list()
    # MonotoneVertex *v,*v2,*vprev,*vnext;
    #  ScanLineEdge newedge;
    newedge = ScanLineEdge()
    error = False

    # numvertices = 0
    # for(iter = inpolys->begin(); iter != inpolys->end(); iter++) {
    # numvertices += iter->GetNumPoints();
    numvertices = inpolys.number_of_points()

    maxnumvertices = numvertices * 3
    for i in range(maxnumvertices):
        vertices.append(MonotoneVertex())
    #vertices = list(range(maxnumvertices))
    newnumvertices = numvertices
    polystartindex = 0

    poly = inpolys
    polyendindex = polystartindex + poly.number_of_points() - 1
    for i in range(poly.number_of_points()):
        vertices[i + polystartindex].p = poly.points[i]
        if i == 0:
            vertices[i + polystartindex].previous = polyendindex
        else:
            vertices[i + polystartindex].previous = i + polystartindex - 1
        if i == (poly.number_of_points() - 1):
            vertices[i + polystartindex].next = polystartindex
        else:
            vertices[i + polystartindex].next = i + polystartindex + 1
        polystartindex = polyendindex + 1

    t = 0

    # construct the priority queue
    # long *priority = new long [numvertices];
    priority = list(range(numvertices))
    vertex_sorter.array = vertices
    priority = sorted(priority, cmp=vertex_sorter)
    # for(i=0;i<numvertices;i++) priority[i] = i;
    # std::sort(priority,&(priority[numvertices]),VertexSorter(vertices));

    # determine vertex types
    vertextypes = list()
    for i in range(maxnumvertices):
        vertextypes.append(0)

    for i in range(numvertices):
        v = vertices[i]
        vprev = vertices[v.previous]
        vnext = vertices[v.next]
        if below(vprev.p, v.p) and below(vnext.p, v.p):
            if is_convex(vnext.p, vprev.p, v.p):
                vertextypes[i] = TPPL_VERTEXTYPE_START
            else:
                vertextypes[i] = TPPL_VERTEXTYPE_SPLIT
        elif below(v.p, vprev.p) and below(v.p, vnext.p):
            if is_convex(vnext.p, vprev.p, v.p):
                vertextypes[i] = TPPL_VERTEXTYPE_END
            else:
                vertextypes[i] = TPPL_VERTEXTYPE_MERGE
        else:
            vertextypes[i] = TPPL_VERTEXTYPE_REGULAR

    # helpers
    # long *helpers = new long[maxnumvertices];
    helpers = list(range(maxnumvertices))
    # binary search tree that holds edges intersecting the scanline
    # note that while set doesn't actually have to be implemented as a tree
    # complexity requirements for operations are the same as for the balanced binary search tree
    edgeTree = set()
    edgeTreeList = list()

    # set<ScanLineEdge> edgeTree;

    # store iterators to the edge tree elements
    # this makes deleting existing edges much faster
    # set<ScanLineEdge>::iterator *edgeTreeIterators,edgeIter;
    # edgeIter = None
    edgeTreeIterators = list()
    for i in range(numvertices):
        edgeTreeIterators.append(0)
    # edgeTreeIterators
	# edgeTreeIterators = new set<ScanLineEdge>::iterator[maxnumvertices];
	# pair<set<ScanLineEdge>::iterator,bool> edgeTreeRet;
	# for(i = 0; i<numvertices; i++) edgeTreeIterators[i] = edgeTree.end();


    # for each vertex
    for i in range(numvertices):
        vindex = priority[i]
        v = vertices[vindex]
        vindex2 = vindex
        v2 = v

        # depending on the vertex type, do the appropriate action
        # comments in the following sections are copied from "Computational Geometry: Algorithms and Applications"
        if vertextypes[vindex] == TPPL_VERTEXTYPE_START:
            # Insert ei in T and set helper(ei) to vi.
            newedge.p1 = v.p
            newedge.p2 = vertices[v.next].p
            newedge.index = vindex
            prevSetNumber = len(edgeTree)
            edgeTree.add(newedge)
            if prevSetNumber != len(edgeTree):

                edgeTreeIterators[vindex] = prevSetNumber # index of in array
            # edgeTreeRet = edgeTree.insert(newedge)
            edgeTreeIterators[vindex] = edgeTreeRet.first
            helpers[vindex] = vindex


			case TPPL_VERTEXTYPE_END:
				//if helper(ei-1) is a merge vertex
				if(vertextypes[helpers[v->previous]]==TPPL_VERTEXTYPE_MERGE) {
					//Insert the diagonal connecting vi to helper(ei-1) in D.
					AddDiagonal(vertices,&newnumvertices,vindex,helpers[v->previous],
						vertextypes, edgeTreeIterators, &edgeTree, helpers);
				}
				//Delete ei-1 from T
				edgeTree.erase(edgeTreeIterators[v->previous]);
				break;

			case TPPL_VERTEXTYPE_SPLIT:
				//Search in T to find the edge e j directly left of vi.
				newedge.p1 = v->p;
				newedge.p2 = v->p;
				edgeIter = edgeTree.lower_bound(newedge);
				if(edgeIter == edgeTree.begin()) {
					error = true;
					break;
				}
				edgeIter--;
				//Insert the diagonal connecting vi to helper(ej) in D.
				AddDiagonal(vertices,&newnumvertices,vindex,helpers[edgeIter->index],
					vertextypes, edgeTreeIterators, &edgeTree, helpers);
				vindex2 = newnumvertices-2;
				v2 = &(vertices[vindex2]);
				//helper(e j)�vi
				helpers[edgeIter->index] = vindex;
				//Insert ei in T and set helper(ei) to vi.
				newedge.p1 = v2->p;
				newedge.p2 = vertices[v2->next].p;
				newedge.index = vindex2;
				edgeTreeRet = edgeTree.insert(newedge);
				edgeTreeIterators[vindex2] = edgeTreeRet.first;
				helpers[vindex2] = vindex2;
				break;

			case TPPL_VERTEXTYPE_MERGE:
				//if helper(ei-1) is a merge vertex
				if(vertextypes[helpers[v->previous]]==TPPL_VERTEXTYPE_MERGE) {
					//Insert the diagonal connecting vi to helper(ei-1) in D.
					AddDiagonal(vertices,&newnumvertices,vindex,helpers[v->previous],
						vertextypes, edgeTreeIterators, &edgeTree, helpers);
					vindex2 = newnumvertices-2;
					v2 = &(vertices[vindex2]);
				}
				//Delete ei-1 from T.
				edgeTree.erase(edgeTreeIterators[v->previous]);
				//Search in T to find the edge e j directly left of vi.
				newedge.p1 = v->p;
				newedge.p2 = v->p;
				edgeIter = edgeTree.lower_bound(newedge);
				if(edgeIter == edgeTree.begin()) {
					error = true;
					break;
				}
				edgeIter--;
				//if helper(ej) is a merge vertex
				if(vertextypes[helpers[edgeIter->index]]==TPPL_VERTEXTYPE_MERGE) {
					//Insert the diagonal connecting vi to helper(e j) in D.
					AddDiagonal(vertices,&newnumvertices,vindex2,helpers[edgeIter->index],
						vertextypes, edgeTreeIterators, &edgeTree, helpers);
				}
				//helper(e j)�vi
				helpers[edgeIter->index] = vindex2;
				break;

			case TPPL_VERTEXTYPE_REGULAR:
				//if the interior of P lies to the right of vi
				if(Below(v->p,vertices[v->previous].p)) {
					//if helper(ei-1) is a merge vertex
					if(vertextypes[helpers[v->previous]]==TPPL_VERTEXTYPE_MERGE) {
						//Insert the diagonal connecting vi to helper(ei-1) in D.
						AddDiagonal(vertices,&newnumvertices,vindex,helpers[v->previous],
							vertextypes, edgeTreeIterators, &edgeTree, helpers);
						vindex2 = newnumvertices-2;
						v2 = &(vertices[vindex2]);
					}
					//Delete ei-1 from T.
					edgeTree.erase(edgeTreeIterators[v->previous]);
					//Insert ei in T and set helper(ei) to vi.
					newedge.p1 = v2->p;
					newedge.p2 = vertices[v2->next].p;
					newedge.index = vindex2;
					edgeTreeRet = edgeTree.insert(newedge);
					edgeTreeIterators[vindex2] = edgeTreeRet.first;
					helpers[vindex2] = vindex;
				} else {
					//Search in T to find the edge ej directly left of vi.
					newedge.p1 = v->p;
					newedge.p2 = v->p;
					edgeIter = edgeTree.lower_bound(newedge);
					if(edgeIter == edgeTree.begin()) {
						error = true;
						break;
					}
					edgeIter--;
					//if helper(ej) is a merge vertex
					if(vertextypes[helpers[edgeIter->index]]==TPPL_VERTEXTYPE_MERGE) {
						//Insert the diagonal connecting vi to helper(e j) in D.
						AddDiagonal(vertices,&newnumvertices,vindex,helpers[edgeIter->index],
							vertextypes, edgeTreeIterators, &edgeTree, helpers);
					}
					//helper(e j)�vi
					helpers[edgeIter->index] = vindex;
				}
				break;
		}

		if(error) break;
	}


'''

//triangulates a set of polygons by first partitioning them into monotone polygons
//O(n*log(n)) time complexity, O(n) space complexity
//the algorithm used here is outlined in the book
//"Computational Geometry: Algorithms and Applications"
//by Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars
int TPPLPartition::MonotonePartition(list<TPPLPoly> *inpolys, list<TPPLPoly> *monotonePolys) {
	list<TPPLPoly>::iterator iter;
	MonotoneVertex *vertices;
	long i,numvertices,vindex,vindex2,newnumvertices,maxnumvertices;
	long polystartindex, polyendindex;
	TPPLPoly *poly;
	MonotoneVertex *v,*v2,*vprev,*vnext;
	ScanLineEdge newedge;
	bool error = false;

	numvertices = 0;
	for(iter = inpolys->begin(); iter != inpolys->end(); iter++) {
		numvertices += iter->GetNumPoints();
	}

	maxnumvertices = numvertices*3;
	vertices = new MonotoneVertex[maxnumvertices];
	newnumvertices = numvertices;

	polystartindex = 0;
	for(iter = inpolys->begin(); iter != inpolys->end(); iter++) {
		poly = &(*iter);
		polyendindex = polystartindex + poly->GetNumPoints()-1;
		for(i=0;i<poly->GetNumPoints();i++) {
			vertices[i+polystartindex].p = poly->GetPoint(i);
			if(i==0) vertices[i+polystartindex].previous = polyendindex;
			else vertices[i+polystartindex].previous = i+polystartindex-1;
			if(i==(poly->GetNumPoints()-1)) vertices[i+polystartindex].next = polystartindex;
			else vertices[i+polystartindex].next = i+polystartindex+1;
		}
		polystartindex = polyendindex+1;
	}

	//construct the priority queue
	long *priority = new long [numvertices];
	for(i=0;i<numvertices;i++) priority[i] = i;
	std::sort(priority,&(priority[numvertices]),VertexSorter(vertices));

	//determine vertex types
	char *vertextypes = new char[maxnumvertices];
	for(i=0;i<numvertices;i++) {
		v = &(vertices[i]);
		vprev = &(vertices[v->previous]);
		vnext = &(vertices[v->next]);

		if(Below(vprev->p,v->p)&&Below(vnext->p,v->p)) {
			if(IsConvex(vnext->p,vprev->p,v->p)) {
				vertextypes[i] = TPPL_VERTEXTYPE_START;
			} else {
				vertextypes[i] = TPPL_VERTEXTYPE_SPLIT;
			}
		} else if(Below(v->p,vprev->p)&&Below(v->p,vnext->p)) {
			if(IsConvex(vnext->p,vprev->p,v->p))
			{
				vertextypes[i] = TPPL_VERTEXTYPE_END;
			} else {
				vertextypes[i] = TPPL_VERTEXTYPE_MERGE;
			}
		} else {
			vertextypes[i] = TPPL_VERTEXTYPE_REGULAR;
		}
	}

	//helpers
	long *helpers = new long[maxnumvertices];

	//binary search tree that holds edges intersecting the scanline
	//note that while set doesn't actually have to be implemented as a tree
	//complexity requirements for operations are the same as for the balanced binary search tree
	set<ScanLineEdge> edgeTree;
	//store iterators to the edge tree elements
	//this makes deleting existing edges much faster
	set<ScanLineEdge>::iterator *edgeTreeIterators,edgeIter;
	edgeTreeIterators = new set<ScanLineEdge>::iterator[maxnumvertices];
	pair<set<ScanLineEdge>::iterator,bool> edgeTreeRet;
	for(i = 0; i<numvertices; i++) edgeTreeIterators[i] = edgeTree.end();

	//for each vertex
	for(i=0;i<numvertices;i++) {
		vindex = priority[i];
		v = &(vertices[vindex]);
		vindex2 = vindex;
		v2 = v;

		//depending on the vertex type, do the appropriate action
		//comments in the following sections are copied from "Computational Geometry: Algorithms and Applications"
		switch(vertextypes[vindex]) {
			case TPPL_VERTEXTYPE_START:
				//Insert ei in T and set helper(ei) to vi.
				newedge.p1 = v->p;
				newedge.p2 = vertices[v->next].p;
				newedge.index = vindex;
				edgeTreeRet = edgeTree.insert(newedge);
				edgeTreeIterators[vindex] = edgeTreeRet.first;
				helpers[vindex] = vindex;
				break;

			case TPPL_VERTEXTYPE_END:
				//if helper(ei-1) is a merge vertex
				if(vertextypes[helpers[v->previous]]==TPPL_VERTEXTYPE_MERGE) {
					//Insert the diagonal connecting vi to helper(ei-1) in D.
					AddDiagonal(vertices,&newnumvertices,vindex,helpers[v->previous],
						vertextypes, edgeTreeIterators, &edgeTree, helpers);
				}
				//Delete ei-1 from T
				edgeTree.erase(edgeTreeIterators[v->previous]);
				break;

			case TPPL_VERTEXTYPE_SPLIT:
				//Search in T to find the edge e j directly left of vi.
				newedge.p1 = v->p;
				newedge.p2 = v->p;
				edgeIter = edgeTree.lower_bound(newedge);
				if(edgeIter == edgeTree.begin()) {
					error = true;
					break;
				}
				edgeIter--;
				//Insert the diagonal connecting vi to helper(ej) in D.
				AddDiagonal(vertices,&newnumvertices,vindex,helpers[edgeIter->index],
					vertextypes, edgeTreeIterators, &edgeTree, helpers);
				vindex2 = newnumvertices-2;
				v2 = &(vertices[vindex2]);
				//helper(e j)�vi
				helpers[edgeIter->index] = vindex;
				//Insert ei in T and set helper(ei) to vi.
				newedge.p1 = v2->p;
				newedge.p2 = vertices[v2->next].p;
				newedge.index = vindex2;
				edgeTreeRet = edgeTree.insert(newedge);
				edgeTreeIterators[vindex2] = edgeTreeRet.first;
				helpers[vindex2] = vindex2;
				break;

			case TPPL_VERTEXTYPE_MERGE:
				//if helper(ei-1) is a merge vertex
				if(vertextypes[helpers[v->previous]]==TPPL_VERTEXTYPE_MERGE) {
					//Insert the diagonal connecting vi to helper(ei-1) in D.
					AddDiagonal(vertices,&newnumvertices,vindex,helpers[v->previous],
						vertextypes, edgeTreeIterators, &edgeTree, helpers);
					vindex2 = newnumvertices-2;
					v2 = &(vertices[vindex2]);
				}
				//Delete ei-1 from T.
				edgeTree.erase(edgeTreeIterators[v->previous]);
				//Search in T to find the edge e j directly left of vi.
				newedge.p1 = v->p;
				newedge.p2 = v->p;
				edgeIter = edgeTree.lower_bound(newedge);
				if(edgeIter == edgeTree.begin()) {
					error = true;
					break;
				}
				edgeIter--;
				//if helper(ej) is a merge vertex
				if(vertextypes[helpers[edgeIter->index]]==TPPL_VERTEXTYPE_MERGE) {
					//Insert the diagonal connecting vi to helper(e j) in D.
					AddDiagonal(vertices,&newnumvertices,vindex2,helpers[edgeIter->index],
						vertextypes, edgeTreeIterators, &edgeTree, helpers);
				}
				//helper(e j)�vi
				helpers[edgeIter->index] = vindex2;
				break;

			case TPPL_VERTEXTYPE_REGULAR:
				//if the interior of P lies to the right of vi
				if(Below(v->p,vertices[v->previous].p)) {
					//if helper(ei-1) is a merge vertex
					if(vertextypes[helpers[v->previous]]==TPPL_VERTEXTYPE_MERGE) {
						//Insert the diagonal connecting vi to helper(ei-1) in D.
						AddDiagonal(vertices,&newnumvertices,vindex,helpers[v->previous],
							vertextypes, edgeTreeIterators, &edgeTree, helpers);
						vindex2 = newnumvertices-2;
						v2 = &(vertices[vindex2]);
					}
					//Delete ei-1 from T.
					edgeTree.erase(edgeTreeIterators[v->previous]);
					//Insert ei in T and set helper(ei) to vi.
					newedge.p1 = v2->p;
					newedge.p2 = vertices[v2->next].p;
					newedge.index = vindex2;
					edgeTreeRet = edgeTree.insert(newedge);
					edgeTreeIterators[vindex2] = edgeTreeRet.first;
					helpers[vindex2] = vindex;
				} else {
					//Search in T to find the edge ej directly left of vi.
					newedge.p1 = v->p;
					newedge.p2 = v->p;
					edgeIter = edgeTree.lower_bound(newedge);
					if(edgeIter == edgeTree.begin()) {
						error = true;
						break;
					}
					edgeIter--;
					//if helper(ej) is a merge vertex
					if(vertextypes[helpers[edgeIter->index]]==TPPL_VERTEXTYPE_MERGE) {
						//Insert the diagonal connecting vi to helper(e j) in D.
						AddDiagonal(vertices,&newnumvertices,vindex,helpers[edgeIter->index],
							vertextypes, edgeTreeIterators, &edgeTree, helpers);
					}
					//helper(e j)�vi
					helpers[edgeIter->index] = vindex;
				}
				break;
		}

		if(error) break;
	}

	char *used = new char[newnumvertices];
	memset(used,0,newnumvertices*sizeof(char));

	if(!error) {
		//return result
		long size;
		TPPLPoly mpoly;
		for(i=0;i<newnumvertices;i++) {
			if(used[i]) continue;
			v = &(vertices[i]);
			vnext = &(vertices[v->next]);
			size = 1;
			while(vnext!=v) {
				vnext = &(vertices[vnext->next]);
				size++;
			}
			mpoly.Init(size);
			v = &(vertices[i]);
			mpoly[0] = v->p;
			vnext = &(vertices[v->next]);
			size = 1;
			used[i] = 1;
			used[v->next] = 1;
			while(vnext!=v) {
				mpoly[size] = vnext->p;
				used[vnext->next] = 1;
				vnext = &(vertices[vnext->next]);
				size++;
			}
			monotonePolys->push_back(mpoly);
		}
	}

	//cleanup
	delete [] vertices;
	delete [] priority;
	delete [] vertextypes;
	delete [] edgeTreeIterators;
	delete [] helpers;
	delete [] used;

	if(error) {
		return 0;
	} else {
		return 1;
	}
}
'''