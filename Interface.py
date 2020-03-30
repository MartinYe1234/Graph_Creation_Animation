import sys

import pygame
import pygame.display as pydisplay
import pygame.mouse as pymouse
import pygame.draw as pydraw
from pygame.locals import *

pygame.init()


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node, position):
        self.graph[node] = [("pos", position)]

    def add_bi_edge(self, u, v):  # connects nodes u and v and adds a weight based on position
        x1, y1 = self.graph[u][0][1]
        x2, y2 = self.graph[v][0][1]
        weight = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def add_non_bi_edge(self, u, v):
        self.graph[u].append(v)

    def draw(self):
        for node in self.graph:
            start = self.graph[node][0][1]  # begin at the node itself
            pydraw.circle(screen, (0, 0, 255), self.graph[node][0][1], 10)  # draw nodes
            end = (100, 100)  # ends at every node adjacent to it
            pydraw.line(screen, (30, 144, 255), start, end, 2)  # draw edges

    def get_nodes(self):  # returns nodes of the graph with their positions
        nodes = {}
        for node in self.graph:
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
            whether or not the node about to be added is violating US airspace and needs to be shot down
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


my_graph = Graph()
screen = pydisplay.set_mode((1400, 800))  # display surface for graph creation
graph_screen = pygame.Rect((120, 0, 1400, 800))
font = pygame.font.Font(None, 28)  # font to use
add_node_mode = 1   # differentiate between adding nodes or edges


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
        screen.blit(button_text, (self.x-(width-self.width)/2, self.y-(height-self.height)/2))

    def is_clicked(self, mouse_pos):  # returns whether the button has been selected or not
        global add_node_mode
        if self.collidepoint(mouse_pos):
            if self.text == "Add Edge":
                add_node_mode = 0
            elif self.text == "Add Node":
                add_node_mode = 1
            return True
        return False


add_node = Button(10, 10, 100, 50, "Add Node")
add_edge = Button(10, 70, 100, 50, "Add Edge")
buttons = [add_node, add_edge]  # list of all buttons


def main():
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
                    print(button.is_clicked(event.pos))

        if pymouse.get_pressed()[0]:
            mouse_pos = pymouse.get_pos()
            if my_graph.not_within_min(mouse_pos) and graph_screen.collidepoint(mouse_pos) and add_node_mode:  # only if node is within graph screen and far enough away
                my_graph.add_node(node_name, mouse_pos)
                node_name += 1
                print(my_graph.get_nodes())

        for button in buttons:  # draw all buttons
            button.draw()
        my_graph.draw()
        pydisplay.update()


main()
