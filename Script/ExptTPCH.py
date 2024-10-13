import os
import sys
import getopt

def record(algo_name, res):
    global query_name
    global database_name
    global epsilon
    global beta 
    global global_sensitivity
    res = res.split()
    file = open("../Result/"+algo_name+"/"+query_name+','+database_name+','+str(epsilon)+','+str(beta)+','+str(int(global_sensitivity))+".txt", "a")
    file.write(res[7]+' '+res[10]+' '+res[13]+'\n')
    file.close()

def main(argv):
    global database_name
    global query_name
    global query_path
    global private_relation_path
    global primary_key_path
    global epsilon
    global beta
    global global_sensitivity
    global processor_num

    epsilon = 0.8
    beta = 0.1
    global_sensitivity = 1000000
    processor_num = 4

    display_result = 0
    record_result = 0
    include_R2T_wo_ES = 0
    include_R2T = 0
    include_Greedy = 0
    include_TSensDP = 0
    jump_start = 0

    try:
        opts, args = getopt.getopt(argv, "h:D:Q:e:b:G:p:R:A:J:")
    except getopt.GetoptError:
        print("System.py -A <algorithms> -D <database name> -Q <query name> -e <epsilon(default 0.8)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)> -R <display/record result> -J <jump start>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("System.py -A <algorithms> -D <database name> -Q <query name> -e <epsilon(default 0.8)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)> -R <display/record result> -J <jump start>")
            sys.exit()
        elif opt in ("-D", "--Database"):
            database_name = arg
        elif opt in ("-Q", "--QueryPath"):
            query_name = arg
            query_path = "../Query/"+arg+".txt"
            private_relation_path = "../Query/"+arg+"_private_relation.txt"
            primary_key_path = "../Query/"+arg+"_key.txt"
        elif opt in ("-e", "--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b", "--beta"):
            beta = float(arg)
        elif opt in ("-G", "--GlobalSensitivity"):
            global_sensitivity = float(arg)
        elif opt in ("-p", "--ProcessorNum"):
            processor_num = int(arg)
        elif opt == "-R":
            if "d" in arg:
                display_result = 1
            if "r" in arg:
                record_result = 1
        elif opt == "-A":
            if "0" in arg:
                include_R2T_wo_ES = 1
            if "1" in arg:
                include_R2T = 1
            if "2" in arg:
                include_Greedy = 1
            if "3" in arg:
                include_TSensDP = 1
        elif opt == "-J":
            jump_start = int(arg)

    info_path = "../Information/TPCH/"+query_name+database_name[2:]+".txt"
    if jump_start == 0:
        cmd = "python ../Code/ExtractInfo.py -D "+database_name+" -Q "+query_path
        cmd = cmd+" -P "+private_relation_path+" -K "+primary_key_path+" -O "+"../Information/TempInfo.txt"
        shell = os.popen(cmd, 'r')
        shell.read()
        shell.close()
        info_path = "../Information/TempInfo.txt"

    if display_result == 1:
        print(">>>>>", database_name+',', query_name+',', "GS =", str(global_sensitivity), "<<<<<\n")
    
    if include_R2T_wo_ES == 1:
        cmd = "python ../Code/R2T_wo_ES.py -I "+info_path
        cmd = cmd+" -b"+str(beta)+" -e "+str(epsilon)+" -G "+str(global_sensitivity)+" -p "+str(processor_num)
        shell = os.popen(cmd, 'r')
        res = shell.read()
        shell.close()
        if display_result == 1:
            print("------------ R2T* -----------");
            print(res)
        if record_result == 1:
            record("R2T_wo_ES", res)

    if include_R2T == 1:
        cmd = "python ../Code/R2T.py -I "+info_path
        cmd = cmd+" -b"+str(beta)+" -e "+str(epsilon)+" -G "+str(global_sensitivity)+" -p "+str(processor_num)
        shell = os.popen(cmd, 'r')
        res = shell.read()
        shell.close()
        if display_result == 1:
            print("------------ R2T ------------");
            print(res)
        if record_result == 1:
            record("R2T", res)

    if include_Greedy == 1:
        cmd = "python ../Code/Greedy.py -I "+info_path
        cmd = cmd+" -b"+str(beta)+" -e "+str(epsilon)+" -G "+str(global_sensitivity)+" -p "+str(processor_num)
        shell = os.popen(cmd, 'r')
        res = shell.read()
        shell.close()
        if display_result == 1:
            print("----------- Greedy ----------");
            print(res)
        if record_result == 1:
            record("Greedy", res)

    if include_TSensDP == 1:
        cmd = "python ../Code/TSensDP.py -I "+info_path
        cmd = cmd+" -e "+str(epsilon)+" -G "+str(int(global_sensitivity))
        shell = os.popen(cmd, 'r')
        res = shell.read()
        shell.close()
        if display_result == 1:
            print("---------- TSensDP ----------");
            print(res)
        if record_result == 1:
            record("TSensDP", res)
    if jump_start == 0:
        cmd = "rm Information/TempInfo.txt"
        shell = os.popen(cmd, 'r')
        shell.read()
        shell.close()

if __name__ == "__main__":
    main(sys.argv[1:])
