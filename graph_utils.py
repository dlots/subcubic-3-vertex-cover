import random

import matplotlib.pyplot as plt
from networkx.generators.classic import full_rary_tree
from networkx.generators.random_graphs import random_regular_graph
from networkx import draw, draw_planar, Graph, get_edge_attributes
from networkx import draw_networkx_edge_labels, spring_layout, planar_layout
from networkx import connected_components
from random import randint, choice, sample
from collections import deque

color_key = 'color'


def generate_subcubic_graph_from_rary_tree(n_vertices):
    graph = full_rary_tree(2, n_vertices)
    return graph


def generate_subcubic_graph_from_cubic_graph(n_vertices, lower_delete_percentage=25, higher_delete_percentage=50):
    graph = random_regular_graph(3, n_vertices)
    delete_percentage = randint(lower_delete_percentage, higher_delete_percentage)
    n_to_delete = int(n_vertices * delete_percentage * 0.01)
    to_delete = sample(graph.edges(), k=n_to_delete)
    graph.remove_edges_from(to_delete)
    components = [component for component in connected_components(graph)]
    max_length = 0
    max_component = 0
    for i, component in enumerate(components):
        if len(component) > max_length:
            max_length = len(component)
            max_component = i
    for i, component in enumerate(components):
        found_connection_point = False
        if i == max_component:
            continue
        for u in component:
            if graph.degree(u) < 3:
                for v in components[max_component]:
                    if graph.degree(v) < 3:
                        graph.add_edge(u, v)
                        found_connection_point = True
                        break
                if found_connection_point:
                    break
    return graph


def generate_subcubic_graph_inside_out(n_vertices):
    graph = Graph()

    return graph


def print_adjacency_list(graph):
    for node in graph:
        print(node, end=': ')
        for adj in graph.adj[node]:
            print(adj, end=',')
        print()


def nx_to_adj_list(graph):
    adj_list = []
    for node in graph:
        adj_list.append([])
        for adj in graph.adj[node]:
            adj_list[node].append([adj, graph[node][adj]['weight']])
    return adj_list


def draw_weighted_graph(graph):
    pos = planar_layout(graph)
    draw_planar(graph, with_labels=True)
    weights = get_edge_attributes(graph, 'weight')
    draw_networkx_edge_labels(graph, pos, weights)
    plt.show()


def draw_graph(graph, edge_colors=None):
    pos = spring_layout(graph)
    color_map = []
    for vertex in graph:
        if color_key in graph.nodes[vertex]:
            color_map.append(graph.nodes[vertex][color_key])
        else:
            color_map.append('deepskyblue')
    plt.figure(figsize=(12, 12))
    draw(graph, pos, with_labels=True, edge_color=edge_colors, node_color=color_map, node_size=100, font_size=20)
    weights = get_edge_attributes(graph, 'weight')
    draw_networkx_edge_labels(graph, pos, weights)
    plt.show()


def print_degrees(graph):
    degrees = [0, 0, 0]
    for v in graph:
        degrees[graph.degree(v) - 1] += 1
    print(degrees)
