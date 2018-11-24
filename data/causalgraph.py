
""" Randomly generate directed graphs to use as causal graph
"""

import numpy as np
import networkx as nx
import random

class cgraph:
    """ Causal graph simulator
    """
    def __init__(self,
                number_of_X,
                density = 1,
                edges = "random",
                weights = None):

        self.nvars = int(number_of_X)

        if self.nvars <= 0:
            raise ValueError("input number_of_X must be a positive integer")

        if not 0 < density <= 1:
            raise ValueError("Density must be in the interval [0,1]")

        self.ncon = np.ceil(density* ((self.nvars - 1)*(self.nvars))/2)
        self.nodelist = [i for i in range(self.nvars)] + ['Y']
        self.G = nx.DiGraph()

        # Add X-variables 0-nvars and Y
        self.G.add_nodes_from(self.nodelist)
        if edges == "random":
            self.edges, self.weights = self.random_edges()
            for e,c in zip(self.edges, self.weights):
                self.G.add_edge(*e, weight = c)

        else:
            self.edges,self.weights = edges, weights
            for e,c in zip(self.edges, self.weights):
                self.G.add_edge(*e, weight = c)


    def random_edges(self):
        """ Randomly constructs causal edges between variables
        """
        e = list()
        c = list()

        while len(e) < self.ncon:
            corr = np.random.uniform(-1,1)
            begin = random.choice(self.nodelist)
            end = random.choice(self.nodelist)

            if begin == 'Y' \
            or begin == end \
            or (begin, end) in e \
            or (end, begin) in e:
                continue

            # Ensures result is a DAG
            if len(list(nx.simple_cycles(nx.DiGraph(e + [(begin, end)])))) > 0:
                continue

            e.append((begin, end))
            c.append(corr)

        return e,c


    def draw_graph(self):
        """ Plot the simulated graph
        """
        fig = nx.draw(self.G, with_labels = True, pos = nx.circular_layout(self.G))
        return fig
