from collections import deque
from graph_utils import draw_graph
import debug


class SubCubicVertexCoverP3:
    def __init__(self, graph):
        self.__graph = graph
        self.__global_candidates = [0 for _ in self.__graph]
        self.__iteration_candidates = [False for _ in self.__graph]

    def __find_next_3_vertex_or_leaf(self, previous_vertex, current_vertex):
        debug.print('__find_next_3_vertex_or_leaf', previous_vertex, current_vertex)
        while self.__graph.degree(current_vertex) == 2:
            for neighbor in self.__graph.neighbors(current_vertex):
                if neighbor != previous_vertex:
                    previous_vertex = current_vertex
                    current_vertex = neighbor
                    break
        return previous_vertex, current_vertex

    def __find_next_3_vertex_or_leaf_with_cover(self, leaf):
        debug.print('__find_next_3_vertex_or_leaf_with_cover', leaf)
        current_vertex = next(self.__graph.neighbors(leaf))
        previous_vertex = leaf
        path_length = 1
        while self.__graph.degree(current_vertex) == 2:
            if path_length % 3 == 2:
                self.__iteration_candidates[current_vertex] = True
            path_length += 1
            for neighbor in self.__graph.neighbors(current_vertex):
                if neighbor != previous_vertex:
                    previous_vertex = current_vertex
                    current_vertex = neighbor
                    break

        since_last_candidate = path_length % 3
        if since_last_candidate == 1 and self.__graph.degree(current_vertex) == 3:
            for neighbor in self.__graph.neighbors(current_vertex):
                if neighbor != previous_vertex:
                    self.__iteration_candidates[neighbor] = True
        elif since_last_candidate == 2:
            self.__iteration_candidates[current_vertex] = True

        return previous_vertex, current_vertex

    def __is_star_covered(self, center):
        debug.print('__is_star_covered', center)
        neighbors_candidates_sum =\
            sum([self.__iteration_candidates[neighbor] for neighbor in self.__graph.neighbors(center)])
        return self.__iteration_candidates[center] or neighbors_candidates_sum >= 2, neighbors_candidates_sum

    def __solve_cover_for_3_vertex_and_stop_vertex(self, center, direction, stop):
        debug.print('__solve_cover_for_3_vertex_and_leaf', center, direction, stop)
        current = direction
        previous = center
        if self.__iteration_candidates[direction]:
            length = 0
        elif self.__iteration_candidates[center]:
            length = 1
        else:
            length = 2
        while current != stop:
            for neighbor in self.__graph.neighbors(current):
                if neighbor != previous:
                    length += 1
                    if length % 3 == 0:
                        self.__iteration_candidates[neighbor] = True
                    previous = current
                    current = neighbor
                    break

    def __solve_cover_for_3_3_bridge(self, parent_vertex, left_center, left_bridge_side,
                                     right_bridge_side, right_center):
        debug.print('__solve_cover_for_3_3_bridge', parent_vertex, left_center,
                  left_bridge_side, right_bridge_side, right_center)
        # cover left star
        left_star_covered, left_neighbors_candidates_sum = self.__is_star_covered(left_center)
        if not left_star_covered:
            if left_neighbors_candidates_sum == 0:
                self.__iteration_candidates[left_center] = True
            else:
                if self.__iteration_candidates[left_bridge_side]:
                    # candidate on bridge; take one of sides; not the side we came from (previous is 3-3 covered)
                    for neighbor in self.__graph.neighbors(left_center):
                        if neighbor == left_bridge_side or neighbor == parent_vertex:
                            continue
                        else:
                            self.__iteration_candidates[neighbor] = True
                            break
                else:  # candidate on side, need to take left_bridge_side to take cover more far away
                    self.__iteration_candidates[left_bridge_side] = True

        # traverse to right star, picking vertices along the way
        current_vertex = None
        previous_vertex = None
        path_length = 1
        if self.__iteration_candidates[left_center]:
            previous_vertex = left_center
            current_vertex = left_bridge_side
        if self.__iteration_candidates[left_bridge_side]:
            previous_vertex = left_bridge_side
            for neighbor in self.__graph.neighbors(left_bridge_side):
                if neighbor != left_center:
                    current_vertex = neighbor
        if current_vertex is None:
            previous_vertex = left_center
            current_vertex = left_bridge_side
            path_length = 2
        while current_vertex != right_bridge_side and current_vertex != right_center and previous_vertex != right_center:
            for neighbor in self.__graph.neighbors(current_vertex):
                if neighbor != previous_vertex:
                    debug.print('\t\t', neighbor)
                    previous_vertex = current_vertex
                    current_vertex = neighbor
                    path_length += 1
                    if path_length % 3 == 0:
                        self.__iteration_candidates[current_vertex] = True
                    break
        if current_vertex == right_bridge_side and path_length == 2:
            self.__iteration_candidates[right_center] = True

        # cover right star
        right_star_covered, right_neighbors_candidates_sum = self.__is_star_covered(right_center)
        if not right_star_covered:
            if right_neighbors_candidates_sum == 0:
                # just go for minimum possible cover
                self.__iteration_candidates[right_center] = True
            else:
                if self.__iteration_candidates[right_bridge_side]:
                    # take side vertex with highest degree (leaf is already covered; 3-vertex is better than 2-vertex)
                    max_degree = 0
                    max_degree_vertex = None
                    for neighbor in self.__graph.neighbors(right_center):
                        if neighbor != right_bridge_side:
                            degree = self.__graph.degree(neighbor)
                            if degree > max_degree:
                                max_degree = degree
                                max_degree_vertex = neighbor
                    self.__iteration_candidates[max_degree_vertex] = True
                else:
                    # take other side vertex
                    for neighbor in self.__graph.neighbors(right_center):
                        if neighbor == right_bridge_side or self.__iteration_candidates[neighbor]:
                            continue
                        else:
                            self.__iteration_candidates[neighbor] = True
                            break

    def __bfs_cover_compute(self, starting_point_parent, starting_point):
        debug.print('__bfs_cover_compute', starting_point_parent, starting_point)
        queued = [False for _ in self.__graph]
        backtrack = [[] for _ in self.__graph]
        queue = deque()
        queue.append((starting_point_parent, starting_point))
        while len(queue) != 0:
            leaf_cycle = False
            parent_vertex, first_vertex = queue.popleft()
            debug.print(first_vertex)

            other_neighbor = None
            for neighbor in self.__graph.neighbors(first_vertex):
                if leaf_cycle or neighbor in backtrack[first_vertex]:
                    debug.print('\t', neighbor, 'visited')
                else:
                    debug.print('\t', neighbor, 'not visited')
                    previous_vertex, second_vertex = self.__find_next_3_vertex_or_leaf(first_vertex, neighbor)
                    backtrack[second_vertex].append(previous_vertex)

                    # corner cases (special handling needed when solving for cover)
                    # leaf or "double path"
                    if self.__graph.degree(second_vertex) == 1 or other_neighbor == second_vertex:
                        self.__solve_cover_for_3_vertex_and_stop_vertex(first_vertex, neighbor, second_vertex)
                        if other_neighbor == second_vertex:
                            print("found double path", first_vertex, neighbor, second_vertex)
                            self.__graph.nodes[first_vertex]['color'] = 'red'
                            self.__graph.nodes[second_vertex]['color'] = 'red'
                        continue

                    # found "leaf cycle"
                    if second_vertex == first_vertex:
                        leaf_cycle = True
                        self.__solve_cover_for_3_vertex_and_stop_vertex(first_vertex, neighbor, second_vertex)
                        continue

                    # save to check if the second path leads to the same 3-vertex
                    if other_neighbor is None:
                        other_neighbor = second_vertex

                    self.__solve_cover_for_3_3_bridge(parent_vertex, first_vertex, neighbor,
                                                      previous_vertex, second_vertex)

                    if debug.PRINT_DEBUG:
                        for vertex, count in enumerate(self.__iteration_candidates):
                            if count > 0:
                                self.__graph.nodes[vertex]['color'] = 'green'
                        draw_graph(self.__graph)

                    if not queued[second_vertex]:
                        queue.append((previous_vertex, second_vertex))
                        queued[second_vertex] = True

    def __leaf_iteration(self, leaf):
        debug.print('__leaf_iteration', leaf)
        self.__iteration_candidates = [False for _ in self.__graph]
        starting_point_parent, starting_point = self.__find_next_3_vertex_or_leaf_with_cover(leaf)
        self.__bfs_cover_compute(starting_point_parent, starting_point)
        for vertex, _ in enumerate(self.__global_candidates):
            self.__global_candidates[vertex] += self.__iteration_candidates[vertex]

    def compute(self):
        debug.print('compute')
        self.__global_candidates = [0 for _ in self.__graph]
        self.__iteration_candidates = [False for _ in self.__graph]
        cover = []

        leaves_count = 0
        for vertex in self.__graph:
            if self.__graph.degree(vertex) == 1:
                leaves_count += 1
                self.__leaf_iteration(vertex)
                break  # TODO: remove break to check all leaves; then construct cover with strongest candidates
        if leaves_count == 1:
            for vertex, candidate_order in enumerate(self.__global_candidates):
                if candidate_order != 0:
                    cover.append(vertex)

        return cover, self.__global_candidates


