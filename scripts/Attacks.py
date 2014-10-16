#!/usr/bin/env python

import sys
import networkx as nx
import math
import numpy
import random
import itertools as it
import a_centrality as ac

class Attacks:

    def __init__(self, v1, v2, v3):
        self.node_num = v1
        self.graph_lists = v2
        self.attack_seq = v3
        self.aflowrobust= [0,0,0,0,0,0]
        self.flowrobust= [0,0,0,0,0,0]
        self.biconnect = [0,0,0,0,0,0]
        self.maxdiam =   [0,0,0,0,0,0]
        self.mindegree = [0,0,0,0,0,0]
        
    def bases(self):
        base_flowrobust = []
        base_biconnect = []
        for graph in self.graph_lists:
            print graph
            G_topo = nx.Graph()
            G_topo.add_edges_from(graph)
            base_biconnect.append(nx.is_biconnected(G_topo))
            base_flowrobust.append(self.__flow_robust(G_topo))
        return base_flowrobust
    
    def get_all_metrics(self):
        return [self.flowrobust, self.biconnect, self.maxdiam, self.mindegree]
    
    def get_aflowrobust(self):
        return self.aflowrobust
    
    def get_flowrobust(self):
        return self.flowrobust
    
    def get_biconnect(self):
        return self.biconnect
    
    def get_maxdiam(self):
        return self.maxdiam
    
    def get_mindegree(self):
        return self.mindegree
    
    # this calculates graph connectivity measures at each time step
    def attacks(self):
        for graph in self.graph_lists:
            G_topo = nx.Graph()
            G_topo.add_nodes_from(range(self.node_num))
            G_topo.add_edges_from(graph)
            # graph connectivity measures without attacks 
            self.flowrobust[0]+=self.__flow_robust(G_topo)
            if nx.is_biconnected(G_topo):
                self.biconnect[0]+=1
            self.maxdiam[0]+=self.__max_diam(G_topo)
            self.mindegree[0]+=min(G_topo.degree().values())
            #graph connectivity measures under node failures 
            for fail_rate in [0.1, 0.2, 0.3, 0.4, 0.5]:
                node_to_remove = \
                range(int(self.node_num*fail_rate-self.node_num*0.1),
                int(self.node_num*fail_rate))
                
                for node_index in node_to_remove:
                    G_topo.remove_node(self.attack_seq[node_index])

                self.flowrobust[int(fail_rate*10)] += self.__flow_robust(G_topo)
                if nx.is_biconnected(G_topo):
                    self.biconnect[int(fail_rate*10)]+=1        
                self.maxdiam[int(fail_rate*10)] += self.__max_diam(G_topo)
                self.mindegree[int(fail_rate*10)]+=min(G_topo.degree().values())
    
    def a_attack(self, sink_node):
        print self.attack_seq
        for graph in self.graph_lists:
            G_topo = nx.Graph()
            G_topo.add_nodes_from(range(self.node_num))
            G_topo.add_edges_from(graph)
            # graph connectivity measures without attacks 
            self.aflowrobust[0]+=self.__a_flow_robust(G_topo, sink_node)
            #graph connectivity measures under node failures 
            for fail_rate in [0.1, 0.2, 0.3, 0.4, 0.5]:
                node_to_remove = \
                range(int(self.node_num*fail_rate-self.node_num*0.1),
                int(self.node_num*fail_rate))
                
                for node_index in node_to_remove:
                    G_topo.remove_node(self.attack_seq[node_index])

                self.aflowrobust[int(fail_rate*10)] += \
                self.__a_flow_robust(G_topo, sink_node)

    def a_normalize_measure(self):
        for i in range(6):
            self.aflowrobust[i] = self.aflowrobust[i]/len(self.graph_lists)
    

    def normalize_measure(self):
        for i in range(6):
            self.flowrobust[i] = self.flowrobust[i]/len(self.graph_lists)
            self.biconnect[i] = self.biconnect[i]/len(self.graph_lists)
            self.maxdiam[i] = self.maxdiam[i]/len(self.graph_lists)
            self.mindegree[i] = self.mindegree[i]/len(self.graph_lists)

    def __a_flow_robust(self, graph, sink):
        flows = 0.0
        comps = nx.connected_components(graph)
        # make a copy of sink
        sinkl = sink[:]
        for comp in comps:
            ns = 0 # number of sink in each component
            for s in sinkl:
                if s in comp:
                  ns += 1
            # it considers sink to sink traffic
            flows = flows + (len(comp) - ns ) * ns
        total_flows = (self.node_num - len(sink)) * len(sink)
        a_flow_robust = flows/total_flows
        
        return a_flow_robust
    
    def __flow_robust(self, graph):
        flows = 0
        comps = nx.connected_components(graph)
        #print len(comps)
        for comp in comps:
            flows = flows + len(comp) * (len(comp) - 1)/2.0
        total_flows = self.node_num * (self.node_num - 1)/2
        flow_robust = flows/total_flows
        return flow_robust

    def __max_diam(self, graph):
        max_diam = 0
        for comp in nx.connected_component_subgraphs(graph):
            if len(comp.nodes())>1:
                comp_diam = nx.diameter(comp)
                if comp_diam>max_diam:
                    max_diam = comp_diam
        return max_diam

