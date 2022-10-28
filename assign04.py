"""
Assign 04 - <INSERT YOUR NAME HERE>

Directions:
    * Complete the graph algorithm functions given below. Note that it may be
      helpful to define auxiliary/helper functions that are called from the
      functions below.  Refer to the README.md file for additional info.

    * NOTE: As with other assignments, please feel free to share ideas with
      others and to reference sources from textbooks or online. However, be sure
      to **cite your resources in your code. Also, do your best to attain a
      reasonable grasp of the algorithm that you are implementing as there will
      very likely be questions related to it on quizzes/exams.

    * NOTE: Remember to add a docstring for each function, and that a reasonable
      coding style is followed (e.g. blank lines between functions).
      Your program will not pass the tests if this is not done!
"""

# for timing checks
import time
import sys


def adjMatFromFile(filename):
    """ Create an adj/weight matrix from a file with verts, neighbors, and weights. """
    f = open(filename, "r")
    n_verts = int(f.readline())
    print(f" n_verts = {n_verts}")
    adjmat = [[None] * n_verts for i in range(n_verts)]
    for i in range(n_verts):
        adjmat[i][i] = 0
    for line in f:
        int_list = [int(i) for i in line.split()]
        vert = int_list.pop(0)
        assert len(int_list) % 2 == 0
        n_neighbors = len(int_list) // 2
        neighbors = [int_list[n] for n in range(0, len(int_list), 2)]
        distances = [int_list[d] for d in range(1, len(int_list), 2)]
        for i in range(n_neighbors):
            adjmat[vert][neighbors[i]] = distances[i]
    f.close()
    return adjmat


def minWeight(W, visited):
    """ Prim helper method to find index of ninimum weight edge."""
    min = sys.maxsize

    for i in range(len(visited)):
        if W[i] < min and visited[i] is False:
            min = W[i]
            min_index = i

    return min_index


def prim(W):
    """ Carry out Prim's algorithm using W as a weight/adj matrix."""
    q_vertices = len(W)
    mst_list = [0] * (q_vertices - 1)
    selected = [0] * q_vertices
    edges = 0

    selected[0] = True

    while edges < (q_vertices - 1):
        weight = sys.maxsize
        for i in range(q_vertices):
            if selected[i]:
                for j in range(q_vertices):
                    if ((not selected[j]) and W[i][j] is not None):
                        if weight > W[i][j]:
                            weight = W[i][j]
                            x = i
                            y = j
        mst_list[edges] = [x, y, weight]
        selected[y] = True
        edges += 1

    for i in range(len(mst_list)):
        if mst_list[i][0] > mst_list[i][1]:
            temp = mst_list[i][0]
            mst_list[i][0] = mst_list[i][1]
            mst_list[i][1] = temp

    mst_tuple = [tuple(ele) for ele in mst_list]

    return mst_tuple


def sortGraph(W):
    """ Sorts list of edges and their weights."""
    graph = []
    for i in range(len(W)):
        for j in range(len(W)):
            if W[i][j] is not None and W[i][j] != 0:
                graph.append([i, j, W[i][j]])
    return sorted(graph, key=lambda item: item[2])


def find(graph, root, i):
    """ Kruskal union helper method."""
    if root[i] == i:
        return i
    return find(graph, root, root[i])


def union(graph, root, rank, x, y):
    """ Kruskal helper method."""
    xroot = find(graph, root, x)
    yroot = find(graph, root, y)

    if rank[xroot] < rank[yroot]:
        root[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        root[yroot] = xroot
    else:
        root[yroot] = xroot
        rank[xroot] += 1


def kruskal(W):
    """ Carry out Kruskal's using W as a weight/adj matrix. """
    result = []
    q_vertices = len(W)
    i, e = 0, 0

    graph = sortGraph(W)
    parent = []
    rank = []

    for node in range(q_vertices):
        parent.append(node)
        rank.append(0)
    while e < q_vertices - 1:
        u, v, w = graph[i]
        i = i + 1
        x = find(graph, parent, u)
        y = find(graph, parent, v)

        if x != y:
            e = e + 1
            result.append([u, v, w])
            union(graph, parent, rank, x, y)

    for i in range(len(result)):
        if result[i][0] > result[i][1]:
            temp = result[i][0]
            result[i][0] = result[i][1]
            result[i][1] = temp

    result_tuple = [tuple(ele) for ele in result]

    return result_tuple


def assign04_main():
    """ Demonstrate the functions, starting with creating the graph. """
    g = adjMatFromFile("graph_verts10.txt")

    # Run Prim's algorithm
    start_time = time.time()
    res_prim = prim(g)
    elapsed_time_prim = time.time() - start_time
    print(f"Prim's runtime: {elapsed_time_prim:.2f}")

    # Run Kruskal's for a single starting vertex, 2
    start_time = time.time()
    res_kruskal = kruskal(g)
    elapsed_time_kruskal = time.time() - start_time
    print(f"Kruskal's runtime: {elapsed_time_kruskal:.2f}")

    # Check that sum of edges weights are the same for this graph
    cost_prim = sum([e[2] for e in res_prim])
    print("MST cost w/ Prim: ", cost_prim)
    cost_kruskal = sum([e[2] for e in res_kruskal])
    print("MST cost w/ Kruskal: ", cost_kruskal)
    assert cost_prim == cost_kruskal


# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign04_main()
