#!/usr/bin/env python
'''
Created on November 11, 2012
Modified on 03 July, 2013
use: calculate link duration based on the Gauss-Markov (only) mobility traces in
ns-3
@author: Dongsheng Zhang
dzhang@ittc.ku.edu
'''
import sys
import networkx as nx
import math
import numpy
import random
import itertools as it

# the output print is a link duration list, each element is the # of time steps.
# make sure that you multiple it them step size to show the actual link duration
# in [s]. Also, this script stores the adjacency matrices of whole time in
# memory. Hence, it would use extremely high amount of memeory. Be careful when
# you use it.
def main():
    # set up the parameters for trace processing
    ts = 100 # the start time in the trace. in unit [s]
    te = 500 # the end time in the trace. in unit [s]
    tran_range = 100
    time_step = 0.01
    node_num = 20
    trace_name = "n8s1000v5.mob"
    
    mobility_file = open(trace_name, 'r')
    mobility_lines = mobility_file.readlines()
    mobility_file.close()
    traffic_start = node_num * ts * int(1/time_step)
    traffic_end = node_num * te * int(1/time_step)
    graph_lists = []
    # start aggregating topology based on traffic_start and traffic_end		
    positions_per_timestep = []
    for line in mobility_lines[traffic_start:traffic_end]:
        s_line = line.rstrip().split(' ')
        pos_x,pos_y,pos_z = s_line[2].split('=')[1].split(':')
        positions_per_timestep.append([float(pos_x), float(pos_y)])
        # calculate adjacency matrix for every node_num lines
        if len(positions_per_timestep) == node_num:
            # list that stores adjacency matrix per time step 
            matrix_per_timestep = []
            for pos_i in range(0, node_num - 1):
                for pos_j in range(pos_i + 1, node_num):
                    dist=math.sqrt(pow(abs(positions_per_timestep[pos_i][0]
                    -positions_per_timestep[pos_j][0]), 2)+
                    pow(abs(positions_per_timestep[pos_i][1]-
                    positions_per_timestep[pos_j][1]), 2))
                    if dist <= tran_range:
                        matrix_per_timestep.append((int(pos_i), int(pos_j)))
            # append adj for each time step into the graph_lists
            graph_lists.append(matrix_per_timestep)
            # clear list that stores node positions 
            positions_per_timestep = []
    ''' input variable topologies is a sequence of graph adjacency matrices
    parsed from mobility traces. link duration is calcualted as checking each
    adjacency matrix entry of each time step, whenever the entry change from 1
    to 0, save the link duration value to link_duration_list. For the end of the
    trace, append all the link duration values that are not equal to 0 to the
    link_duration_list
    '''

    link_duration_list = []
    # initialize topology hash
    link_duration_hash = {}
    link_duration_pre_hash = {}
    for i in range(0, node_num-1):
        for j in range(i+1, node_num):
            link_duration_hash[(i,j)] = 0
            link_duration_pre_hash[(i,j)] = 0
    # process topology of each snapshot
    for topo in graph_lists:
        for edge in topo:
            link_duration_hash[edge]+=1
        # compare previous topology and current topology 
        for i in range(0, node_num-1):
            for j in range(i+1, node_num):
                if (link_duration_hash[(i,j)]!= 0 and link_duration_hash[(i,j)]
                    == link_duration_pre_hash[(i,j)]):
                    link_duration_list.append(link_duration_hash[(i,j)])
                    link_duration_hash[(i,j)]=0
        link_duration_pre_hash = link_duration_hash.copy()
    for time in sorted(link_duration_hash.values()):
        if time!=0:
            link_duration_list.append(time)
    print link_duration_list
    #return numpy.mean(link_duration_list)


if __name__=='__main__':
    main()

