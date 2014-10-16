#!/usr/bin/env python

import sys
import networkx as nx
import math
import numpy
import random

class Aggregation:
    # python list is a very special data structure. within
    # the class, all the new objects shares the same ptr addr

    # input: number_of_node, neighbour_count, velocity, seed, trace, win_size 
    def __init__(self, v1, v2, v3, v4, v5, v6, v7):
        self.node_num = v1
        self.neigh_count = v2
        self.velocity = v3
        self.seed = v4
        self.trace = v5
        self.ts = v6
        self.te = v7
        self.weighted_graph_hash = {}            # (vi, vj) -> edge weight
        self.aggregated_list = []
        self.graph_lists = []
        # initiate weighteh graph hash table    
        for i in range(0, self.node_num - 1):
            for j in range (i + 1, self.node_num):
                self.weighted_graph_hash[(i,j)] = 0
    
    def get_graph_list(self):
        return self.graph_lists

    def get_aggregated_list(self):
        return self.aggregated_list
        #return weighted_graph_hash

    def __disToadj(self,positions_per_timestep):
        tran_range = 100                    # transmission range set as 100 m     
        matrix_per_timestep = []
        for pos_i in range(0, self.node_num - 1):
            for pos_j in range(pos_i + 1, self.node_num):
                dist=math.sqrt(pow(abs(positions_per_timestep[pos_i][0]
                -positions_per_timestep[pos_j][0]), 2)+
                pow(abs(positions_per_timestep[pos_i][1]-
                positions_per_timestep[pos_j][1]), 2))
                if dist <= tran_range:
                    matrix_per_timestep.append((int(pos_i), int(pos_j)))
                    # store the number of time that two nodes are connected into
                    # the hash table
                    self.weighted_graph_hash[(pos_i, pos_j)]= \
                    self.weighted_graph_hash[(pos_i, pos_j)] + 1
        return matrix_per_timestep


    def parse_trace(self):
        # read mobility trace file based on node_num, neigh_count, and velocity
        time_step = 0.1
        mobility_file = open(self.trace, 'r')
        mobility_lines = mobility_file.readlines()
        mobility_file.close()
        traffic_start = self.node_num * self.ts * int(1/time_step)
        traffic_end = self.node_num * self.te * int(1/time_step)
        
        # start aggregating topology based on traffic_start and traffic_end		
        positions_per_timestep = []         # stores node positions per time step
        for line in mobility_lines[traffic_start:traffic_end]:
            s_line = line.rstrip().split(' ')
            pos_x,pos_y,pos_z = s_line[2].split('=')[1].split(':')
            positions_per_timestep.append([float(pos_x), float(pos_y)])
            # calculate adjacency matrix for every node_num lines
            if len(positions_per_timestep) == self.node_num:
                # convert distance metric to adjacency matrix based on
                # transmission range
                matrix_per_timestep = self.__disToadj(positions_per_timestep)
                self.graph_lists.append(matrix_per_timestep)
                # clear list that stores node position
                positions_per_timestep = []
    
    def aggregate(self):
        # normalize the link availability and store weighted graph adj into a list
        for i in range(0, self.node_num - 1):
            for j in range (i + 1, self.node_num):
                
                link_weight = \
                float(self.weighted_graph_hash[(i,j)])/(10*(self.te-self.ts))
                # remove those links with extremely small weights 0.05*10=0.5 is
                # the threshold
                if link_weight > 0.01:
                    self.aggregated_list.append((i, j,
                    float(self.weighted_graph_hash[(i,j)])/(10*(self.te-self.ts))))

