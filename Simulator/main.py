# -*- coding: utf-8 -*-

import random 
from random import choices
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from methods import *
from eval import *

"""g=random_Bernoulli_graph_gen(15, 0.1)
nx.draw_circular(g, with_labels=True)
plt.show()"""

d=[0.5,0,0,0,0,0.5]

g=random_1_from_distrib_incremental(15, d)
nx.draw_circular(g, with_labels=True)
plt.show()

#draw_edges_growth(random_1_from_distrib, d, 10, 200, 10)

"""g=nx.barbell_graph(8, 4)
nx.draw_circular(g, with_labels=True)
plt.show()"""

print(detect_communities(g,0.25))