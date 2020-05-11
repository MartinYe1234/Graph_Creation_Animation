import sys

import pygame
import pygame.display as pydisplay
import pygame.mouse as pymouse
import pygame.draw as pydraw
from pygame.locals import *
from main import *

pygame.init()

"""Globals"""

button_unselected = (255, 255, 255)
not_selected_color = (0, 0, 255)
selected_color = (255, 0, 0)
selected_final_color = (0, 255, 0)

selected_algorithm = ""  # used for determining which algorithm to use


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

    def draw(self):
        if self.state != -1:
            pydraw.circle(screen, self.colour, self.position, 10)


class Edge:
    def __init__(self, u, v, colour):
        self.u = u
        self.v = v
        self.colour = colour
        x1, y1 = self.u.position
        x2, y2 = self.v.position
        self.weight = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        self.edge = (self.u, self.v, self.weight)

    def get_edge(self):
        return self.edge

    def get_edge_data(self):
        return self.u.name, self.v.name, self.weight

    def is_selected(self):  # sets edge as being selected if conditions are satisfied
        self.colour = selected_color

    def not_selected(self):
        self.colour = not_selected_color

    def draw(self):
        pydraw.line(screen, self.colour, self.u.position, self.v.position, 2)


class Graph:
    def __init__(self):
        self.graph = {}
        self.edge_list = []

    def add_node(self, node):
        self.graph[node] = []

    def add_bi_edge(self, edge):  # connects nodes u and v and adds a weight based on position

        self.graph[edge.u].append((edge.v, edge.weight))
        self.graph[edge.v].append((edge.u, edge.weight))

        self.edge_list.append(edge)
        self.edge_list = list(set(self.edge_list))  # insure no duplicates

    def add_non_bi_edge(self, u, v):
        self.graph[u].append(v)

    def del_node(self, node):  # remove node from graph as well as any edges connected to the node
        node.state = -1  # set to -1 meaning it should be ignored
        # all connecting edges must also be deleted
        edges_to_delete = []
        for edge in self.edge_list:
            if edge.u == node or edge.v == node:
                edges_to_delete.append(edge)
        while edges_to_delete:
            self.edge_list.remove(edges_to_delete.pop())

    def del_edge(self, edge):  # remove an edge between two nodes
        self.edge_list.remove(edge)

        self.graph[edge.u].remove((edge.v, edge.weight))
        self.graph[edge.v].remove((edge.u, edge.weight))

    def get_graph(self):  # includes "deleted nodes"
        return self.graph

    def get_nodes(self):  # returns the adjacency list without "deleted nodes"
        nodes = {}
        for node in self.graph:
            if node.state != -1:
                nodes[node.name] = set()
                for adjacent in self.graph[node]:
                    if adjacent[0].state != -1:
                        nodes[node.name].add((adjacent[0].name, adjacent[1]))
        return nodes

    def get_edges(self):  # returns all edges as tuple like this : (u, v, weight)
        # (v, u, weight) and (u, v, weight) will not be treated as the same
        edges = []
        for edge in self.edge_list:
            edges.append((edge.u.name, edge.v.name, edge.weight))
        return list(set(edges))

    def get_positions(self):  # returns dictionary of each nodes position without "deleted nodes"
        pos = {}
        for node in self.graph:
            if node.name not in pos.keys() and node.state != -1:
                pos[node.name] = node.position
        return pos

    def not_within_min(self, mouse_pos):
        """
        Nodes can only be added if they are a certain distance away from other nodes, deleted nodes are not counted

        Parameters
        ----------
        mouse_pos : tuple
            coordinates of mouse click

        Returns
        -------
        not_within : boolean
            true if mouse click was far enough away (> min_distance) from a node, false otherwise
        """
        not_within = True
        min_distance = 20
        x_mpos, y_mpos = mouse_pos[0], mouse_pos[1]
        for node in self.graph:
            if node.state != -1:
                x_node, y_node = node.position
                distance = ((x_node - x_mpos) ** 2 + (y_node - y_mpos) ** 2) ** .5
                if distance < min_distance:
                    not_within = False
                    if add_node_mode != 1:
                        node.is_selected()  # set node as being selected
        return not_within

    def draw(self):
        for node in self.graph:
            node.draw()
        for edge in self.edge_list:
            edge.draw()


my_graph = Graph()

screen = pydisplay.set_mode((1400, 800))  # display surface for graph creation
graph_screen = pygame.Rect((120, 0, 1400, 800))
font = pygame.font.Font(None, 28)  # font to use
add_node_mode = 1  # differentiate between adding nodes or edges


