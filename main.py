from graph_utils import generate_subcubic_graph_from_rary_tree
from graph_utils import generate_subcubic_graph_from_cubic_graph
from graph_utils import generate_subcubic_graph_inside_out
from graph_utils import draw_graph, color_key, print_degrees
from vertex_cover_p3 import SubCubicVertexCoverP3
import queue
from networkx import Graph
from greedy_cubic_vertex_cover import compute_greedy_cubic_vertex_cover


# a center vertex or any 2 vertices are enough to cover a star
def is_star_covered(graph, candidates, center):
    neighbors_candidates_sum = sum([candidates[neighbor] for neighbor in graph.neighbors(center)])
    return candidates[center] or neighbors_candidates_sum >= 2, neighbors_candidates_sum


def solve_cover(graph, candidates, left_center, left_bridge_side, right_bridge_side, right_center, parent_vertex=-1):
    # cover left star
    left_star_covered, left_neighbors_candidates_sum = is_star_covered(graph, candidates, left_center)
    if not left_star_covered:
        if left_neighbors_candidates_sum == 0:
            candidates[left_center] = True
        else:
            if candidates[left_bridge_side]:
                # candidate on bridge, need to take one of sides; not the side we came from (previous is 3-3 covered)
                for neighbor in graph.neighbors(left_center):
                    if neighbor == left_bridge_side or neighbor == parent_vertex:
                        continue
                    else:
                        candidates[neighbor] = True
                        break
            else:  # candidate on side, need to take left_bridge_side to take cover more far away
                candidates[left_bridge_side] = True

    # traverse to right star, picking vertices along the way
    current_vertex = None
    previous_vertex = None
    path_length = 1
    if candidates[left_center]:
        previous_vertex = left_center
        current_vertex = left_bridge_side
    if candidates[left_bridge_side]:
        previous_vertex = left_bridge_side
        for neighbor in graph.neighbors(left_bridge_side):
            if neighbor != left_center:
                current_vertex = neighbor
    if current_vertex is None:
        previous_vertex = left_center
        current_vertex = left_bridge_side
        path_length = 2
    while current_vertex != right_bridge_side and current_vertex != right_center and previous_vertex != right_center:
        for neighbor in graph.neighbors(current_vertex):
            if neighbor != previous_vertex:
                previous_vertex = current_vertex
                current_vertex = neighbor
                path_length += 1
                if path_length % 3 == 0:
                    candidates[current_vertex] = True

    # cover right star
    right_star_covered, right_neighbors_candidates_sum = is_star_covered(graph, candidates, right_center)
    if not right_star_covered:
        if right_neighbors_candidates_sum == 0:
            # just go for minimum possible cover
            candidates[right_center] = True
        else:
            if candidates[right_bridge_side]:
                # take side vertex with highest degree (leaf is already covered; 3-vertex is better than 2-vertex)
                max_degree = 0
                max_degree_vertex = None
                for neighbor in graph.neighbors(right_center):
                    if neighbor != right_bridge_side:
                        degree = graph.degree(neighbor)
                        if degree > max_degree:
                            max_degree = degree
                            max_degree_vertex = neighbor
                candidates[max_degree_vertex] = True
            else:
                # take other side vertex
                for neighbor in graph.neighbors(right_center):
                    if neighbor == right_bridge_side or candidates[neighbor]:
                        continue
                    else:
                        candidates[neighbor] = True
                        break


if __name__ == '__main__':
    found = False
    graph = None
    while not found:
        graph = generate_subcubic_graph_from_cubic_graph(100, 20, 30)
        # cover, candidates = compute_vertex_cover_p3_on_subcubic_graph(graph)
        for vertex in graph:
            if graph.degree(vertex) == 1:
                found = True
                break
    graph_greedy = graph.copy()
    # draw_graph(graph)

    algorithm = SubCubicVertexCoverP3(graph)
    cover, candidates = algorithm.compute()
    for vertex, count in enumerate(candidates):
        if count > 0:
            if color_key in graph.nodes[vertex] and graph.nodes[vertex][color_key] == 'red':
                graph.nodes[vertex][color_key] = 'black'
            else:
                graph.nodes[vertex][color_key] = 'green'
    # print(cover, candidates)
    print('my', cover, len(cover))
    draw_graph(graph)

    graph_greedy_backup = graph_greedy.copy()
    cover = compute_greedy_cubic_vertex_cover(graph_greedy)
    print('greedy', cover, len(cover))
    # for vertex in cover:
    #     graph_greedy_backup.nodes[vertex][color_key] = 'green'
    # draw_graph(graph_greedy_backup)

    # print_degrees(graph)
    # pairs, intersections = count_intersections_bfs(graph)
    # pairs, intersections = count_intersections_pseudo_dfs(graph)
    # print('pairs: {}, intersections: {}, ratio: {:.2f}'.format(pairs, intersections, intersections/pairs))


# if __name__ == '__main__':
#     g = Graph()
#     for i in range(5):
#         g.add_node(i)
#     g.add_edge(0, 1)
#     g.add_edge(1, 2)
#     g.add_edge(3, 4)
#     g.add_edge(4, 2)
#
#     g.add_edge(1, 4)
#
#     cover = [False for _ in g]
#     cover[0] = True
#
#     solve_cover(g, cover, 1, 2, 2, 4)
#
#     for vertex, in_cover in enumerate(cover):
#         if in_cover:
#             g.nodes[vertex][color_key] = 'green'
#     draw_graph(g)

