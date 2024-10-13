# -*- coding: utf-8 -*-
import getopt
import math
import sys
import random
import numpy as np
import time
import gc
import multiprocessing
from multiprocessing.sharedctypes import Value
from ctypes import c_double
manager = multiprocessing.Manager()
gc.enable()

def LapNoise():
    a = random.uniform(0,1)
    b = math.log(1/(1-a))
    c = random.uniform(0,1)
    if c > 0.5:
        return b
    else:
        return -b

def ReadInput():
    global input_file_path
    global connections
    global weights
    global local_sensitivity
    global downward_sensitivity
    global query_result
    global query_type

    id_dic = {}
    id_num = 0
    downward_sensitivity = 0
    query_result = 0
    query_type = -1

    connections = []
    weights = []
    local_sensitivity = []
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        elements = line.split()
        if query_type == -1:
            query_type = len(elements)-1
        # The first value is the aggregation value
        aggregation_value = float(elements[0])
        # Iterate each entity contributing to this tuple
        min_element = -1
        for element in elements[1:]:
            element = int(element)
            # Re-order the IDs
            if element in id_dic.keys():
                element = id_dic[element]
            else:
                local_sensitivity.append(0)
                if query_type == 2:
                    connections.append([])
                if query_type != 1:
                    weights.append([])
                id_dic[element] = id_num
                element = id_num
                id_num += 1
            # Update Min-ID
            if min_element == -1 or element < min_element:
                min_element = element
            # Update the entity's sensitivity
            local_sensitivity[element] += aggregation_value
            # Update DS
            if downward_sensitivity <= local_sensitivity[element]:
                downward_sensitivity = local_sensitivity[element];                
        if query_type == 2:
            a = id_dic[int(elements[1])]
            b = id_dic[int(elements[2])]
            connections[min(a, b)].append(max(a, b))
        if query_type != 1:
            weights[min_element].append(aggregation_value)
        query_result += aggregation_value

def Greedy(tau_id, tau):
    global entities
    global connections
    global weights
    global local_sensitivity
    global query_type
    global Q_tau
    
    n = len(local_sensitivity)
    if query_type == 1:
        result = 0
        for cur_entity in range(n):
            result += min(local_sensitivity[cur_entity], tau)
        Q_tau[tau_id] = result
    elif query_type == 2:
        result = 0
        avail = [tau]*n
        for cur_entity in range(n):
            m = len(connections[cur_entity])
            for i in range(m):
                adj_entity = int(connections[cur_entity][i])
                truncated = min(weights[cur_entity][i], avail[cur_entity])
                truncated = min(truncated, avail[adj_entity])
                avail[cur_entity] -= truncated
                avail[adj_entity] -= truncated
                result += truncated
        Q_tau[tau_id] = result

def RunThread(base, assigned_tau_ids):
    global downward_sensitivity
    for i in assigned_tau_ids:
        tau = math.pow(base, i)
        if tau < downward_sensitivity:
            Greedy(i, tau)

def RunAlgorithm():
    global epsilon
    global beta
    global query_result
    global approximate_factor
    global global_sensitivity
    global downward_sensitivity
    global Q_tau

    base = 5.5
    Q_tau = manager.dict()
    max_i = max(int(math.log(global_sensitivity, base)), 1)
    tilde_Q_tau = {}
    hat_Q_tau = {}

    assigned_tau_ids = []
    for i in range(processor_num):
        assigned_tau_ids.append([])

    pid = 0
    for i in reversed(range(1, max_i+1)):
        tau = math.pow(base, i)
        assigned_tau_ids[pid].append(i)
        pid = (pid+1)%processor_num
        Q_tau[i] = 0

    threads = []
    for i in range(processor_num):
        threads.append(multiprocessing.Process(target = RunThread, args = (base, assigned_tau_ids[i])))
        threads[i].start()
    for i in range(processor_num):
        threads[i].join()

    max_result = 0
    for i in range(1, max_i+1):
        tau = math.pow(base, i)
        if tau >= downward_sensitivity:
            Q_tau[i] = query_result
        hat_Q_tau = Q_tau[i]+LapNoise()*tau/epsilon*max_i*(approximate_factor+1)
        tilde_Q_tau = hat_Q_tau-tau/epsilon*max_i*math.log(max_i/beta)*(approximate_factor+1)
        max_result = max(max_result, tilde_Q_tau)
    return max_result

def main(argv):
    global input_file_path
    global epsilon
    global beta
    global global_sensitivity
    global processor_num
    processor_num = 4
    global approximate_factor
    approximate_factor = 0
    global query_result
    global query_type
    try:
        opts, args = getopt.getopt(argv,"h:I:e:b:G:p:",["Input=","epsilon=","beta=","GlobalSensitivity=","ProcessorNum="])
    except getopt.GetoptError:
        print("Greedy.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("Greedy.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)>")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_file_path = str(arg)
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b","--beta"):
            beta = float(arg)
        elif opt in ("-G","--GlobalSensitivity"):
            global_sensitivity = float(arg)
        elif opt in ("-p","--ProcessorNum"):
            processor_num = int(arg)
    start = time.time()
    ReadInput()
    if query_type >= 3:
        print("Not Supported!")
        os.abort()
    res = RunAlgorithm()
    end = time.time()
    print("Query Result:", query_result)
    print("Noised Result:", res)
    print("Error:", abs(query_result-res))
    print("Error Rate:", abs(query_result-res)/query_result*100, "%")
    print("Time:", end-start)

if __name__ == "__main__":
    main(sys.argv[1:])