class Button(pygame.Rect):

    def __init__(self, x, y, width, height, text, colour, shown):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.colour = colour
        self.shown = shown

    def draw(self):
        if self.shown:
            button_text = font.render(self.text, True, (0, 0, 0))
            width = button_text.get_width()
            height = button_text.get_height()
            pygame.draw.rect(screen, self.colour, self)
            screen.blit(button_text, (self.x - (width - self.width) / 2, self.y - (height - self.height) / 2))

    def is_clicked(self, mouse_pos):  # returns whether the button has been selected or not
        # handles what happens if a certain button is clicked
        global add_node_mode, selected_algorithm
        # add_node_mode = 0 --> adding edges
        # add_node_mode = 1 --> adding nodes
        # add_node_mode = 2 --> deleting nodes
        # add_node_mode = 3 --> deleting edges
        if self.collidepoint(mouse_pos):
            if self.text == "Add Edge":
                add_node_mode = 0
            elif self.text == "Add Node":
                add_node_mode = 1
            elif self.text == "Del Node":
                add_node_mode = 2
            elif self.text == "Del Edge":
                add_node_mode = 3

            elif self.text == "Selection":  # open selection menu
                bfs_mode.shown = 1
                dfs_mode.shown = 1
                dij_mode.shown = 1
                kru_mode.shown = 1

            elif self.text == "Bfs":
                selected_algorithm = self.text
            elif self.text == "Dfs":
                selected_algorithm = self.text
            elif self.text == "Dijkstra":
                selected_algorithm = self.text
            elif self.text == "Kruskal":
                selected_algorithm = self.text

            elif self.text == "Run":  # Run button is responsible for animating the algorithms
                positions = my_graph.get_positions()
                nodes = [node for node in my_graph.get_nodes().keys()]
                edges = my_graph.get_edges()
                create_networkx_graph(positions, nodes, edges)
                fig, ax = plt.subplots(figsize=(14, 7))

                if selected_algorithm == "":
                    print("UH OH")
                elif selected_algorithm == "Bfs":
                    ani_mst = mpa.FuncAnimation(fig, update_bfs, interval=500, repeat=True)
                elif selected_algorithm == "Dfs":
                    ani_mst = mpa.FuncAnimation(fig, update_dfs, interval=500, repeat=True)
                elif selected_algorithm == "Dijkstra":
                    ani_mst = mpa.FuncAnimation(fig, update_dijkstra, interval=500, repeat=True)
                elif selected_algorithm == "Kruskal":
                    ani_mst = mpa.FuncAnimation(fig, update_mst, interval=500, repeat=True)
                plt.show()

            self.colour = selected_color
            return True
        self.colour = button_unselected
        return False


add_node = Button(10, 10, 100, 50, "Add Node", button_unselected, 1)
add_edge = Button(10, 70, 100, 50, "Add Edge", button_unselected, 1)
del_node = Button(10, 130, 100, 50, "Del Node", button_unselected, 1)
del_edge = Button(10, 190, 100, 50, "Del Edge", button_unselected, 1)
select_algorithm = Button(10, 250, 100, 50, "Selection", button_unselected, 1)
bfs_mode = Button(10, 310, 100, 50, "Bfs", button_unselected, 0)
dfs_mode = Button(10, 370, 100, 50, "Dfs", button_unselected, 0)
dij_mode = Button(10, 430, 100, 50, "Dijkstra", button_unselected, 0)
kru_mode = Button(10, 490, 100, 50, "Kruskal", button_unselected, 0)
run_visual = Button(10, 740, 100, 50, "Run", button_unselected, 1)
buttons = [add_node, add_edge, del_node, del_edge, select_algorithm, bfs_mode, dfs_mode, dij_mode, kru_mode, run_visual]  # list of all buttons
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
                # adding nodes -> must be far enough away, on screen, correct mode
                if my_graph.not_within_min(mouse_pos) and graph_screen.collidepoint(mouse_pos) and add_node_mode == 1:
                    new_node = Node(node_name, not_selected_color, mouse_pos, 0)
                    my_graph.add_node(new_node)
                    node_name += 1
                # adding edges -> a node must be selected and correct mode
                if not my_graph.not_within_min(mouse_pos) and not add_node_mode:
                    for node in my_graph.get_graph():
                        if primary == -1 and node.state == 1:  # if no primary node has been selected
                            primary = node
                        elif primary != -1 and node.state == 1 and primary != node:  # cannot make a edge with itself
                            secondary = node
                        if primary != -1 and secondary != -1:  # add the edge and reset primary and secondary
                            new_edge = Edge(primary, secondary, not_selected_color)
                            if new_edge.get_edge_data() not in my_graph.get_edges():  # no duplicate edges allowed
                                my_graph.add_bi_edge(new_edge)

                            primary.not_selected()
                            secondary.not_selected()
                            primary = -1
                            secondary = -1
                # deleting nodes -> correct mode, and node selected
                if add_node_mode == 2 and not my_graph.not_within_min(mouse_pos):
                    for node in my_graph.get_graph():  # find which node was selected
                        if node.state == 1:
                            my_graph.del_node(node)
                # deleting edges -> correct mode, edge selected NEEDS FIXING
                if add_node_mode == 3 and not my_graph.not_within_min(mouse_pos):
                    for node in my_graph.get_graph():
                        if primary == -1 and node.state == 1:  # if no primary node has been selected
                            primary = node
                        elif primary != -1 and node.state == 1 and primary != node:  # cannot make a edge with itself
                            secondary = node
                        if primary != -1 and secondary != -1:  # add the edge and reset primary and secondary

                            for edge in my_graph.edge_list:
                                if (edge.u is primary and edge.v is secondary) or (edge.v is primary and edge.u is secondary):
                                    my_graph.del_edge(edge)

                            primary.not_selected()
                            secondary.not_selected()
                            primary = -1
                            secondary = -1

        for button in buttons:  # draw all buttons
            button.draw()
        my_graph.draw()
        pydisplay.update()


main()
