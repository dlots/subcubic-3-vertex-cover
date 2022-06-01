from graph_utils import generate_subcubic_graph_from_rary_tree
from graph_utils import generate_subcubic_graph_from_cubic_graph
from graph_utils import generate_subcubic_graph_inside_out
from graph_utils import draw_graph, color_key, print_degrees
from vertex_cover_p3 import SubCubicVertexCoverP3
import queue
from networkx import Graph
from greedy_cubic_vertex_cover import compute_greedy_cubic_vertex_cover
from verify_cover import verify_cover


if __name__ == '__main__':
    count_errors = 0
    for i in range(10000):
        found = False
        graph = None
        while not found:
            graph = generate_subcubic_graph_from_cubic_graph(100, 20, 30)
            for vertex in graph:
                if graph.degree(vertex) == 1:
                    found = True
                    break

        # graph_greedy = graph.copy()
        # draw_graph(graph)

        algorithm = SubCubicVertexCoverP3(graph)
        cover, candidates = algorithm.compute()
        count_errors += not verify_cover(graph, cover)
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
