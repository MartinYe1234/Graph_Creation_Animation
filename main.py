from Interface import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as mpa


hpush = __import__("heapq").heappush
hpop = __import__("heapq").heappop

"""Create networkX graph to visualise"""

adj_list = {}
# animation is based off of the concept from:
# https://stackoverflow.com/questions/43646550/how-to-use-an-update-function-to-animate-a-networkx-graph-in-matplotlib-2-0-0?rq=1
def create_networkx_graph(p, nodes, edges):
    global G, position, edge_weights_labels
    G = nx.Graph()
    print("type=", type(G))
    G.add_nodes_from(nodes)
    # set position of every node
    nx.set_node_attributes(G, p, 'pos')
    position = nx.get_node_attributes(G, 'pos')
    print("position of nodes", position)
    # add all edges
    G.add_weighted_edges_from(edges)
    # labels for edge weights
    edge_weights_labels = []

    # fill adjacency list
    for node in nodes:
        adj_list[node] = []
    for edge in edges:
        node = edge[0]
        connected_node = edge[1]
        # generate weights by calculating distance between the two nodes
        x1, y1 = position[node][0], position[node][1]
        x2, y2 = position[connected_node][0], position[connected_node][1]
        # The weight is the euclidean distance between the coordinates
        # of the nodes divided by 10 and rounded to the nearest tenth.
        weight = int(round((((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5), 1))
        adj_list[node].append([weight, connected_node])
        adj_list[connected_node].append([weight, node])
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
    order_visited = [(start, start)]
    # while there is something in the queue
    while queue:
        current_node = queue[0]
        # for each adjacent node to the current node
        for neighbour in graph[current_node]:
            adjacent_node = neighbour[1]
            # if the vertex has not been visited yet
            if adjacent_node not in bfs_visited:
                order_visited.append((current_node, adjacent_node))
                # add adjacent (neighbour) node to queue
                queue.append(adjacent_node)
                # mark as visited
                bfs_visited.append(adjacent_node)
        queue.pop(0)
    return order_visited


def dfs(graph, current, parent, visited, path):
    """
        Runs dfs on a selected node (0 by default)

        Parameters
        ----------
        graph : dict
            keys are nodes, values are lists containing edges in the form of (weight, adjacent)
        current : int
            current node dfs is being run on
        parent : int
            parent node
        visited : list
            list meant to contain all visited nodes
        path : list
            list meant to store order nodes were visited in, including back tracking

        Returns
        -------
        path : list
            List of nodes visited in order, including back tracking
        """
    if current in visited:
        return
    visited.append(current)
    path.append(current)
    for adj in graph[current]:
        adjacent_node = adj[1]
        dfs(graph, adjacent_node, current, visited, path)
    if parent != -1:
        path.append(parent)
    return path


def update_dfs(itr, start):
    """
    DFS counterpart for previous function

    Parameters
    ----------
    itr : int
        An iterable
    """
    plt.clf()
    path = dfs(adj_list, start, -1, [], [])
    order = [(start, start)]  # use path to create order
    for i in range(len(path)-1):
        new_edge = (path[i], path[i+1])
        reversed_edge = (path[i+1], path[i])
        if reversed_edge not in order:
            order.append(new_edge)
    node_col = "blue"

    targeted_index = itr % len(order)
    targeted_nodes = [order[targeted_index][1]]
    targeted_edges = [order[targeted_index]]
    already_visited_nodes = [start]
    already_visited_nodes.extend(item[1] for item in order[:targeted_index])
    already_visited_edges = order[:targeted_index]

    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=targeted_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=250, node_color='red')
    nx.draw_networkx_labels(G, position)  # label nodes
    plt.tight_layout()


def kruskals(G, N):
    root = list(range(N))
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


INF = int(2e9)


def dijk(graph, start):
    # G is in the format {node : [[neighbor, weight]]}
    # Flip G to be in the format {node : [[weight, neighbor]]}
    order_visited = [start]
    dists = dict(zip(list(graph.keys()), [INF for i in range(len(graph.keys()))]))
    heap = [(0, start)]
    dists[start] = 0
    animation_dists = [dists.copy()]
    while heap:
        cur = hpop(heap)[1]
        for wt, node in graph[cur]:
            if dists[cur] + wt < dists[node]:
                dists[node] = dists[cur] + wt
                hpush(heap, (dists[node], node))
                order_visited.append(node)
                animation_dists.append(dists.copy())
    return animation_dists, order_visited


"""
Animation created using matplotlib animation function
"""


def update_dijk(itr, start):
    plt.clf()
    node_col = 'blue'
    order, node_order = dijk(adj_list, start)
    targeted_index = itr % len(order)
    print("order=",order)
    print("node_order = ", node_order)

    current_label = order[targeted_index]
    for node in current_label:
        if current_label[node] == 2e9:
            current_label[node] = "Inf"
    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)

    targeted_nodes = [node_order[targeted_index]]
    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=250, node_color='red')

    nx.draw_networkx_labels(G, position)  # label nodes
    # position of weight labels (above node)
    weight_pos = {node: (position[node][0], position[node][1] + 12) for node in position}
    nx.draw_networkx_labels(G, weight_pos, labels=current_label)  # label nodes


