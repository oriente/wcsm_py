#!/usr/bin/env python    
from TimeVaryingGraphInfo import TimeVaryingGraph
from Aggregate import Aggregation
from CalculateCentrality import CalculateCentrality
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
    output = open("verification/"+filename, 'w')
    for n in range(6):
        output.write(str(avg[n]*co)+'\t'+str(conf[n]*co)+'\n')
    output.close()

def write_metric(filename, alist):
    output = open("centrality_metrics/"+filename, 'a')
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
    acloseness_flow_list = []
    abetweenness_flow_list = []

    traffic_start = 100
    traffic_end = 200
    
    for seed in range(1000,1002):
        random_flow = [0,0,0,0,0,0]
        degree_flow = [0,0,0,0,0,0]
        eigenvector_flow = [0,0,0,0,0,0]
        closeness_flow = [0,0,0,0,0,0]
        betweenness_flow = [0,0,0,0,0,0]

        arandom_flow = [0,0,0,0,0,0]
        acloseness_flow = [0,0,0,0,0,0]
        abetweenness_flow = [0,0,0,0,0,0]
        
        trace_name = "mob/w" + str(number_of_node) + "n" + str(neighbour_count)\
        + "s" +str(seed)+"v"+ str(velocity)+".mob"
        print trace_name
        for t_start in range(traffic_start, traffic_end, int(win_size)):
            print t_start
            t_end = t_start + int(win_size)
            if t_end > traffic_end:
                t_end = traffic_end

            tvgraph = (Aggregation(int(number_of_node), int(neighbour_count),
            int(velocity), seed, trace_name, t_start, t_end))
            tvgraph.parse_trace()
            tvgraph.aggregate()
            # calculate based on aggregated window
            cc = CalculateCentrality(number_of_node, tvgraph.get_aggregated_list())
            # invert weight for weighted graph
            cc.invert_weight()
            # output these metrics into .csv file for ns-3 simulation
            
            # calculate symmetric scenario 
            calculate_random = range(number_of_node)
            for i in range(random.randint(0,5)):
                random.shuffle(calculate_random)
            
            random_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            calculate_random)
            random_atk.attacks()
            #random_atk.normalize_measure()
            add_lists(random_flow, random_atk.get_flowrobust())
            write_metric("random"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", calculate_random)
            
            degree_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_degree())
            degree_atk.attacks()
            #degree_atk.normalize_measure()
            add_lists(degree_flow, degree_atk.get_flowrobust())
            write_metric("degree"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_degree())
            
            eigenvector_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_eigenvector())
            eigenvector_atk.attacks()
            #eigenvector_atk.normalize_measure()
            add_lists(eigenvector_flow, eigenvector_atk.get_flowrobust())
            write_metric("eigenvector"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_eigenvector())
            
            closeness_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_closeness())
            closeness_atk.attacks()
            #closeness_atk.normalize_measure()
            add_lists(closeness_flow, closeness_atk.get_flowrobust())
            write_metric("closeness"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_closeness())
            
            betweenness_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_betweenness())
            betweenness_atk.attacks()
            #betweenness_atk.normalize_measure()
            add_lists(betweenness_flow, betweenness_atk.get_flowrobust())
            write_metric("betweenness"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_betweenness())
            
            
            # calculate asymmetric version 
            calculate_arandom = range(4, number_of_node)
            for i in range(random.randint(0,5)):
                random.shuffle(calculate_arandom)
            sink = range(4)
            a_random_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            calculate_arandom)
            a_random_atk.a_attack(sink)
            #a_random_atk.a_normalize_measure()
            add_lists(arandom_flow, a_random_atk.get_aflowrobust())
            write_metric("arandom"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", calculate_arandom)

            a_closeness_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_a_closeness(sink))
            a_closeness_atk.a_attack(sink)
            #a_closeness_atk.a_normalize_measure()
            add_lists(acloseness_flow, a_closeness_atk.get_aflowrobust())
            write_metric("acloseness"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_a_closeness(sink))

            a_betweenness_atk = Attacks(number_of_node, tvgraph.get_graph_list(),
            cc.calculate_a_betweenness(sink))
            a_betweenness_atk.a_attack(sink)
            #a_betweenness_atk.a_normalize_measure()
            add_lists(abetweenness_flow, a_betweenness_atk.get_aflowrobust())
            write_metric("abetweenness"+str(number_of_node) + str(neighbour_count) +
            str(seed) + str(velocity) + ".csv", cc.calculate_a_betweenness(sink))
        
        
        random_flow_list.append(random_flow)
        degree_flow_list.append(degree_flow)
        eigenvector_flow_list.append(eigenvector_flow)
        closeness_flow_list.append(closeness_flow)
        betweenness_flow_list.append(betweenness_flow)

        arandom_flow_list.append(arandom_flow)
        acloseness_flow_list.append(acloseness_flow)
        abetweenness_flow_list.append(abetweenness_flow)
    
    coeffi = time_step/(traffic_end-traffic_start)
    
    random_avg,random_conf = list_avg_conf(random_flow_list)
    write_list("random"+str(number_of_node)+str(neighbour_count)+str(velocity),
    random_avg, random_conf, coeffi)
    
    degree_avg,degree_conf = list_avg_conf(degree_flow_list)
    write_list("degree"+str(number_of_node)+str(neighbour_count)+str(velocity),
    degree_avg, degree_conf, coeffi)
    
    eigenvector_avg,eigenvector_conf = list_avg_conf(eigenvector_flow_list)
    write_list("eigenvector"+str(number_of_node)+str(neighbour_count)+str(velocity),
    eigenvector_avg, eigenvector_conf, coeffi)
    
    closeness_avg,closeness_conf = list_avg_conf(closeness_flow_list)
    write_list("closeness"+str(number_of_node)+str(neighbour_count)+str(velocity),
    closeness_avg, closeness_conf, coeffi)
    
    betweenness_avg,betweenness_conf = list_avg_conf(betweenness_flow_list)
    write_list("betweenness"+str(number_of_node)+str(neighbour_count)+str(velocity),
    betweenness_avg, betweenness_conf, coeffi)
    
    arandom_avg,arandom_conf = list_avg_conf(arandom_flow_list)
    write_list("arandom"+str(number_of_node)+str(neighbour_count)+str(velocity),
    arandom_avg, arandom_conf, coeffi)
    
    abetweenness_avg,abetweenness_conf = list_avg_conf(abetweenness_flow_list)
    write_list("abetweenness"+str(number_of_node)+str(neighbour_count)+str(velocity),
    abetweenness_avg, abetweenness_conf, coeffi)
    
    acloseness_avg,acloseness_conf = list_avg_conf(acloseness_flow_list)
    write_list("acloseness"+str(number_of_node)+str(neighbour_count)+str(velocity),
    acloseness_avg, acloseness_conf, coeffi)