# def count_intersections_bfs(graph):
#     queued = [False for _ in graph]
#     backtrack = [[] for _ in graph]
#     possible_candidates = [False for _ in graph]
#     intersections = 0
#     intersections_axis = []
#     pairs = 0
#     queue = deque()
#     double_paths = []
#
#     previous_vertex = -1
#     for vertex in graph:
#         if graph.degree(vertex) == 1:
#             previous_vertex = vertex
#             break
#     if previous_vertex == -1:
#         print("graph does not contain leaves")
#         return
#     print(previous_vertex)
#
#     current_vertex = next(graph.neighbors(previous_vertex))
#     previous_vertex, current_vertex = find_next_3_vertex_or_leaf(graph, previous_vertex, current_vertex)
#
#     queue.append((previous_vertex, current_vertex))
#     while len(queue) != 0:
#         parent_vertex, first_vertex = queue.popleft()
#         possible_candidates[parent_vertex] = True
#         possible_candidates[first_vertex] = True
#         other_neighbor = None
#         for neighbor in graph.neighbors(first_vertex):
#             if neighbor not in backtrack[first_vertex]:
#                 previous_vertex, second_vertex = find_next_3_vertex_or_leaf(graph, first_vertex, neighbor)
#                 backtrack[second_vertex].append(previous_vertex)
#
#                 # corner cases (special handling needed when solving for cover)
#                 if graph.degree(second_vertex) == 1:  # found leaf
#                     continue
#                 if second_vertex == first_vertex:  # found "leaf cycle"
#                     continue
#                 if other_neighbor is None:
#                     other_neighbor = second_vertex
#                 elif other_neighbor == second_vertex:  # found "double path"
#                     double_paths.append((first_vertex, second_vertex))
#                     continue
#
#                 # check if far side of 3-3 bridge has been visited
#                 for far_neighbor in graph.neighbors(second_vertex):
#                     if far_neighbor == first_vertex:
#                         continue
#                     if possible_candidates[far_neighbor]:
#                         intersections += 1
#                         break
#                 intersections_axis.append(intersections)
#
#                 possible_candidates[second_vertex] = True
#                 for far_neighbor in graph.neighbors(second_vertex):
#                     possible_candidates[far_neighbor] = True
#                 print('({}, {})'.format(first_vertex, second_vertex), end=', ')
#                 pairs += 1
#                 if not queued[second_vertex]:
#                     queue.append((previous_vertex, second_vertex))
#                     queued[second_vertex] = True
#     print()
#     for double_path in double_paths:
#         print('({}, {})'.format(double_path[0], double_path[1]), end=', ')
#     print()
#     plt.plot(intersections_axis)
#     plt.show()
#     return pairs, intersections
#
#
# def count_intersections_dfs(graph):
#     # не думаю что имеет смысл это реализовывать
#     # может не хватить времени
#     # попробовать когда в ширину будет готово
#     pass
