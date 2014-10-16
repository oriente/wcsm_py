"""
Created on November 11, 2012
Modified on April 18, 2013
use: calculate topology duration that can be used as aggregation window size
@author: Dongsheng Zhang
"""

import math
import networkx as nx
import sys
import numpy
def count_topology_change(trace_file, num_of_node):
    # read from mobility trace
    f = open(trace_file, 'r')
    lines = f.readlines()
    f.close()
    ts = 100 
    te = 1100
    time_step = 0.1
    traffic_start = int(num_of_node*ts/time_step)   # traffic start line
    traffic_end = int(num_of_node*te/time_step)     # traffic end line
    sampling_rate = 1                               # the sampling rate taken into account to construct a graph
    tran_range = 100
    positions_per_timestep = []
    graph_list = []
    pre_topo = []
    change_count = 0
    # read x, y axis postion for each node
    for line in lines[traffic_start:traffic_end]:
        s_line = line.rstrip().split(' ')
        pos_x,pos_y,pos_z = s_line[2].split('=')[1].split(':')
        positions_per_timestep.append([float(pos_x), float(pos_y)])

		# start aggregation if line number is equal to multiple of number of nodes
        if len(positions_per_timestep) == num_of_node:
            # start calculating matrix per step     
            cur_topo = []
            for pos_i in range(0, num_of_node - 1):
                for pos_j in range(pos_i + 1, num_of_node):
                    dist = math.sqrt(pow(abs(positions_per_timestep[pos_i][0] - positions_per_timestep[pos_j][0]), 2) +
                                    pow(abs(positions_per_timestep[pos_i][1] - positions_per_timestep[pos_j][1]), 2))
                    if dist <= tran_range:
                        cur_topo.append((int(pos_i), int(pos_j)))
            positions_per_timestep = []
            #print cur_topo 
            #print 
            ischanged = (pre_topo != cur_topo)
            if ischanged:
                change_count += 1
                pre_topo = cur_topo[:]
         
    return change_count


def main():
    nwifis = [10, 20, 30]
    nneighs = [2, 4, 6, 8, 10]
    velocities = [0, 5, 10]
    for wifi in nwifis:
        for neigh in nneighs:
            for vel in velocities:
                topo_change_list = []
                base = "w"+str(wifi)+"n"+str(neigh)+"v"+str(vel)+".csv"
                print base
                out_topo = open(base, 'w')
                for seed in range(1000,1010):
                    trace_name = \
                    "mob/w"+str(wifi)+"n"+str(neigh)+"s"+str(seed)+"v"+str(vel)+".mob"
                    num_of_topo = count_topology_change(trace_name, int(wifi))
                    topo_change_list.append(num_of_topo)
                ave = numpy.average(topo_change_list)
                conf = numpy.std(topo_change_list)*1.96/math.sqrt(10)
                out_topo.write(str(ave)+"\t"+str(conf))

if __name__=='__main__':
    main()


