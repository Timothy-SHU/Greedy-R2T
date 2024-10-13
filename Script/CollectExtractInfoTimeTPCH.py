# -*- coding: utf-8 -*-
import sys
import os
import time



def main(argv):
    queries = ["Q3", "Q12", "Q20", "Q5", "Q8", "Q21", "Q7", "Q11", "Q18", "Q10"]
    if len(argv) > 0:
        queries = argv
    repeat_time = 10
    output_path = "../Result/ExtractInfoTimeTPCH.txt"
    output_file = open(output_path, 'a')
    for i in range(4):
        for j in range(len(queries)):
            time_i_j = 0.0
            for k in range(repeat_time):
                print("sc_"+str(i)+" "+queries[j]+" "+str(k))
                start = time.time()
                cmd = "python ../Code/ExtractInfo.py -D sc_"+str(i)
                cmd += " -Q ../Query/"+queries[j]+".txt"
                cmd += " -K ../Query/"+queries[j]+"_key.txt"
                cmd += " -P ../Query/"+queries[j]+"_private_relation.txt"
                cmd += " -O ../Information/TempInfo.txt"
                shell = os.popen(cmd, 'r')
                shell.read()
                shell.close()
                end= time.time()
                time_i_j+=end-start
                cmd = "rm ../Information/TempInfo.txt"
                shell = os.popen(cmd, 'r')
                shell.read()
                shell.close()
            time_i_j /= repeat_time
            output_file.write("sc_"+str(i)+" "+queries[j]+" "+str(time_i_j)+"\n")
            output_file.flush()
    output_file.close()
 
if __name__ == "__main__":
	main(sys.argv[1:])
