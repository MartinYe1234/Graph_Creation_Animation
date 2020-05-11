from Interface import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as mpa

"""Create networkX graph to visualise"""


# animation is based off of the concept from:
# https://stackoverflow.com/questions/43646550/how-to-use-an-update-function-to-animate-a-networkx-graph-in-matplotlib-2-0-0?rq=1
def create_networkx_graph(p, nodes, edges):
    global adj_list, G, position, edge_weights_labels
    print("edges:", edges)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    # set position of every node
    nx.set_node_attributes(G, p, 'pos')
    position = nx.get_node_attributes(G, 'pos')
    print("position of nodes", position)
    # add all edges
    G.add_weighted_edges_from(edges)
    # labels for edge weights
    edge_weights_labels = []
    # create adjacency list
    adj_list = {}

    # fill adjacency list
    for node in nodes:
        adj_list[node] = []
    for edge in edges:
        node = edge[0]
        connected_node = edge[1]
        # generate weights by calculating distance between the two nodes
        x1, y1 = position[node][0], position[node][1]
        x2, y2 = position[connected_node][0], position[connected_node][1]
        # the weight is the distance between the two connected nodes multiplied by 100 and rounded to 1 decimal place
        weight = round((((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5) * 100, 1)
        adj_list[node].append([connected_node, weight])
        adj_list[connected_node].append([node, weight])
        # fill edge_weight_labels
        if edge not in edge_weights_labels:
            edge_weights_labels.append([edge[0], edge[1], weight])

    print("edge weights:", edge_weights_labels)
    print("adj list:", adj_list)


def bfs(graph, start):
    """
    Runs bfs on a graph with the purpose of visualising it

    Parameters
    ----------
    graph : dict
        Dictionary with nodes as keys and values as the adjacent nodes and weights as values
    start : int
        Starting node

    Returns
    -------
    order_visited : list
        list containing order of nodes visited as tuples (u, v)
    """
    queue = [start]
    bfs_visited = [start]
    # store order of visited nodes
    order_visited = []
    # while there is something in the queue
    while queue:
        current_node = queue[0]
        # for each adjacent node to the current node
        for neighbour in graph[current_node]:
            adjacent_node = neighbour[0]
            # if the vertex has not been visited yet
            if adjacent_node not in bfs_visited:
                order_visited.append((current_node, adjacent_node))
                # add adjacent (neighbour) node to queue
                queue.append(adjacent_node)
                # mark as visited
                bfs_visited.append(adjacent_node)
        queue.pop(0)
    return order_visited


def dfs(graph, start):
    """
    Runs dfs on a graph with the purpose of visualising it - not recursive version

    Parameters
    ----------
    graph : dict
        Dictionary with nodes as keys and values as the adjacent nodes and weights
    start : int
        start node ()

    Returns
    -------
    order_visited : list
        list containing order of nodes visited
    """
    parent = {node:-1 for node in graph}  # key --> visited node, value --> node used to discover key
    visited, stack = [], [start]
    order_visited = []
    depth = []
    print("graph", graph)
    depth_count = 0
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.append(current)
        for adjacent in graph[current]:
            adjacent_node = adjacent[0]
            stack.append(adjacent_node)
            if adjacent_node != start and parent[adjacent_node] == -1:
                parent[adjacent_node] = current
    print("parent",parent)
    # fill in order_visited with edges
    for i in range(len(visited)):
        if i == 0:
            order_visited.append((visited[i], visited[i]))
        else:
            order_visited.append((parent[visited[i]], visited[i]))
    print("order:", order_visited)
    return order_visited


def kruskals(G, N):
    root = list(range(N))
    steps = []
    added = []
    edges = edge_weights_labels
    edges.sort(key=lambda x: x[2])

    def find(x):
        if root[x] == x:
            return x

        root[x] = find(root[x])
        return root[x]

    def join(a, b):
        root[find(a)] = root[find(b)]

    order_vis = []

    for i in range(len(edges)):
        added = False
        a = edges[i][0]
        b = edges[i][1]
        wt = edges[i][2]

        if find(a) != find(b):
            join(a, b)
            added = True

        order_vis.append([edges[i], added])
    return order_vis


"""
Animation created using matplotlib animation function
"""


def update_bfs(itr):
    """
    Function used to animate bfs - uses an iterable to access certain sections of a list

    Parameters
    ----------
    itr : int
        An iterable
    """
    plt.clf()
    node_col = 'blue'
    order = bfs(adj_list, 0)

    targeted_index = itr % len(order)
    targeted_edges = [order[targeted_index]]
    targeted_nodes = [order[targeted_index][1]]
    already_visited_nodes = [0]
    already_visited_nodes.extend(item[1] for item in order[:targeted_index])
    already_visited_edges = order[:targeted_index]

    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=targeted_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=250, node_color='red')
    plt.tight_layout()


def update_dfs(itr):
    """
    DFS counterpart for previous function

    Parameters
    ----------
    itr : int
        An iterable
    """
    plt.clf()
    order = dfs(adj_list, 0)
    node_col = "blue"

    targeted_index = itr % len(order)
    targeted_nodes = [order[targeted_index][1]]
    targeted_edges = [order[targeted_index]]
    already_visited_nodes = [0]
    already_visited_nodes.extend(item[1] for item in order[:targeted_index])
    already_visited_edges = []


    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=targeted_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=250, node_color='red')
    nx.draw_networkx_labels(G, position)
    plt.tight_layout()


def update_mst(itr):
    """
    Meant to visualise kruskals
    Parameters
    ----------
    itr : int
        iterable
    """
    plt.clf()

    order = kruskals(edge_weights_labels, len(G.nodes))

    targeted_index = itr % len(order)
    current_edge = [(order[targeted_index][0][0], order[targeted_index][0][1])]
    show = order[targeted_index][1]
    current_node = []
    already_visited_nodes = []
    already_visited_edges = [tuple(edge[0][:2]) for edge in order[:targeted_index] if edge[1]]
    print(already_visited_edges)

    # draw
    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=current_edge, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color='blue')
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_labels(G, position)
    plt.tight_layout()

def update_dijkstra(itr):
    pass
