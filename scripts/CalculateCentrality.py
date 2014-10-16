#!/usr/bin/env python

import sys
import networkx as nx
import math
import numpy
import random
import a_centrality as ac

class CalculateCentrality:
    # python list is a very special data structure. within
    # the class, all the new objects shares the same ptr addr

    def __init__(self, n_node, agg_list):
        self.node_num = n_node
        self.aggregated_list = agg_list
        self.graph_inv = []

    def calculate_degree(self):
        degree_attack = []
        G = nx.Graph()
        G.add_nodes_from(range(self.node_num))
        G.add_weighted_edges_from(self.aggregated_list)
        degree = G.degree(weight='weight')
        dgr_sort = sorted(degree, key=degree.__getitem__, reverse=True)
        degree_attack.append(dgr_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G.remove_node(dgr_sort[0])
            degree = G.degree(weight='weight')
            dgr_sort = sorted(degree, key=degree.__getitem__, reverse=True)
            degree_attack.append(dgr_sort[0])
        return degree_attack

    def calculate_eigenvector(self):
        eigen_attack = []
        G = nx.Graph()
        G.add_nodes_from(range(self.node_num))
        G.add_weighted_edges_from(self.aggregated_list)
        eigen = nx.eigenvector_centrality_numpy(G)
        eigen_sort = sorted(eigen, key=eigen.__getitem__, reverse=True)
        eigen_attack.append(eigen_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G.remove_node(eigen_sort[0])
            eigen = nx.eigenvector_centrality_numpy(G)
            eigen_sort = sorted(eigen, key=eigen.__getitem__, reverse=True)
            eigen_attack.append(eigen_sort[0])
        return eigen_attack

    def invert_weight(self):
        # invert weight of the graph for betweenness and closeness
        for i in range (0,len(self.aggregated_list)):
            # aggregrated_list[i][2] cannot be equal to 0
            a_weight = math.pow(1/self.aggregated_list[i][2], 1)
            a = (self.aggregated_list[i][0], self.aggregated_list[i][1],
            a_weight)
            self.graph_inv.append(a)
    
    def calculate_betweenness(self):
        # calculate betweenness adptively
        #print self.graph_inv
        betweenness_attack = []
        G_inv = nx.Graph()
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(self.graph_inv)
        betweenness = nx.betweenness_centrality(G_inv, weight='weight')
        betweenness_sort = sorted(betweenness, key=betweenness.__getitem__,
        reverse=True)
        betweenness_attack.append(betweenness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(betweenness_sort[0])
            betweenness = nx.betweenness_centrality(G_inv, weight='weight')
            betweenness_sort = sorted(betweenness, key=betweenness.__getitem__,
            reverse=True)
            betweenness_attack.append(betweenness_sort[0])
        return betweenness_attack

    def calculate_closeness(self):
        # calculate closeness adptively
        #print self.graph_inv
        closeness_attack = []
        G_inv = nx.Graph()
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(self.graph_inv)
        closeness = nx.closeness_centrality(G_inv, distance='weight')
        closeness_sort = sorted(closeness, key=closeness.__getitem__,
        reverse=True)
        closeness_attack.append(closeness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(closeness_sort[0])
            closeness = nx.closeness_centrality(G_inv, distance='weight')
            closeness_sort = sorted(closeness, key=closeness.__getitem__,
            reverse=True)
            closeness_attack.append(closeness_sort[0])
        return closeness_attack
    
    def calculate_between(self, sink_node):
        # calculate betweenness adptively
        #print self.graph_inv
        betweenness_attack = []
        G_inv = nx.Graph()
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(self.graph_inv)
        betweenness = nx.betweenness_centrality(G_inv, weight='weight')
        for n in sink_node:
            betweenness[n] = -1
        betweenness_sort = sorted(betweenness, key=betweenness.__getitem__,
        reverse=True)
        betweenness_attack.append(betweenness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(betweenness_sort[0])
            betweenness = nx.betweenness_centrality(G_inv, weight='weight')
            for n in sink_node:
                betweenness[n] = -1
            
            betweenness_sort = sorted(betweenness, key=betweenness.__getitem__,
            reverse=True)
            betweenness_attack.append(betweenness_sort[0])
        return betweenness_attack

    def calculate_close(self, sink_node):
        # calculate closeness adptively
        #print self.graph_inv
        closeness_attack = []
        G_inv = nx.Graph()
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(self.graph_inv)
        closeness = nx.closeness_centrality(G_inv, distance='weight')
        for n in sink_node:
            closeness[n] = 0
        closeness_sort = sorted(closeness, key=closeness.__getitem__,
        reverse=True)
        closeness_attack.append(closeness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(closeness_sort[0])
            closeness = nx.closeness_centrality(G_inv, distance='weight')
            for n in sink_node:
                closeness[n] = -1 
            closeness_sort = sorted(closeness, key=closeness.__getitem__,
            reverse=True)
            closeness_attack.append(closeness_sort[0])
        return closeness_attack

    def calculate_a_betweenness(self, sink_node):
        a_betweenness_attack = []
        sink = sink_node[:]
        G_inv = nx.Graph()
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(self.graph_inv)
        a_betweenness = ac.a_betweenness_centrality(G_inv, Sink=sink,
        weight='weight')
        a_betweenness_sort = sorted(a_betweenness,
        key=a_betweenness.__getitem__, reverse=True)
        a_betweenness_attack.append(a_betweenness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(a_betweenness_sort[0])
            if a_betweenness_sort[0] in sink:
                sink.remove(a_betweenness_sort[0])
            a_betweenness = ac.a_betweenness_centrality(G_inv, Sink=sink,
            weight='weight')
            a_betweenness_sort = sorted(a_betweenness,
            key=a_betweenness.__getitem__, reverse=True)
            a_betweenness_attack.append(a_betweenness_sort[0])
        return a_betweenness_attack
        
    def calculate_a_closeness(self, sink_node):
        a_closeness_attack = []
        sink = sink_node[:]
        G_inv = nx.Graph()
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(self.graph_inv)
        a_closeness = ac.a_closeness_centrality(G_inv, Sink=sink,
        distance='weight')
        a_closeness_sort = sorted(a_closeness, key=a_closeness.__getitem__,
        reverse=True)
        a_closeness_attack.append(a_closeness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(a_closeness_sort[0])
            a_closeness = ac.a_closeness_centrality(G_inv, Sink=sink,
            distance='weight')
            a_closeness_sort = sorted(a_closeness, key=a_closeness.__getitem__,
            reverse=True)
            a_closeness_attack.append(a_closeness_sort[0])
        return a_closeness_attack

