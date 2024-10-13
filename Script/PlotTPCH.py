# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt

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

def main(argv):
    InfoTime = {}
    input_file = open("../Result/ExtractInfoTimeTPCH.txt", 'r')
    for line in input_file.readlines():
        elements = line.split()
        InfoTime[(elements[0], elements[1])] = float(elements[2])
    input_file.close()

    if argv[0] == '0':
        queries = ["Q3", "Q12", "Q20"]
        queries_name = [r"Q$_3$", r"Q$_{12}$", r"Q$_{20}$"]
        results = [2888656, 6001215, 6001215]
        algorithms = ["R2T", "Greedy", "TSensDP"]
        algorithms_name = [r"R2T$_\text{LP}$", "Greedy", "TSensDP"]
        epsilons = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]

        res = []
        for i in range(len(queries)):
            res.append([])
            for j in range(len(algorithms)):
                res[i].append([])
                for k in range(len(epsilons)):
                    qry = queries[i]; algo = algorithms[j]; eps = epsilons[k]
                    result_path = "../Result/"+algo+"/"+qry+",sc_3,"+str(eps)+",0.1,1000000.txt" 
                    err, rate, time = ReadData(result_path)
                    res[i][j].append(err)
       
        markers = ['s', '^', 'v']
        markeredgewidths = [1, 2, 2]
        linestyles = ['-.', '--', '--']
        colors = [plt.cm.tab20c(0), plt.cm.tab20c(6), plt.cm.tab20c(4)]
        fig, axes = plt.subplots(1, 3, figsize = (20, 6))
        for i in range(len(queries)):
            axes[i].set_xscale('log')
            axes[i].set_yscale('log')
            axes[i].set_xticks(epsilons, epsilons)
            axes[i].set_title(queries_name[i], fontsize = 18)
            axes[i].tick_params(axis = 'both', which = 'major', labelsize = 15)
            axes[i].set_xlabel(r"Privacy Budget ($\epsilon$)", fontsize = 18)
            axes[i].set_facecolor("white")
            for k in range(9):
                val = int(pow(10, k)); mi = val+1; mx = val-1
                for j in range(len(algorithms)):
                    mi = min(mi, min(res[i][j])); mx = max(mx, max(res[i][j]))
                if val >= mi and val <= mx:
                    axes[i].axhline(y = val, color = plt.cm.tab20c(19))
            for j in range(len(algorithms)):
                axes[i].plot(epsilons, res[i][j], label = algorithms_name[j], 
                             linestyle = linestyles[j], linewidth = 2, color = colors[j], 
                             marker = markers[j], markersize = 8, markerfacecolor = colors[j], 
                             markeredgewidth = markeredgewidths[j], markeredgecolor = colors[j])
            axes[i].axhline(y = results[i], linestyle = "--", linewidth = 2, 
                            color = plt.cm.tab20c(9), label = 'Query Result')
        axes[0].set_ylabel("Error Level", fontsize = 18)
        axes[0].legend(bbox_to_anchor = (0.42, 1.25), fontsize = 12, ncol = 2, facecolor = "white")
        fig.tight_layout()
        plt.savefig("../Result/SingleEps.pdf")
        plt.show(block = True)

    elif argv[0] == '1':
        queries = ["Q3", "Q12", "Q20"]
        queries_name = ["Q$_3$", "Q$_{12}$", "Q$_{20}$"]
        results = [2888656, 6001215, 6001215]
        algorithms = ["R2T", "Greedy", "TSensDP"]
        algorithms_name = [r"R2T$_\text{LP}$", "Greedy", "TSensDP"]
        sensitivities = [1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]

        res = []
        for i in range(len(queries)):
            res.append([])
            for j in range(len(algorithms)):
                res[i].append([])
                for k in range(len(sensitivities)):
                    qry = queries[i]; algo = algorithms[j]; GS = sensitivities[k]
                    result_path = "../Result/"+algo+"/"+qry+",sc_3,0.8,0.1,"+str(GS)+".txt" 
                    err, rate, time = ReadData(result_path)
                    res[i][j].append(err)
       
        markers = ['s', '^', 'v']
        markeredgewidths = [1, 2, 2]
        linestyles = ['-.', '--', '--']
        colors = [plt.cm.tab20c(0), plt.cm.tab20c(6), plt.cm.tab20c(4)]
        fig, axes = plt.subplots(1, 3, figsize = (20, 6))
        for i in range(len(queries)):
            axes[i].set_xscale('log')
            axes[i].set_yscale('log')
            axes[i].set_title(queries_name[i], fontsize = 18)
            axes[i].tick_params(axis = 'both', which = 'major', labelsize = 15)
            axes[i].set_xlabel(r"Global Sensitivity (GS$_\text{Q}$)", fontsize = 18)
            axes[i].set_facecolor("white")
            for k in range(9):
                val = int(pow(10, k)); mi = val+1; mx = val-1
                for j in range(len(algorithms)):
                    mi = min(mi, min(res[i][j])); mx = max(mx, max(res[i][j]))
                if val >= mi and val <= mx:
                    axes[i].axhline(y = val, color = plt.cm.tab20c(19))
            for j in range(len(algorithms)):
                axes[i].plot(sensitivities, res[i][j], label = algorithms_name[j], 
                             linestyle = linestyles[j], linewidth = 2.5, color = colors[j], 
                             marker = markers[j], markersize = 8, markerfacecolor = colors[j], 
                             markeredgewidth = markeredgewidths[j], markeredgecolor = colors[j])
            axes[i].axhline(y = results[i], linestyle = "--", linewidth = 2, 
                            color = plt.cm.tab20c(9), label = 'Query Result')
        axes[0].set_ylabel("Error Level", fontsize = 18)
        axes[0].legend(bbox_to_anchor = (0.42, 1.25), fontsize = 12, ncol = 2, facecolor = "white")
        fig.tight_layout()
        plt.savefig("../Result/SingleGS.pdf")
        plt.show(block = True)

    elif argv[0] == '2':
        queries = ["Q3", "Q12", "Q20"]
        queries_name = ["Q$_3$", "Q$_{12}$", "Q$_{20}$"]
        time_slice = [5, 10, 10]
        algorithms = ["R2T", "Greedy", "TSensDP", "Query Result"]
        algorithms_name = [r"R2T$_\text{LP}$", "Greedy", "TSensDP", "Query Result"]
        scales = [0.125, 0.25, 0.5, 1]

        res = []
        for i in range(len(queries)):
            res.append([])
            for j in range(len(algorithms)-1):
                res[i].append([[], []])
                for k in range(len(scales)):
                    qry = queries[i]; algo = algorithms[j]; db = "sc_"+str(k)
                    result_path = "../Result/"+algo+"/"+qry+","+db+",0.8,0.1,1000000.txt"
                    err, rate, time = ReadData(result_path)
                    res[i][j][0].append(err)
                    res[i][j][1].append(time+InfoTime[(db, qry)])
            res[i].append([[], []])
            for k in range(len(scales)):
                result_path = "../Result/SQL/"+qry+",sc_"+str(k)+".txt"
                err, rate, time = ReadData(result_path)
                res[i][len(algorithms)-1][0].append(err)
                res[i][len(algorithms)-1][1].append(time)
       
        markers = ['s', '^', 'v', 'o']
        markeredgewidths = [1, 2, 2, 1]
        linestyles = ['-.', '--', '--', ':']
        colors = [plt.cm.tab20c(0), plt.cm.tab20c(6), plt.cm.tab20c(4), plt.cm.tab20c(9)]
        fig, axes = plt.subplots(2, 3, figsize = (20, 9))
        for l in range(2):
            for i in range(len(queries)):
                axes[l, i].set_xticks(np.arange(4), scales)
                axes[l, i].tick_params(axis = 'both', which = 'major', labelsize = 15)
                axes[l, i].set_facecolor("white")
                for k in range(10):
                    if l == 0: val = int(pow(10, k))
                    else: val = int(time_slice[i]*k)
                    mi = val+1; mx = val-1
                    for j in range(len(algorithms)):
                        mi = min(mi, min(res[i][j][l])); mx = max(mx, max(res[i][j][l]))
                    if val > mx: break
                    if val >= mi or l == 1:
                        axes[l, i].axhline(y = val, color = plt.cm.tab20c(19))
                for j in range(len(algorithms)):
                    axes[l, i].plot(np.arange(4), res[i][j][l], label = algorithms_name[j], 
                                    linestyle = linestyles[j], linewidth = 2.5, color = colors[j], 
                                    marker = markers[j], markersize = 8, markerfacecolor = colors[j], 
                                    markeredgewidth = markeredgewidths[j], markeredgecolor = colors[j])
        axes[0, 0].set_ylabel("Error Level", fontsize = 18)
        axes[1, 0].set_ylabel("Running Time (s)", fontsize = 18)
        for i in range(len(queries)):
            axes[0, i].set_yscale('log')
            axes[0, i].set_title(queries_name[i], fontsize = 18)
            axes[1, i].set_xlabel("Dataset Scale", fontsize = 18)
        axes[0, 0].legend(bbox_to_anchor = (0.42, 1.3), fontsize = 12, ncol = 2, facecolor = "white")
        fig.tight_layout()
        plt.savefig("../Result/SingleScale.pdf")
        plt.show(block = True)

    elif argv[0] == '3':
        queries = ["Q5", "Q8", "Q21"]
        queries_name = ["Q$_5$", "Q$_8$", "Q$_{21}$"]
        time_slice = [1, 10, 50]
        algorithms = ["R2T", "Greedy", "Query Result"]
        algorithms_name = [r"R2T$_\text{LP}$", "Greedy", "Query Result"]
        scales = [0.125, 0.25, 0.5, 1]

        res = []
        for i in range(len(queries)):
            res.append([])
            for j in range(len(algorithms)-1):
                res[i].append([[], []])
                for k in range(len(scales)):
                    qry = queries[i]; algo = algorithms[j]; db = "sc_"+str(k)
                    result_path = "../Result/"+algo+"/"+qry+","+db+",0.8,0.1,1000000.txt" 
                    err, rate, time = ReadData(result_path)
                    res[i][j][0].append(err)
                    res[i][j][1].append(time+InfoTime[(db, qry)])
            res[i].append([[], []])
            for k in range(len(scales)):
                result_path = "../Result/SQL/"+qry+",sc_"+str(k)+".txt"
                err, rate, time = ReadData(result_path)
                res[i][len(algorithms)-1][0].append(err)
                res[i][len(algorithms)-1][1].append(time)
       
        markers = ['s', '^', 'o']
        markeredgewidths = [1, 2, 1]
        linestyles = ['-.', '--', ':']
        colors = [plt.cm.tab20c(0), plt.cm.tab20c(6), plt.cm.tab20c(9)]
        fig, axes = plt.subplots(2, 3, figsize = (20, 8))
        for l in range(2):
            for i in range(len(queries)):
                axes[l, i].set_xticks(np.arange(4), scales)
                axes[l, i].tick_params(axis = 'both', which = 'major', labelsize = 15)
                axes[l, i].set_facecolor("white")
                for k in range(10):
                    if l == 0: val = int(pow(10, k))
                    else: val = int(time_slice[i]*k)
                    mi = val+1; mx = val-1
                    for j in range(len(algorithms)):
                        mi = min(mi, min(res[i][j][l])); mx = max(mx, max(res[i][j][l]))
                    if val > mx: break
                    if val >= mi or l == 1:
                        axes[l, i].axhline(y = val, color = plt.cm.tab20c(19))
                for j in range(len(algorithms)):
                    axes[l, i].plot(np.arange(4), res[i][j][l], label = algorithms_name[j], 
                                    linestyle = linestyles[j], linewidth = 2.5, color = colors[j], 
                                    marker = markers[j], markersize = 8, markerfacecolor = colors[j], 
                                    markeredgewidth = markeredgewidths[j], markeredgecolor = colors[j])
        axes[0, 0].set_ylabel("Error Level", fontsize = 18)
        axes[1, 0].set_ylabel("Running Time (s)", fontsize = 18)
        for i in range(len(queries)):
            axes[0, i].set_yscale('log')
            # axes[1, i].set_yscale('log')
            axes[0, i].set_title(queries_name[i], fontsize = 18)
            axes[1, i].set_xlabel("Dataset Scale", fontsize = 18)
        axes[0, 0].legend(bbox_to_anchor = (0.65, 1.27), fontsize = 12, ncol = 3, facecolor = "white")
        fig.tight_layout()
        plt.savefig("../Result/MultipleScale.pdf")
        plt.show(block = True)

    elif argv[0] == '4':
        queries = ["Q7", "Q11", "Q18"]
        queries_name = ["Q$_7$", "Q$_{11}$", "Q$_{18}$"]
        time_slice = [50, 2, 20]
        algorithms = ["R2T", "Greedy", "Query Result"]
        algorithms_name = [r"R2T$_\text{LP}$", "Greedy", "Query Result"]
        scales = [0.125, 0.25, 0.5, 1]

        res = []
        for i in range(len(queries)):
            res.append([])
            for j in range(len(algorithms)-1):
                res[i].append([[], []])
                for k in range(len(scales)):
                    qry = queries[i]; algo = algorithms[j]; db = "sc_"+str(k)
                    result_path = "../Result/"+algo+"/"+qry+","+db+",0.8,0.1,1000000.txt" 
                    err, rate, time = ReadData(result_path)
                    res[i][j][0].append(err)
                    res[i][j][1].append(time+InfoTime[(db, qry)])
            res[i].append([[], []])
            for k in range(len(scales)):
                result_path = "../Result/SQL/"+qry+",sc_"+str(k)+".txt"
                err, rate, time = ReadData(result_path)
                res[i][len(algorithms)-1][0].append(err)
                res[i][len(algorithms)-1][1].append(time)
       
        markers = ['s', '^', 'o']
        markeredgewidths = [1, 2, 1]
        linestyles = ['-.', '--', ':']
        colors = [plt.cm.tab20c(0), plt.cm.tab20c(6), plt.cm.tab20c(9)]
        fig, axes = plt.subplots(2, 3, figsize = (20, 8))
        for l in range(2):
            for i in range(len(queries)):
                axes[l, i].set_xticks(np.arange(4), scales)
                axes[l, i].tick_params(axis = 'both', which = 'major', labelsize = 15)
                axes[l, i].set_facecolor("white")
                for k in range(10):
                    if l == 0: val = int(pow(10, k))
                    else: val = int(time_slice[i]*k)
                    mi = val+1; mx = val-1
                    for j in range(len(algorithms)):
                        mi = min(mi, min(res[i][j][l])); mx = max(mx, max(res[i][j][l]))
                    if val > mx: break
                    if val >= mi or l == 1:
                        axes[l, i].axhline(y = val, color = plt.cm.tab20c(19))
                for j in range(len(algorithms)):
                    axes[l, i].plot(np.arange(4), res[i][j][l], label = algorithms_name[j], 
                                    linestyle = linestyles[j], linewidth = 2.5, color = colors[j], 
                                    marker = markers[j], markersize = 8, markerfacecolor = colors[j], 
                                    markeredgewidth = markeredgewidths[j], markeredgecolor = colors[j])
        axes[0, 0].set_ylabel("Error Level", fontsize = 18)
        axes[1, 0].set_ylabel("Running Time (s)", fontsize = 18)
        for i in range(len(queries)):
            axes[0, i].set_yscale('log')
            # axes[1, i].set_yscale('log')
            axes[0, i].set_title(queries_name[i], fontsize = 18)
            axes[1, i].set_xlabel("Dataset Scale", fontsize = 18)
        axes[0, 0].legend(bbox_to_anchor = (0.65, 1.27), fontsize = 12, ncol = 3, facecolor = "white")
        fig.tight_layout()
        plt.savefig("../Result/AggregationScale.pdf")
        plt.show(block = True)
        
if __name__ == "__main__":
	main(sys.argv[1:])
