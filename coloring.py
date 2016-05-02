
class Coloring:
    def __init__(self):
        self.polygon = None
        self.triangles = None
        self.dual_vertexes = None
        self.dual_edges = None

    def set_triangulation(self, p, tr):
        self.polygon = p
        self.triangles = tr
        self.create_dual_graph_optimal()
        #self.create_dual_graph()

    def create_dual_graph(self):
        d_vertexes = {i: self.triangles[i] for i in range(0, len(self.triangles))}
        d_edges = {}
        for i in range(0, len(self.triangles)):
            for j in range(i+1, len(self.triangles)):
                if len(list(set(self.triangles[i]) & set(self.triangles[j]))) > 1:
                    if i in d_edges and j not in d_edges[i] and i is not j:
                        d_edges[i].append(j)
                    elif i not in d_edges and i is not j:
                        d_edges[i] = [j]

                    if j in d_edges and i not in d_edges[j] and i is not j:
                        d_edges[j].append(i)
                    elif j not in d_edges and i is not j:
                        d_edges[j] = [i]
        self.dual_vertexes = d_vertexes
        self.dual_edges = d_edges

    def get_tr_code(self, tr):
        code = int(tr[0])*(len(self.triangles)**2) + int(tr[1])*len(self.triangles) + int(tr[2])
        return code

    def create_dual_graph_optimal(self):
        d_vertexes = {i: self.triangles[i] for i in range(0, len(self.triangles))}
        d_vertexes_indexes = {self.get_tr_code(self.triangles[i]): i for i in range(0, len(self.triangles))}
        d_edges = {}
        d_vertex_per_edge = {}
        # 0 - unused
        # 1 - gray
        # 2 - black
        d_vertex_color = {self.get_tr_code(self.triangles[i]): 0 for i in range(0, len(self.triangles))}
        for vertex in d_vertexes:
            vertex = d_vertexes[vertex]
            p1, p2, p3 = vertex[0], vertex[1], vertex[2]
            p1, p2, p3 = int(p1), int(p2), int(p3)
            p1p2 = (p1, p2) if p1 < p2 else (p2, p1)
            p2p3 = (p2, p3) if p2 < p3 else (p3, p2)
            p3p1 = (p3, p1) if p3 < p1 else (p1, p3)

            if p1p2 not in d_vertex_per_edge:
                d_vertex_per_edge[p1p2] = list()
            if p2p3 not in d_vertex_per_edge:
                d_vertex_per_edge[p2p3] = list()
            if p3p1 not in d_vertex_per_edge:
                d_vertex_per_edge[p3p1] = list()

            d_vertex_per_edge[p1p2].append([p1, p2, p3])
            d_vertex_per_edge[p2p3].append([p1, p2, p3])
            d_vertex_per_edge[p3p1].append([p1, p2, p3])

        current_triangle = 0
        all_count = 0
        stack = list()
        stack.append(current_triangle)
        while all_count < len(self.triangles):
            if len(stack) == 0:
                t = 0
            current_triangle = stack.pop()
            vertex = d_vertexes[current_triangle]

            vertex_code = self.get_tr_code(vertex)
            d_vertex_color[vertex_code] = 2
            all_count += 1

            p1, p2, p3 = vertex[0], vertex[1], vertex[2]
            p1, p2, p3 = int(p1), int(p2), int(p3)
            vertex_int = [p1, p2, p3]
            p1p2 = (p1, p2) if p1 < p2 else (p2, p1)
            p2p3 = (p2, p3) if p2 < p3 else (p3, p2)
            p3p1 = (p3, p1) if p3 < p1 else (p1, p3)

            if current_triangle not in d_edges:
                d_edges[current_triangle] = list()

            #neighbors = list()
            edges = [p1p2, p2p3, p3p1]
            for edge in edges:
                for tr in d_vertex_per_edge[edge]:
                    v_code = self.get_tr_code([str(tr[0]), str(tr[1]), str(tr[2])])
                    if tr != vertex_int and d_vertex_color[v_code] == 0:
                        v_index = d_vertexes_indexes[v_code]
                        d_vertex_color[v_code] = 1
                        if v_index not in d_edges:
                            d_edges[v_index] = list()

                        if v_index not in d_edges[current_triangle]:
                            d_edges[current_triangle].append(v_index)
                            stack.append(v_index)
                        if current_triangle not in d_edges[v_index]:
                            d_edges[v_index].append(current_triangle)
        self.dual_vertexes = d_vertexes
        self.dual_edges = d_edges

    def dfs(self, s):
        # s = int(s)
        visited, stack = set(), [s]
        while stack:
            vertex = stack.pop()
            # vertex = int(vertex)
            if vertex not in visited:
                color_sum = self.polygon[int(self.dual_vertexes[vertex][0])].color + \
                    self.polygon[int(self.dual_vertexes[vertex][1])].color + \
                    self.polygon[int(self.dual_vertexes[vertex][2])].color

                if color_sum < 3:
                    # print("Triangle #" + str(vertex) + " has one vertex uncolored!!!")
                    if self.polygon[int(self.dual_vertexes[vertex][0])].color is -1:
                        self.polygon[int(self.dual_vertexes[vertex][0])].color = 3 - (color_sum + 1)
                        # print("Triangle #" + str(vertex) + " Vertex #0 found uncolored!!! Now colored to " + str(
                        #    vdual[vertex][0].color))
                    elif self.polygon[int(self.dual_vertexes[vertex][1])].color is -1:
                        self.polygon[int(self.dual_vertexes[vertex][1])].color = 3 - (color_sum + 1)
                        # print("Triangle #" + str(vertex) + " Vertex #1 found uncolored!!! Now colored to " + str(
                        #    vdual[vertex][1].color))
                    elif self.polygon[int(self.dual_vertexes[vertex][2])].color is -1:
                        self.polygon[int(self.dual_vertexes[vertex][2])].color = 3 - (color_sum + 1)
                        # print("Triangle #" + str(vertex) + " Vertex #2 found uncolored!!! Now colored to " + str(
                        #     vdual[vertex][2].color))
                visited.add(vertex)
                stack.extend(set(self.dual_edges[vertex]) - visited)
        return visited

    def colorize(self): #, map_points, listTriangle, vdual, edual):
        # ear_vertex = None
        # ear_tri = None
        # key = None
        for d_edge in self.dual_edges:
            if len(self.dual_edges[d_edge]) == 1:
                # ear
                key_ear_tri = d_edge
                break

        ear_tri = self.dual_vertexes[key_ear_tri]

        # print("############################# INITIAL COLORING OF ONE TRIANGLE ##################################")
        # print("Triangle #" + str(key) + " Vertex #0 colored to 0")
        self.polygon[int(ear_tri[0])].color = 0
        # print("Triangle #" + str(key) + " Vertex #1 colored to 1")
        self.polygon[int(ear_tri[1])].color = 1
        # print("Triangle #" + str(key) + " Vertex #2 colored to 2")
        self.polygon[int(ear_tri[2])].color = 2
        # print("############################# GOING TO COLOR REMAINING TRIANGLES ###############################")
        self.dfs(key_ear_tri)
        output, col = self.find_min_color()
        # print("Guards are colored " + str(col - 1))
        return output, col

    def find_min_color(self):
        r_count, g_count, b_count = 0, 0, 0
        r, g, b = [], [], []
        out = set()
        for t in self.triangles:
            for it in t:
                it = self.polygon[int(it)]
                if it not in out:
                    if it.color is 0:
                        r_count += 1
                        r.append(it)
                    elif it.color is 1:
                        g_count += 1
                        g.append(it)
                    elif it.color is 2:
                        b_count += 1
                        b.append(it)
                    out.add(it)
        if r_count is g_count and r_count is b_count:
            return r, r_count
        if r_count <= g_count and r_count <= b_count:
            return r, r_count
        if g_count <= r_count and g_count <= b_count:
            return g, g_count
        if b_count <= r_count and b_count <= g_count:
            return b, b_count