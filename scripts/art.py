#!/usr/bin/env python    
from TimeVaryingGraphInfo import TimeVaryingGraph
from Aggregate import Aggregation
from CalculateCentralityRT import CalculateCentrality
from Attacks import Attacks
import sys
import math
import numpy
import random

# add corresonpding value in the list2 to list1
def add_lists(list1, list2):
    if len(list1) == len(list2):
        for i in range(len(list1)):
            list1[i] += list2[i]
    else:
        print "lists are not of equal length"
    #return list1

def normalize_list(alist, interval):
    for n in range(len(alist)):
        alist[n] = alist[n]/interval
    return alist

def list_avg_conf(alist):
    avg_list = []
    conf_list = []
    list_len = len(alist)
    per_seed_len = len(alist[0])
    for n in range(per_seed_len):
        temp_list = []
        for seed in range(list_len):
            temp_list.append(alist[seed][n])

        avg_list.append(numpy.average(temp_list))
        conf_list.append(1.96/math.sqrt(10)*numpy.std(temp_list))
    return avg_list, conf_list
    #print avg_list
    #print conf_list

def write_list(filename, avg, conf, co):
    output = open("rt_verification/"+filename, 'w')
    for n in range(6):
        output.write(str(avg[n]*co)+'\t'+str(conf[n]*co)+'\n')
    output.close()

def write_metric(filename, alist):
    output = open("rt_centrality_metrics/"+filename, 'a')
    for a in alist:
        output.write(str(a)+' ')
    output.write('\n')
    output.close()

if __name__== '__main__':
    number_of_node = int(sys.argv[1])
    neighbour_count = int(sys.argv[2])
    velocity = int(sys.argv[3])
    win_size = float(sys.argv[4])
    time_step = 0.1
    isoutput = False 
    
    random_flow_list = []
    degree_flow_list = []
    eigenvector_flow_list = []
    closeness_flow_list = []
    betweenness_flow_list = []

    arandom_flow_list = []
    aclose_flow_list = []
    abetween_flow_list = []

    traffic_start = 100
    traffic_end = 1100
    
    for seed in range(1000,1010):
        random_flow = [0,0,0,0,0,0]
        degree_flow = [0,0,0,0,0,0]
        eigenvector_flow = [0,0,0,0,0,0]
        closeness_flow = [0,0,0,0,0,0]
        betweenness_flow = [0,0,0,0,0,0]

        arandom_flow = [0,0,0,0,0,0]
        aclose_flow = [0,0,0,0,0,0]
        abetween_flow = [0,0,0,0,0,0]
        
        trace_name = "mob/w" + str(number_of_node) + "n" + str(neighbour_count)\
        + "s" +str(seed)+"v"+ str(velocity)+".mob"
        print trace_name
        for t_start in range(traffic_start, traffic_end, int(win_size)):
            t_end = t_start + int(win_size)
            if t_end > traffic_end:
                t_end = traffic_end

            tvgraph = (Aggregation(int(number_of_node), int(neighbour_count),
            int(velocity), seed, trace_name, t_start, t_end))
            tvgraph.parse_trace()
            tvgraph.aggregate()
            # calculate based on aggregated window
            #print tvgraph.get_graph_list()
            cc = CalculateCentrality(number_of_node, tvgraph.get_graph_list()[0])
            # output these metrics into .csv file for ns-3 simulation
            print tvgraph.get_graph_list()[0]
            sink = range(4) 
            # calculate symmetric scenario 
            a_close_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_close(sink))
            a_close_atk.a_attack(sink)
            #a_close_atk.a_normalize_measure()
            add_lists(aclose_flow, a_close_atk.get_aflowrobust())
            '''
            write_metric("aclose"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_a_close(sink))
            '''
            a_between_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_between(sink))
            a_between_atk.a_attack(sink)
            #a_between_atk.a_normalize_measure()
            add_lists(abetween_flow, a_between_atk.get_aflowrobust())
            '''
            write_metric("abetween"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_a_betweenness(sink))
            ''' 
        
        aclose_flow_list.append(aclose_flow)
        abetween_flow_list.append(abetween_flow)
    
    coeffi = time_step/(traffic_end-traffic_start)
    
    abetween_avg,abetween_conf = list_avg_conf(abetween_flow_list)
    write_list("abetween"+str(number_of_node)+str(neighbour_count)+str(velocity),
    abetween_avg, abetween_conf, coeffi)
    
    aclose_avg,aclose_conf = list_avg_conf(aclose_flow_list)
    write_list("aclose"+str(number_of_node)+str(neighbour_count)+str(velocity),
    aclose_avg, aclose_conf, coeffi)

