from graph_utils import color_key


def compute_greedy_cubic_vertex_cover(graph):
    cover = []
    for vertex in list(graph):
        if graph.degree(vertex) == 3:
            cover.append(vertex)
            graph.remove_node(vertex)
    visited = []
    for vertex in list(graph):
        if graph.degree(vertex) == 0:
            # cover.append(vertex)
            # graph.nodes[vertex][color_key] = 'green'
            pass
        elif vertex not in visited and graph.degree(vertex) == 1:
            cover.append(vertex)
            graph.nodes[vertex][color_key] = 'green'
            current = next(graph.neighbors(vertex))
            previous = vertex
            length = 1
            while graph.degree(current) != 1:
                for neighbor in graph.neighbors(current):
                    if neighbor != previous:
                        length += 1
                        if length % 3 == 0:
                            cover.append(neighbor)
                            graph.nodes[neighbor][color_key] = 'green'
                        previous = current
                        current = neighbor
                        break
            visited.append(current)
    return cover
