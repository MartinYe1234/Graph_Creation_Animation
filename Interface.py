import sys

import pygame
import pygame.display as pydisplay
import pygame.mouse as pymouse
import pygame.draw as pydraw
from pygame.locals import *
from main import *

pygame.init()

"""Globals
different possible states a node/ edge could be in:
final = 2, 
selected = 1
not_selected = 0
"""
not_selected_color = (0, 0, 255)
selected_color = (255, 0, 0)
selected_final_color = (0, 255, 0)
selected_algorithm = ""

class Node:
    def __init__(self, name, colour, position, state):
        self.name = name
        self.colour = colour
        self.position = position
        self.state = state

    def is_selected(self):  # sets node as being selected if conditions are satisfied
        self.state = 1
        self.colour = selected_color

    def not_selected(self):
        self.state = 0
        self.colour = not_selected_color


class Edge:
    def __init__(self, u, v, colour, state):
        self.u = u
        self.v = v
        self.colour = colour
        self.state = state
        x1, y1 = self.u.position
        x2, y2 = self.v.position
        self.weight = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        self.edge = (u, v, self.weight)

    def get_edge(self):
        return self.edge

    def get_edge_data(self):
        return self.u.name, self.v.name, self.weight

    def is_selected(self):  # sets edge as being selected if conditions are satisfied
        self.state = 1
        self.colour = selected_color

    def not_selected(self):
        self.state = 0
        self.colour = not_selected_color


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[node] = []

    def add_bi_edge(self, edge):  # connects nodes u and v and adds a weight based on position

        self.graph[edge.u].append((edge.v, edge.weight))
        self.graph[edge.u].append((edge.v, edge.weight))

    def add_non_bi_edge(self, u, v):
        self.graph[u].append(v)

    def draw(self):
        for node in self.graph:
            start = node.position  # begin at the node itself
            pydraw.circle(screen, node.colour, start, 10)  # draw nodes
            # draw edges
            for adjacent in self.graph[node]:
                end = adjacent[0].position
                pydraw.line(screen, adjacent[0].colour, start, end, 2)

    def get_graph(self):
        return self.graph

    def get_nodes(self):  # returns nodes of the graph with their positions as well as neighbours
        nodes = {}
        for node in self.graph:
            if node.name not in nodes.keys():
                nodes[node.name] = set()
            for neighbour in self.graph[node]:
                nodes[node.name].add((neighbour[0].name, neighbour[1]))
        return nodes

    def get_edges(self):  # returns all edges as tuple like this : (u, v, weight)
        # (v, u, weight) and (u, v, weight) will not be treated as the same
        edges = []
        for node in self.graph:
            for adjacent in self.graph[node]:
                edges.append((node.name, adjacent[0].name, adjacent[1]))
        return edges

    def get_positions(self):  # returns dictionary of each nodes position
        pos = {}
        for node in self.graph:
            if node.name not in pos.keys():
                pos[node.name] = node.position
        return pos

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
            whether or not the node about to be added is violating US airspace and needs to be shot down
        """
        not_within = True
        min_distance = 20
        x_mpos, y_mpos = mouse_pos[0], mouse_pos[1]
        for node in self.graph:
            x_node, y_node = node.position
            distance = ((x_node - x_mpos) ** 2 + (y_node - y_mpos) ** 2) ** .5
            if distance < min_distance:
                not_within = False
                if not add_node_mode:
                    node.is_selected()  # set node as being selected
        return not_within

my_graph = Graph()

screen = pydisplay.set_mode((1400, 800))  # display surface for graph creation
graph_screen = pygame.Rect((120, 0, 1400, 800))
font = pygame.font.Font(None, 28)  # font to use
add_node_mode = 1  # differentiate between adding nodes or edges


class Button(pygame.Rect):

    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    def draw(self):
        button_text = font.render(self.text, True, (0, 0, 0))
        width = button_text.get_width()
        height = button_text.get_height()
        pygame.draw.rect(screen, (255, 255, 255), self)
        screen.blit(button_text, (self.x - (width - self.width) / 2, self.y - (height - self.height) / 2))

    def is_clicked(self, mouse_pos):  # returns whether the button has been selected or not
        global add_node_mode
        if self.collidepoint(mouse_pos):
            if self.text == "Add Edge":
                add_node_mode = 0
            elif self.text == "Add Node":
                add_node_mode = 1
            elif self.text == "Run":
                positions = my_graph.get_positions()
                nodes = [node for node in my_graph.get_nodes().keys()]
                edges = my_graph.get_edges()
                print("nodes",nodes)
                create_networkx_graph(positions, nodes, edges)

                plt.show()
            return True
        return False


add_node = Button(10, 10, 100, 50, "Add Node")
add_edge = Button(10, 70, 100, 50, "Add Edge")
run_visual = Button(10,130, 100, 50,"Run")
buttons = [add_node, add_edge, run_visual]  # list of all buttons
# used to add edges
primary = -1
secondary = -1


def main():
    global primary, secondary, node_name
    running = True
    pydisplay.init()
    pydisplay.set_caption("Create your graph")
    # used to name nodes
    node_name = 0
    while running:
        pygame.draw.rect(screen, (192, 192, 192), graph_screen)  # draw background for graph screen
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):  # exit screen check
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # button click check
                for button in buttons:  # check if a button is clicked
                    button.is_clicked(event.pos)

                mouse_pos = pymouse.get_pos()
                # nodes are added if the satisfy the following: within the screen, far enough from other nodes, add_node_mode is true
                if my_graph.not_within_min(mouse_pos) and graph_screen.collidepoint(mouse_pos) and add_node_mode:
                    new_node = Node(node_name, not_selected_color, mouse_pos, 0)
                    my_graph.add_node(new_node)
                    node_name += 1
                # to add edges a node must be selected and add edge mode must be on
                if not my_graph.not_within_min(mouse_pos) and not add_node_mode:
                    for node in my_graph.get_graph():
                        if primary == -1 and node.state == 1:  # if no primary node has been selected
                            primary = node
                        elif primary != -1 and node.state == 1 and primary != node:  # cannot make a edge with itself
                            secondary = node
                        if primary != -1 and secondary != -1:  # add the edge and reset primary and secondary
                            new_edge = Edge(primary, secondary, not_selected_color, 0)
                            if new_edge.get_edge_data() not in my_graph.get_edges():  # no duplicate edges allowed
                                my_graph.add_bi_edge(new_edge)

                            primary.not_selected()
                            secondary.not_selected()
                            primary = -1
                            secondary = -1

        for button in buttons:  # draw all buttons
            button.draw()
        my_graph.draw()
        pydisplay.update()


main()
