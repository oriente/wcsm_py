#!/usr/bin/env python    
from TimeVaryingGraphInfo import TimeVaryingGraph
import sys
import math
import numpy

if __name__== '__main__':
    
    number_of_node = 20
    neighbour_count = 8
    velocity = 5
    isoutput = False 
    '''
    win_size_file = "expect_interval/node"+number_of_node+"neigh"+neighbour_count+"velocity"+velocity
    print win_size_file
    win_size_read = open(win_size_file, 'r')
    # 10% topology change 
    win_size = int(math.ceil(float(win_size_read.readlines()[0].split("\t")[1])))
    win_size_read.close()
    '''
    random_stat = []
    degree_stat = []
    between_stat = []

    win_size = 35
    for seed in range(1000,1001):
        trace_name = "n8s"+str(seed)+"v5.mob"
        print trace_name
        tvgraph = (TimeVaryingGraph(int(number_of_node), int(neighbour_count), int(velocity), seed, trace_name, win_size))
        #tvgraph.aggregate(100, 200)
        #print tvgraph.bases()
        tvgraph.calculate()
        random_stat.append(tvgraph.return_random())
        degree_stat.append(tvgraph.return_degree())
        between_stat.append(tvgraph.return_between())
    print random_stat
    print degree_stat
    print between_stat

    if isoutput:
        maxdiam_output_file = "maxdiam_stat/node20neigh8vel5"
        maxdiam_output = open(maxdiam_output_file, 'w')
        for i in range(6):
            maxdiam_output.write(str(i*0.1))
            for stat in [random_stat, degree_stat, eigen_stat, between_stat, close_stat]:
                print stat
                alist = []
                for s in range(10):
                    alist.append(stat[s][4][i])
                ave = numpy.mean(alist)
                conf = numpy.std(alist)*1.96/math.sqrt(10)
                maxdiam_output.write('\t'+str(ave)[0:6]+'\t'+str(conf)[0:6])
            maxdiam_output.write('\n')
        maxdiam_output.close()
    
        dmin_output_file = "dmin_stat/node20neigh8vel5"
        dmin_output = open(dmin_output_file, 'w')
        for i in range(6):
            dmin_output.write(str(i*0.1))
            for stat in [random_stat, degree_stat, eigen_stat, between_stat, close_stat]:
                alist = []
                for s in range(10):
                    alist.append(stat[s][3][i])
                ave = numpy.mean(alist)
                conf = numpy.std(alist)*1.96/math.sqrt(10)
                dmin_output.write('\t'+str(ave)[0:6]+'\t'+str(conf)[0:6])
            dmin_output.write('\n')
        dmin_output.close()

        flow_robust_output_file = "flow_robust_stat/node20neigh8vel5"
        flow_robust_output = open(flow_robust_output_file, 'w')
        for i in range(6):
            flow_robust_output.write(str(i*0.1))
            for stat in [random_stat, degree_stat, eigen_stat, between_stat, close_stat]:
                alist = []
                for s in range(10):
                    alist.append(stat[s][0][i])
                ave = numpy.mean(alist)
                conf = numpy.std(alist)*1.96/math.sqrt(10)
                flow_robust_output.write('\t'+str(ave)[0:6]+'\t'+str(conf)[0:6])
            flow_robust_output.write('\n')
        flow_robust_output.close()

        biconnect_output_file = "biconnect_stat/node20neigh8vel5"
        biconnect_output = open(biconnect_output_file, 'w')
        for i in range(6):
            biconnect_output.write(str(i*0.1))
            for stat in [random_stat, degree_stat, eigen_stat, between_stat, close_stat]:
                alist = []
                for s in range(10):
                    alist.append(stat[s][1][i])
                ave = numpy.mean(alist)
                conf = numpy.std(alist)*1.96/math.sqrt(10)
                biconnect_output.write('\t'+str(ave)[0:6]+'\t'+str(conf)[0:6])
            biconnect_output.write('\n')
        biconnect_output.close()

        link_duration_output_file = "link_duration_stat/node20neigh8vel5"
        link_duration_output = open(link_duration_output_file, 'w')
        for i in range(6):
            link_duration_output.write(str(i*0.1))
            for stat in [random_stat, degree_stat, eigen_stat, between_stat, close_stat]:
                alist = []
                for s in range(10):
                    alist.append(stat[s][2][i])
                ave = numpy.mean(alist)
                conf = numpy.std(alist)*1.96/math.sqrt(10)
                link_duration_output.write('\t'+str(ave)[0:6]+'\t'+str(conf)[0:6])
            link_duration_output.write('\n')
        link_duration_output.close()
     
