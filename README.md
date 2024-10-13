# GreedyR2T

### Load Database
```
ProcessTPCHData.py -D <Database_Name> -d <Data_File_Name> -m <0/1:Create/Clear> -r <Relation_File_Loc>
```
E.g.
```
python ProcessTPCHData.py -D sc_0 -d _0 -m 0 -r ../Query/sc.txt
python ProcessTPCHData.py -D sc_0 -m 1
```

### Run Mechanism
```
R2T.py -I <Info_File_Loc> -b <Beta> -e <Epsilon> -G <Global_Sensitivity> -p <Processor_Num>
```
E.g.
```
python ../Code/R2T.py -I ../Information/TempInfo.txt -b 0.1 -e 0.8 -G 1000000.0 -p 4
python ../Code/Greedy.py -I ../Information/TempInfo.txt -b 0.1 -e 0.8 -G 1000000.0 -p 4
```

### Experiment:
```
ExptTPCH.py -A <Algorithm:0-R2T*,1-R2T,2-Greedy,3-TSens> -D <Database_Name> -Q <Query_Name> -R <Verbosity:d-Display,r-Record> -J <Jumpstart:0/1> -b <Beta> -e <Epsilon> -G <Global_Sensitivity> -p <Processor_Num>
```
E.g.
```
python ExptTPCH.py -A 7 -D sc_0 -Q Q3 -R d -J 1 -p 4
python ExptTPCH.py -A 4 -D sc_3 -Q Q7 -R r -J 1 -p 4
```

### Batch Experiment
```
ExptBatchTPCH.py -A <Algorithm:0-R2T*,1-R2T,2-Greedy,3-TSens> -D <Database_Name> -Q <Query_Name> -b <Beta> -e <Epsilon> -G <Global_Sensitivity> -r <Repetition> -p <Processor_Num>
```
E.g.
```
python ExptBatchTPCH.py -A 123 -D sc_0,sc_1,sc_2,sc_3 -Q Q3,Q12,Q20 -G 1000000 -e 0.8 -r 30 -p 4
python ExptBatchTPCH.py -A 123 -D sc_3 -Q Q3,Q12,Q20 -G 1000000 -e 0.1,0.2,0.4,1.6,3.2,6.4,12.8 -r 30 -p 4
python ExptBatchTPCH.py -A 123 -D sc_3 -Q Q3,Q12,Q20 -G 1000,10000,100000,10000000,100000000,1000000000 -e 0.8 -r 30 -p 4
python ExptBatchTPCH.py -A 12 -D sc_0,sc_1,sc_2,sc_3 -Q Q5,Q8,Q21 -G 1000000 -e 0.8 -r 30 -p 4
python ExptBatchTPCH.py -A 12 -D sc_0,sc_1,sc_2,sc_3 -Q Q7,Q11,Q18 -G 1000000 -e 0.8 -r 30 -p 4
```

### Collect Query / Extract Time:
```
CollectQueryTimeTPCH.py <Queries>
CollectExtractInfoTimeTPCH.py <Queries>
```
E.g.
```
python CollectQueryTimeTPCH.py Q3 Q12 Q20
python CollectQueryTimeTPCH.py Q5 Q8 Q21
python CollectQueryTimeTPCH.py Q7 Q11 Q18
python CollectExtractInfoTimeTPCH.py Q3 Q12 Q20
python CollectExtractInfoTimeTPCH.py Q5 Q8 Q21
python CollectExtractInfoTimeTPCH.py Q7 Q11 Q18
```

### Plot Figures:
```
PlotTPCH.py <Figure_Type:0-SingleEps,1-SingleGS,2-SingleScale,3-MultipleScale,4-AggregationScale>
```
E.g.
```
python PlotTPCH.py 0
python PlotTPCH.py 1
python PlotTPCH.py 2
python PlotTPCH.py 3
python PlotTPCH.py 4
```