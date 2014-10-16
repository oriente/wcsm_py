#!/usr/bin/env python

import sys
import networkx as nx
import math
import numpy
import random
import itertools as it
import a_centrality as ac
'''!!!
the calculation of link duration is not correct since link duration of
each time window is analysed separately.
'''

class TimeVaryingGraph:
    # python list is a very special data structure. within
    # the class, all the new objects shares the same ptr addr

    # input: number_of_node, neighbour_count, velocity, seed, trace, win_size 
    def __init__(self, v1, v2, v3, v4, v5, v6):
        self.node_num = v1
        self.neigh_count = v2
        self.velocity = v3
        self.seed = v4
        self.trace = v5
        self.win_size = v6
        
        self.aggregated_list = []
        self.degree_attack = []
        self.betweenness_attack = []
        self.graph_lists = []
        
    def __reini_per_window(self):
        self.aggregated_list = []
        self.degree_attack = []
        self.betweenness_attack = []
        self.graph_lists = []
        
    def return_random(self):
        return [self.random_flow_robust, self.random_biconnect,
        self.random_dmin, self.random_maxdiam]

    def return_degree(self):
        return [self.degree_flow_robust, self.degree_biconnect,
        self.degree_dmin, self.degree_maxdiam]

    def return_between(self):
        return [self.between_flow_robust, self.between_biconnect,
        self.between_dmin, self.between_maxdiam]

    # reinitialize all list variable for each seed
    def __reinit(self):
        self.random_flow_robust = [0,0,0,0,0,0]
        self.degree_flow_robust = [0,0,0,0,0,0]
        self.between_flow_robust = [0,0,0,0,0,0]

        self.random_maxdiam = [0,0,0,0,0,0]
        self.degree_maxdiam = [0,0,0,0,0,0]
        self.between_maxdiam = [0,0,0,0,0,0]

        self.random_dmin = [0,0,0,0,0,0]
        self.degree_dmin = [0,0,0,0,0,0]
        self.between_dmin = [0,0,0,0,0,0]

        self.random_biconnect = [0,0,0,0,0,0]
        self.degree_biconnect = [0,0,0,0,0,0]
        self.between_biconnect = [0,0,0,0,0,0]
        
    def display(self):
        print "random flow robustness: ",
        print self.random_flow_robust
        print "degree flow robustness: ",
        print self.degree_flow_robust

    def calculate(self):
        self.traffic_start = 100
        self.traffic_end = 1100 
        self.__reinit()
        '''the attack is performed for every time window, centrality metric is
        calculated for each time windows also.
        '''
        for time_start in range(self.traffic_start, self.traffic_end, self.win_size):
            time_end = time_start+self.win_size
            if time_end > self.traffic_end:
                time_end = self.traffic_end
            self.__reini_per_window()
            self.aggregate(time_start, time_end)
            self.calculate_centrality()
            self.attacks()

    def aggregate(self, ts, te):
        # read mobility trace file based on node_num, neigh_count, and velocity
        tran_range = 100                    # transmission range set as 100 m     
        time_step = 0.1
        mobility_file = open(self.trace, 'r')
        mobility_lines = mobility_file.readlines()
        mobility_file.close()
        traffic_start = self.node_num * ts * int(1/time_step)
        traffic_end = self.node_num * te * int(1/time_step)
        
        weighted_graph_hash = {}            # (vi, vj) -> edge weight
        # constructing dictionary that includes all pairs of node
        for i in range(0, self.node_num - 1):
            for j in range (i + 1, self.node_num):
                weighted_graph_hash[(i,j)] = 0
		
        # start aggregating topology based on traffic_start and traffic_end		
        positions_per_timestep = []         # stores node positions per time step
        for line in mobility_lines[traffic_start:traffic_end]:
            s_line = line.rstrip().split(' ')
            pos_x,pos_y,pos_z = s_line[2].split('=')[1].split(':')
            positions_per_timestep.append([float(pos_x), float(pos_y)])
            # calculate adjacency matrix for every node_num lines
            if len(positions_per_timestep) == self.node_num:
                # list that stores adjacency matrix per time step 
                matrix_per_timestep = []
                for pos_i in range(0, self.node_num - 1):
                    for pos_j in range(pos_i + 1, self.node_num):
                        dist=math.sqrt(pow(abs(positions_per_timestep[pos_i][0]
                        -positions_per_timestep[pos_j][0]), 2)+
                        pow(abs(positions_per_timestep[pos_i][1]-
                        positions_per_timestep[pos_j][1]), 2))
                        if dist <= tran_range:
                            matrix_per_timestep.append((int(pos_i), int(pos_j)))
                            # store the number of time that two nodes are connected into the hash table
                            weighted_graph_hash[(pos_i, pos_j)] = weighted_graph_hash[(pos_i, pos_j)] + 1
                self.graph_lists.append(matrix_per_timestep)
                positions_per_timestep = []         # clear list that stores node positions
        
        # normalize the link availability and store weighted graph adj into a list
        for i in range(0, self.node_num - 1):
            for j in range (i + 1, self.node_num):
                link_weight = float(weighted_graph_hash[(i,j)])/(100*(te-ts))
                # remove those links with extremely small weights 0.05*10=0.5 is the threshold
                if link_weight > 0.01:
                    self.aggregated_list.append((i, j,
                    float(weighted_graph_hash[(i,j)])/(100*(te-ts))))

    def write_centrality(self):
        for node in self.degree_attack:
            self.out_degree.write(str(node)+" ")
        self.out_degree.write("\n")

        for node in self.eigen_attack:
            self.out_eigen.write(str(node)+" ")
        self.out_eigen.write("\n")

        for node in self.betweenness_attack:
            self.out_betweenness.write(str(node)+" ")
        self.out_betweenness.write("\n")

        for node in self.closeness_attack:
            self.out_closeness.write(str(node)+" ")
        self.out_closeness.write("\n")

    def calculate_centrality(self):
        G = nx.Graph()
        G.add_nodes_from(range(self.node_num))
        G.add_weighted_edges_from(self.aggregated_list)
        degree = G.degree(weight='weight')
        dgr_sort = sorted(degree, key=degree.__getitem__, reverse=True)
        self.degree_attack.append(dgr_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G.remove_node(dgr_sort[0])
            degree = G.degree(weight='weight')
            dgr_sort = sorted(degree, key=degree.__getitem__, reverse=True)
            self.degree_attack.append(dgr_sort[0])

        # invert weight of the graph for betweenness and closeness
        graph_inv = []
        for i in range (0,len(self.aggregated_list)):
                a_weight = math.pow(1/self.aggregated_list[i][2], 1)
                a = (self.aggregated_list[i][0], self.aggregated_list[i][1], a_weight)
                graph_inv.append(a)
        G_inv = nx.Graph()
        
        # calculate betweenness adptively
        G_inv.add_nodes_from(range(self.node_num))
        G_inv.add_weighted_edges_from(graph_inv)
        betweenness = nx.betweenness_centrality(G_inv, weight='weight')
        betweenness_sort = sorted(betweenness, key=betweenness.__getitem__, reverse=True)
        self.betweenness_attack.append(betweenness_sort[0])
        for num_of_deletion in range (0,self.node_num/2-1):
            G_inv.remove_node(betweenness_sort[0])
            betweenness = nx.betweenness_centrality(G_inv, weight='weight')
            betweenness_sort = sorted(betweenness, key=betweenness.__getitem__, reverse=True)
            self.betweenness_attack.append(betweenness_sort[0])

    def attacks(self):
        random_attack = range(self.node_num)
        for i in range(random.randint(0,5)):
            random.shuffle(random_attack)

        self.__attack(random_attack, self.random_flow_robust,
        self.random_biconnect, self.random_dmin, self.random_maxdiam)
        
        self.__attack(self.degree_attack, self.degree_flow_robust,
        self.degree_biconnect, self.degree_dmin, self.degree_maxdiam)
        
        self.__attack(self.betweenness_attack, self.between_flow_robust,
        self.between_biconnect, self.between_dmin, self.between_maxdiam)
    
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

    def __attack(self, attack_seq, flow_robusts, biconnects,
        dmins, mdiams):
        mdiam = [0,0,0,0,0,0]
        flow_robust= [0,0,0,0,0,0]
        biconnect = [0,0,0,0,0,0]
        dmin = [0,0,0,0,0,0]
        #print len(self.graph_lists)
        #print attack_seq
        for graph in self.graph_lists:
            G_topo = nx.Graph()
            G_topo.add_nodes_from(range(self.node_num))
            G_topo.add_edges_from(graph)
            mdiam[0]+=self.__max_diam(G_topo)
            flow_robust[0]+=self.__flow_robust(G_topo)
            dmin[0]+=min(G_topo.degree().values())
            if nx.is_biconnected(G_topo):
                biconnect[0]+=1
            
            for node_fail_percent in [0.1, 0.2, 0.3, 0.4, 0.5]:
                node_to_remove = range(int(self.node_num*node_fail_percent-self.node_num*0.1), int(self.node_num*node_fail_percent))
                for node_index in node_to_remove:
                    G_topo.remove_node(attack_seq[node_index])
                mdiam[int(node_fail_percent*10)] += self.__max_diam(G_topo)
                flow_robust[int(node_fail_percent*10)] += self.__flow_robust(G_topo)
                dmin[int(node_fail_percent*10)]+=min(G_topo.degree().values())
                if nx.is_biconnected(G_topo):
                    biconnect[int(node_fail_percent*10)]+=1        
        for i in range(6):
            mdiams[i] += mdiam[i]/10.0/(self.traffic_end - self.traffic_start)
            flow_robusts[i] += flow_robust[i]/10.0/(self.traffic_end - self.traffic_start)
            dmins[i] += dmin[i]/10.0/(self.traffic_end - self.traffic_start)
            biconnects[i] += biconnect[i]/10.0/(self.traffic_end -
            self.traffic_start)
