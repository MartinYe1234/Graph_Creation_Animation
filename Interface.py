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
        self.graph[node] = [("pos", position)]

    def add_bi_edge(self, u, v):    # connects nodes u and v and adds a weight based on position
        x1, y1 = self.graph[u][0][1]
        x2, y2 = self.graph[v][0][1]
        weight = ((x1-x2)**2+(y1-y2)**2)**0.5
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def add_non_bi_edge(self, u, v):
        self.graph[u].append(v)

    def draw(self):
        for node in self.graph:
            pydraw.circle(graph_screen, (0, 0, 255), self.graph[node][0][1], 10)

    def get_nodes(self):  # returns nodes of the graph with their positions
        nodes = {}
        for node in self.graph.keys():
            if node not in nodes.keys():
                nodes[node] = []
            nodes[node].append(self.graph[node][0])
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
            x_node, y_node = self.get_nodes()[node][0][1]
            distance = ((x_node - x_mpos) ** 2 + (y_node - y_mpos) ** 2) ** .5
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
graph_screen = pydisplay.set_mode((1000, 800))    # display surface for graph creation


class Button(pygame.Rect):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def draw(self):
        pygame.draw.rect(graph_screen, (255, 255, 255), self)

    def is_clicked(self, mouse_pos):  # returns whether the button has been selected or not
        if self.collidepoint(mouse_pos):
            return True
        return False


add_node = Button(10, 10, 100, 50)
add_edge = Button(10, 70, 100,50)
buttons = [add_node, add_edge]    # list of all buttons

def main():
    pygame.init()
    running = True
    pydisplay.init()
    pydisplay.set_caption("Create your graph")
    # used to name nodes
    node_name = 0
    while running:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):  # exit screen check
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # button click check
                for button in buttons:  # check if a button is clicked
                    button.is_clicked(event.pos)

        if pymouse.get_pressed()[0]:
            if my_graph.not_within_min(pymouse.get_pos()):
                my_graph.add_node(node_name, pymouse.get_pos())
                node_name += 1
                print(my_graph.get_nodes())

        for button in buttons:  # draw all buttons
            button.draw()
        my_graph.draw()
        pydisplay.update()


main()
