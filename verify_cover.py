from collections import deque
from graph_utils import color_key, draw_graph


def error(graph, cover):
    for vertex in cover:
        graph.nodes[vertex][color_key] = 'green'
    draw_graph(graph)
    print('Incorrect solution!')


def verify_cover(graph, cover):
    queue = deque()
    for vertex in graph:
        if graph.degree(vertex) == 1:
            queue.append((vertex, -1, 0))
            break
    visited = []
    while len(queue) != 0:
        vertex, parent, count_no_cover = queue.popleft()
        if vertex in cover:
            count_no_cover = 0
        else:
            count_no_cover += 1
            if count_no_cover == 3:
                error(graph, cover)
                return False
        visited.append(vertex)
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                queue.append((neighbor, vertex, count_no_cover))
            elif neighbor != parent and neighbor not in cover and count_no_cover + 1 == 3:
                error(graph, cover)
                return False
    return True
