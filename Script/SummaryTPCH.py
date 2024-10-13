# -*- coding: utf-8 -*-
import os
import sys

def ReadData(path):
    try:
        cnt = 0; time = 0
        errs = []; rates = []
        input_file = open(path, 'r')
        for line in input_file.readlines():
            elements = line.split()
            errs.append(float(elements[0]))
            rates.append(float(elements[1]))
            time += float(elements[2]); cnt += 1
        input_file.close()
        if cnt < 30:        
            print("Not Enough Samples:", cnt, "Samples,", path)
        if int(cnt/10)*10 != cnt:
            print("Sample Count Not Divisible:", cnt, "Samples,", path)
        left = int(cnt*0.1); right = int(cnt*0.9); width = right-left
        errs.sort(); err = sum(errs[left:right])/width
        rates.sort(); rate = sum(rates[left:right])/width
        return err, rate, time/cnt
    except:
        print("File Not Exist:", path)
        return 0, 0, 0

if __name__ == "__main__":
    InfoTime = {}
    input_file = open("../Result/ExtractInfoTimeTPCH.txt", 'r')
    for line in input_file.readlines():
        elements = line.split()
        InfoTime[(elements[0], elements[1])] = float(elements[2])
    input_file.close()

    queries = ["Q3", "Q12", "Q20", "Q5", "Q8", "Q21", "Q7", "Q11", "Q18", "Q10"]
    results = [2888656, 6001215, 6001215, 239917, 1829418, 6001215, 218102224, 2003609, 153078795, 1500000]
    algorithms = ["R2T", "Greedy", "TSensDP"]

    SQL = [[], []]
    for i in range(len(queries)):
        qry = queries[i]; res = results[i]; time = InfoTime[("sc_3", qry)]
        print("SQL, {:>3}: {:>11,} {:>4.1f}".format(qry, res, time))
        SQL[0].append(res); SQL[1].append(time)
    print()

    algo_res = []
    for j in range(len(algorithms)):
        algo_res.append([[], [], []])
        for i in range(len(queries)):
            qry = queries[i]; algo = algorithms[j]
            if algo == "TSensDP" and qry not in ["Q3", "Q12", "Q20"]: continue
            result_path = "../Result/"+algo+"/"+qry+",sc_3,0.8,0.1,1000000.txt" 
            err, rate, time = ReadData(result_path); time += InfoTime[("sc_3", qry)]
            print("{:>7}, {:>3}: {:>9,.0f} {:>6.3f} {:>5.1f}".format(algo, qry, err, rate, time))
            algo_res[j][0].append(err); algo_res[j][1].append(rate); algo_res[j][2].append(time)
    print()
    
    print("{:>8}".format(" "), end = '')
    for i in range(len(queries)):
        print("{:>13}".format(queries[i]), end = '')
    print()
    print("-"*138)
    print("{:>8}".format("SQL"), end = '')
    for i in range(len(queries)):
        print("{:>13,}".format(SQL[0][i]), end = '')
    print()
    print("{:>8}".format(" "), end = '')
    for i in range(len(queries)):
        print("{:>13.1f}".format(SQL[1][i]), end = '')
    print()
    print("-"*138)
    for j in range(len(algorithms)):
        print("{:>8}".format(algorithms[j]), end = '')
        for i in range(len(algo_res[j][0])):
            print("{:>13,.0f}".format(algo_res[j][0][i]), end = '')
        print()
        print("{:>8}".format(" "), end = '')
        for i in range(len(algo_res[j][1])):
            print("{:>13.3f}".format(algo_res[j][1][i]), end = '')
        print()
        print("{:>8}".format(" "), end = '')
        for i in range(len(algo_res[j][2])):
            print("{:>13.1f}".format(algo_res[j][2][i]), end = '')
        print()
        print("-"*138)
