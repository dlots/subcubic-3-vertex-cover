from time import time
import queue
from networkx import Graph
from networkx.exception import NetworkXError
import matplotlib.pyplot as plt
from tqdm import tqdm


from graph_utils import generate_subcubic_graph_from_rary_tree
from graph_utils import generate_subcubic_graph_from_cubic_graph
from graph_utils import generate_subcubic_graph_inside_out
from graph_utils import draw_graph, color_key, print_degrees
from vertex_cover_p3 import SubCubicVertexCoverP3
from greedy_cubic_vertex_cover import compute_greedy_cubic_vertex_cover
from verify_cover import verify_cover


if __name__ == '__main__':
    count_errors = 0
    vertices = []
    execution_time = []
    size_list = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, ]
    # for i in tqdm(range(50, 100000, 1000)):
    for i in tqdm(size_list):
        found = False
        graph = None
        while not found:
            try:
                graph = generate_subcubic_graph_from_cubic_graph(i, 20, 30)
            except NetworkXError:
                break
            for vertex in graph:
                if graph.degree(vertex) == 1:
                    found = True
                    break
        if graph is None:
            continue

        # graph_greedy = graph.copy()
        # draw_graph(graph)

        algorithm = SubCubicVertexCoverP3(graph)
        start = time()
        cover, candidates = algorithm.compute()
        elapsed = time() - start
        if verify_cover(graph, cover):
            vertices.append(i)
            execution_time.append(elapsed)
        else:
            count_errors += 1

        plt.plot(vertices, execution_time)
        plt.show()

    print(count_errors, 'errors')

    # for vertex, count in enumerate(candidates):
    #     if count > 0:
    #         if color_key in graph.nodes[vertex] and graph.nodes[vertex][color_key] == 'red':
    #             graph.nodes[vertex][color_key] = 'black'
    #         else:
    #             graph.nodes[vertex][color_key] = 'green'
    # print('my', cover, len(cover))
    # draw_graph(graph)

    # graph_greedy_backup = graph_greedy.copy()
    # cover = compute_greedy_cubic_vertex_cover(graph_greedy)
    # print('greedy', cover, len(cover))
    # verify_cover(graph_greedy_backup, cover)
    # for vertex in cover:
    #     graph_greedy_backup.nodes[vertex][color_key] = 'green'
    # draw_graph(graph_greedy_backup)

    # print_degrees(graph)
    # pairs, intersections = count_intersections_bfs(graph)
    # pairs, intersections = count_intersections_pseudo_dfs(graph)
    # print('pairs: {}, intersections: {}, ratio: {:.2f}'.format(pairs, intersections, intersections/pairs))
