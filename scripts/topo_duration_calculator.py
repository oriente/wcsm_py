"""
Created on November 11, 2012
Modified on April 18, 2013
use: calculate topology duration that can be used as aggregation window size
@author: Dongsheng Zhang
"""

import math
import networkx as nx
import sys

def calculate_metric(trace_file, num_of_node, p_link):
    # read from mobility trace
    f = open(trace_file, 'r')
    lines = f.readlines()
    f.close()
    ts = 100 
    te = 1100
    time_step = 0.01
    traffic_start = int(num_of_node*ts/time_step)   # traffic start line
    traffic_end = int(num_of_node*te/time_step)     # traffic end line
    sampling_rate = 1                               # the sampling rate taken into account to construct a graph
    tran_range = 100
    positions_per_timestep = []
    link_dur_list = []
    link_dur = 0
    topo_dur_list = []                              # list that stores topology durations
    topo_dur = 0
    link_duration_hash = {}
    link_duration_pre_hash = {}
    link_duration_cur_hash = {}
    link_duration_list = []
    graph_list = []
    pre_topo = []

    # construct a link duration dictionary
    for i in range(0, num_of_node - 1):
        for j in range (i + 1, num_of_node):
            link_duration_hash[(i,j)] = 0
            link_duration_pre_hash[(i,j)] = 0
            link_duration_cur_hash[(i,j)] = 0
    # read x, y axis postion for each node
    for line in lines[traffic_start:traffic_end]:
        s_line = line.rstrip().split(' ')
        pos_x,pos_y,pos_z = s_line[2].split('=')[1].split(':')
        positions_per_timestep.append([float(pos_x), float(pos_y)])

		# start aggregation if line number is equal to multiple of number of nodes
        if len(positions_per_timestep) == num_of_node:
            # start calculating matrix per step     
            matrix_per_timestep = []
            for pos_i in range(0, num_of_node - 1):
                for pos_j in range(pos_i + 1, num_of_node):
                    dist = math.sqrt(pow(abs(positions_per_timestep[pos_i][0] - positions_per_timestep[pos_j][0]), 2) +
                                    pow(abs(positions_per_timestep[pos_i][1] - positions_per_timestep[pos_j][1]), 2))
                    if dist <= tran_range:
                        matrix_per_timestep.append((int(pos_i), int(pos_j)))
                        link_duration_cur_hash[(pos_i, pos_j)] = 1
                        #print pos_i, pos_j, dist
                    else:
                        link_duration_cur_hash[(pos_i, pos_j)] = 0
                    
                    if link_duration_cur_hash[(pos_i, pos_j)] == 1:
                        link_duration_hash[(pos_i, pos_j)] += 1
                        link_duration_pre_hash[(pos_i, pos_j)] = 1
                    else:
                        if link_duration_pre_hash[(pos_i, pos_j)] == 1:
                            link_duration_pre_hash[(pos_i, pos_j)] = link_duration_cur_hash[(pos_i, pos_j)]
                            #print pos_i, pos_j, link_duration_hash[(pos_i, pos_j)]
                            link_duration_list.append(link_duration_hash[(pos_i, pos_j)])
                            link_duration_hash[(pos_i, pos_j)] = 0
            # clean up the list that stores node positions per time-step
            #print link_duration_cur_hash
            positions_per_timestep = []
            #print "previous: ", pre_topo
            if pre_topo == []:
                pre_topo = matrix_per_timestep[:]
            ischanged = compare_topo(pre_topo, matrix_per_timestep, p_link, num_of_node)
            #print ischanged
            #print "previous: ", pre_topo
            #print "current: ", matrix_per_timestep
            if not ischanged:
                topo_dur = topo_dur + 1
            else:
                pre_topo =  matrix_per_timestep
                topo_dur_list.append(topo_dur)
                topo_dur = 1
			# end calculating matrix per step
    
    for i in range(0, num_of_node - 1):
        for j in range (i + 1, num_of_node):
            if link_duration_cur_hash[(i,j)] == 1:
                link_duration_list.append(link_duration_hash[(i,j)])
    

    #print link_duration_list, len(link_duration_list)
    # add last topology duration
    topo_dur_list.append(topo_dur)
    
    #print "topology duration:", topo_dur_list
    #print "link duration:", link_duration_list
    return topo_dur_list, link_duration_list

def compare_topo(topo1, topo2, percent, node_num):
    topo1_len = len(topo1)
    topo2_len = len(topo2)
    #print topo1
    #print topo2
    temp_topo = topo2[:]
    num_of_matches = 0
    for pair1 in topo1:
        for pair2 in topo2:
            if pair1 == pair2:
                temp_topo.remove(pair2)
                num_of_matches += 1     
                break
    num_of_changes = topo1_len - num_of_matches + len(temp_topo)
    #print num_of_changes
    #print topo2
    if node_num*(node_num-1)*0.5* percent <= num_of_changes:
        return True 
    else:
        return False


def main():
    n_node = 20
    n_neigh = 8
    vel = 5
    #print n_node, n_neigh, vel
    expect_interval_output = open("expect_interval/node20neigh8velocity5",'w')
    for percentage_link in [0.1, 0.2]:
        dur_dict = {}
        duration_list = []
        link_list = []
        link_dict = {}
        e_interval = 0
        for seed in range(1000, 1001):
            trace_name = "n8s"+str(seed)+"v5.mob"
            duration_list, link_list = calculate_metric(trace_name, int(n_node), percentage_link)
            print trace_name
            #print duration_list
            for duration in duration_list:
                if dur_dict.has_key(duration):
                    dur_dict[duration] += 1
                else:
                    dur_dict[duration] = 1

            for link in link_list:
                if link_dict.has_key(link):
                    link_dict[link] += 1
                else:
                    link_dict[link] = 1
        number_of_duration = 0
        max_interval = 0
        for value in dur_dict.values():
            number_of_duration += value
        for key in sorted(dur_dict.keys()):
            time_interval_pdf = float(dur_dict[key])/number_of_duration
            #print key
            if key > max_interval:
                max_interval = key
            e_interval+= time_interval_pdf * key * 0.1
        expect_interval_output.write(str(percentage_link)+"\t"+str(e_interval)[0:6]+"\t"+str(max_interval*0.1)+"\n")
    expect_interval_output.close()
    
    #print dur_dict
    # write topology duration information into file 
    
if __name__=='__main__':
    main()


