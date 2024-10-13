# -*- coding: utf-8 -*-
import sys
import os
import psycopg2
import time


def main(argv):
    queries = ["Q3", "Q12", "Q20", "Q5", "Q8", "Q21", "Q7", "Q11", "Q18", "Q10"]
    if len(argv) > 0:
        queries = argv
    repeat_time = 30
    times = []
    for i in range(4):
        for j in range(len(queries)):
            query = ""
            query_path = "../Query/"+queries[j]+".txt"
            query_file = open(query_path,'r')
            # Read the query file and store in query
            for line in query_file.readlines():
                query = query + line
                if ";" in query:
                    query = query.replace('\n'," ")
                    break

            con = psycopg2.connect(database = "sc_"+str(i))
            cur = con.cursor()
            output_path = "../Result/SQL/"+queries[j]+",sc_"+str(i)+".txt"
            output_file = open(output_path, 'w')
            for k in range(repeat_time):
                print("sc_"+str(i), queries[j], k)
                start = time.time()
                cur.execute(query)
                res = cur.fetchall()
                end = time.time()
                output_file.write(str(res[0][0])+" 0 "+str(end-start)+'\n')
            con.commit()
            con.close()

if __name__ == "__main__":
	main(sys.argv[1:])
    

