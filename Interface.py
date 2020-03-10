import sys

import pygame
import pygame.display as pydisplay
import pygame.mouse as pymouse
import pygame.draw as pydraw
from pygame.locals import *


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node, position):
        self.graph[node] = position

    def add_bi_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def add_nonbi_edge(self, u, v):
        self.graph[u].append(v)

    def draw(self):
        for node in self.graph:
            pydraw.circle(screen, (0, 0, 255), self.graph[node], 10)

    def get_nodes(self): # returns nodes with their positions
        nodes = {}
        for node in self.graph.keys():
            if node not in nodes.keys():
                nodes[node] = ()
            nodes[node] = self.graph[node]
        return nodes

    def get_edges(self):
        pass

    def not_within_min(self, mouse_pos):
        """
        Nodes can only be added if they are a certain distance away from other nodes

        Parameters
        ----------
        mouse_pos : tuple
            coordinates of mouse click

        Returns
        -------
        not_within : boolean
            should node be added
        """
        not_within = True
        min_distance = 20
        x_mpos, y_mpos = mouse_pos[0], mouse_pos[1]
        for node in self.get_nodes():
            x_node, y_node = self.get_nodes()[node]
            distance = ((x_node-x_mpos)**2+(y_node-y_mpos)**2)**.5
            if distance < min_distance:
                not_within = False
        return not_within

    def bfs(self, start):
        """
        Runs bfs on a graph with the purpose of visualising it

        Parameters
        ----------
        start : int
            Starting node

        Returns
        -------
        order_visited : list
            list containing order of nodes visited
        """
        print(self.graph.keys())
        queue = [start]
        bfs_visited = [0 for i in range(len(self.graph.keys()))]
        # mark as visited
        bfs_visited[start] = 1
        # store order of visited nodes
        order_visited = []
        # while there is something in the queue
        while queue:
            current_node = queue[0]
            # for each adjacent node to the current node
            for neighbour in self.graph[current_node]:
                adjacent_node = neighbour[0]
                # if the vertex has not been visited yet
                if bfs_visited[adjacent_node] == 0:
                    order_visited.append((current_node, adjacent_node))
                    # add adjacent (neighbour) node to queue
                    queue.append(adjacent_node)
                    # mark as visited
                    bfs_visited[adjacent_node] = 1
            queue.pop(0)
        return order_visited


my_graph = Graph()
screen = pydisplay.set_mode((1000, 800))


def main():
    pygame.init()
    running = True
    pydisplay.init()
    node_name = 0
    while running:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
        if pymouse.get_pressed()[0]:
            if my_graph.not_within_min(pymouse.get_pos()):
                my_graph.add_node(node_name, pymouse.get_pos())
                node_name += 1
                print(my_graph.get_nodes())
        my_graph.draw()
        pydisplay.update()


main()