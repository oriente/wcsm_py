#!/usr/bin/env python
import matplotlib.pyplot as plt
import networkx as nx
import a_centrality as ac
import math
from CalculateCentrality import CalculateCentrality
def a_flow_robust(node_num, graph, sink):
    flows = 0.0
    comps = nx.connected_components(graph)
    sinkl = sink[:]
    #print len(comps)
    for comp in comps:
        ns = 0 # number of sink in each component
        for s in sinkl:
            if s in comp:
              ns += 1
              sinkl.remove(s)
        flows = flows + len(comp) * ns
    total_flows = node_num * len(sink)
    a_flow_robust = flows/total_flows
    print a_flow_robust 


'''
G=nx.Graph()
adj = [(1, 2),(1, 3), (2, 3), (2, 4), (4, 5), (5, 6), (7, 8)]
G.add_edges_from(adj)
sink_node = [2, 8]
a_flow_robust(len(G.nodes()), G, sink_node)
print sink_node
'''
G = nx.Graph()
adj = [(1, 2, 1),(1, 3, 0.4), (2, 3, 0.5), (2, 5, 0.6), (3, 5, 0.2), (5, 6, 1),\
(7, 8, 0.4)]
adj_inv = []
for i in range (0,len(adj)):
	if adj[i][2]== 0:
		a  = 100000000
	else:
		a_weight = math.pow(1/adj[i][2], 1)
		a = (adj[i][0], adj[i][1], a_weight)
		adj_inv.append(a)

G.add_weighted_edges_from(adj_inv)
close = ac.a_closeness_centrality(G, Sink=[1, 6])
print 'a_loseness: ', close
