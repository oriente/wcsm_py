'''
Created on November 11, 2012
Modified on November 14, 2012
Calculate Paths for time-varying graphs from mobility trace
@author: dzhang

'''
import math
import networkx as nx
import matplotlib.pyplot as plt
from Attacks import Attacks
from CalculateCentralityRT import CalculateCentrality


num_of_node = 20
matrix_per_timestep = ([[(0, 4), (0, 11), (0, 14), (0, 17), (0, 19), (1, 7), (1, 8), (1, 15), (1, 18),
(2, 3), (2, 5), (2, 15), (3, 5), (3, 6), (3, 7), (3, 9), (3, 13), (3, 15), (4,
9), (4, 10), (4, 12), (4, 17), (5, 15), (6, 7), (6, 9), (6, 10), (6, 12), (6,
13), (6, 15), (6, 18), (7, 10), (7, 13), (7, 15), (7, 18), (8, 16), (9, 10),(9,
12), (9, 13), (10, 12), (10, 13), (10, 17), (10, 18), (11, 19), (12, 13), (12,
17), (13, 15), (13, 18), (14, 19), (15, 18)]])
cc = CalculateCentrality(20, matrix_per_timestep[0])
sink = range(4)
#print cc.calculate_a_closeness(sink)
#print cc.calculate_close(sink)
print "a_closeness"
aclose_atk = Attacks(20, matrix_per_timestep, cc.calculate_a_closeness(sink))
aclose_atk.a_attack(sink)
print aclose_atk.get_aflowrobust()

print "closeness"
close_atk = Attacks(20, matrix_per_timestep, cc.calculate_close(sink))
close_atk.a_attack(sink)
print close_atk.get_aflowrobust()
#num_of_node = 20 
'''
G = nx.Graph()
G.add_nodes_from(range(num_of_node))
G.add_edges_from(matrix_per_timestep[0])
pos = nx.spring_layout(G, iterations=10, scale=1)

for i in range(num_of_node):
    nx.draw_networkx_nodes(G, pos, nodelist=[i], linewidths=0,node_color='#0022b4', node_size=360)

for j in range(len(matrix_per_timestep)):
    edge = matrix_per_timestep[0][j][0:2]
    nx.draw_networkx_edges(G,pos,edgelist=[edge],width=2,edge_color="#000f0e",alpha=1)

nx.draw_networkx_labels(G, pos, font_size=10, font_color='w')
plt.savefig("20node.png", dpi=200)
'''