def update_bfs(itr, start):
    """
    Function used to animate bfs - uses an iterable to access certain sections of a list

    Parameters
    ----------
    itr : int
        An iterable
    """
    plt.clf()
    node_col = 'blue'
    order = bfs(adj_list, start)

    targeted_index = itr % len(order)
    targeted_edges = [order[targeted_index]]
    targeted_nodes = [order[targeted_index][1]]
    already_visited_nodes = [start]
    already_visited_nodes.extend(item[1] for item in order[:targeted_index])
    already_visited_edges = order[:targeted_index]
    nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
    nx.draw_networkx_edges(G, position, edgelist=targeted_edges, width=4, edge_color='red', alpha=1)
    nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='orange', alpha=1)

    nx.draw_networkx_nodes(G, position, node_size=250, node_color=node_col)
    nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
    nx.draw_networkx_nodes(G, position, nodelist=targeted_nodes, node_size=250, node_color='red')
    nx.draw_networkx_labels(G, position)  # label nodes
    plt.tight_layout()


def update_mst(itr, start):
    """
    Meant to visualise kruskals
    Parameters
    ----------
    itr : int
        iterable
    """
    plt.clf()

    order = kruskals(edge_weights_labels, len(G.nodes)) + [(-1, -1)]

    targeted_index = itr % len(order)
    if targeted_index == len(order) - 1:


        already_visited_nodes = []
        already_visited_edges = [tuple(edge[0][:2]) for edge in order[:targeted_index] if edge[1]]
        current_edge = []
        nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
        nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='pink', alpha=1)

        nx.draw_networkx_nodes(G, position, node_size=250, node_color='pink')
        nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='purple')
        nx.draw_networkx_labels(G, position)  # label nodes

    else:
        current_edge = [(order[targeted_index][0][0], order[targeted_index][0][1])]
        show = order[targeted_index][1]
        already_visited_nodes = []
        already_visited_edges = [tuple(edge[0][:2]) for edge in order[:targeted_index] if edge[1]]
        print(already_visited_edges)

        # draw
        nx.draw_networkx_edges(G, position, width=2, alpha=0.5)
        nx.draw_networkx_edges(G, position, edgelist=already_visited_edges, width=4, edge_color='red', alpha=1)
        nx.draw_networkx_edges(G, position, edgelist=current_edge, width=4, edge_color='orange', alpha=1)

        nx.draw_networkx_nodes(G, position, node_size=250, node_color='blue')
        nx.draw_networkx_nodes(G, position, nodelist=already_visited_nodes, node_size=250, node_color='orange')
        nx.draw_networkx_labels(G, position)  # label nodes

    plt.tight_layout()
