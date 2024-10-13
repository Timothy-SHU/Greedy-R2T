import os
import sys
import getopt

def main(argv):
    repeat = 10
    algorithms = 2
    databases = ["sc_3"]
    queries = ["Q3"]
    epsilons = [0.8]
    betas = [0.1]
    sensitivities = [1000000]
    processor_num = -1
    
    try:
        opts, args = getopt.getopt(argv, "D:Q:A:e:b:G:r:p:")
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-D":
            databases = arg.split(',')
        elif opt == "-Q":
            queries = arg.split(',')
        elif opt == "-A":
            algorithms = int(arg)
        elif opt == "-e":
            epsilons = [float(eps) for eps in arg.split(',')]
        elif opt == "-b":
            betas = [float(beta) for beta in arg.split(',')]
        elif opt == "-G":
            sensitivities = [int(GS) for GS in arg.split(',')]
        elif opt == "-r":
            repeat = int(arg)
        elif opt == "-p":
            processor_num = int(arg)
    for db in databases:
        for qry in queries:
            for eps in epsilons:
                for beta in betas:
                    for GS in sensitivities:
                        print(">>>>>", db, qry, eps, beta, GS, "<<<<<")
                        for T in range(repeat):
                            cmd = "python ExptTPCH.py -D "+db+" -Q "+qry+" -A "+str(algorithms)
                            cmd += " -e "+str(eps)+" -b "+str(beta)+" -G "+str(GS)+" -R r -J 1"
                            if processor_num != -1:
                                cmd += " -p "+str(processor_num)
                            os.system(cmd)
                            print("T", T, sep = '', end = ' ')
                            sys.stdout.flush()
                        print("")

if __name__ == "__main__":
    main(sys.argv[1:])
