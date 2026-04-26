

#first paramterize the runGem5.sh script
#read the correct fields in the correct file,
#calculate CPI

import subprocess 
import os
import re


# = "./runGem5.sh"
#subprocess.run(["./runGem5_param.sh"])


#sys.exit(0)
#calculate CPI
def calculate_CPI(benchmark, L1D_SIZE="128kB", L1I_SIZE="128kB", L2_SIZE="1MB", L1D_ASSOC="2", L1I_ASSOC="2", L2_ASSOC="1", CACHE_LINE="64"):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "runGem5_param.sh")
    subprocess.run([script_path, benchmark, L1D_SIZE, L1I_SIZE, L2_SIZE, L1D_ASSOC, L1I_ASSOC, L2_ASSOC, CACHE_LINE ])
    stats = { '401.bzip2' : "401.bzip2/m5out/stats.txt",
              '429.mcf': "429.mcf/m5out/stats.txt",
              '456.hmmer': "456.hmmer/m5out/stats.txt",
              '458.sjeng': "458.sjeng/m5out/stats.txt" ,
              '470.lbm': "470.lbm/m5out/stats.txt" , 
    }
    file = open(stats[benchmark], "r")
    lines = file.readlines()
    numInsts = 1
    dcacheMisses = 0
    icacheMisses = 0
    l2Misses = 0
    for line in lines:
        pattern = r'(?<!\S)\d+(?!\S)'
        if "system.cpu.commitStats0.numInsts " in line:
            numInsts = re.findall(pattern, line)[0]
        if "system.cpu.dcache.overallMisses::total" in line:
            print("found dcahce misses")
            dcacheMisses = re.findall(pattern, line)[0]
        if "system.cpu.icache.overallMisses::total" in line:
            icacheMisses = re.findall(pattern, line)[0]
        if "system.l2.overallMisses::total" in line:
            l2Misses = re.findall(pattern, line)[0]
    print("dcacheMisses", dcacheMisses)
    print("icacheMisses", icacheMisses)
    print("l2Misses", l2Misses)
    print("numInsts", numInsts)
    print(((int(dcacheMisses) + int(icacheMisses))*6 + int(l2Misses)*50)/int(numInsts))
    CPI = 1+((int(dcacheMisses) + int(icacheMisses))*6 + int(l2Misses)*50)/int(numInsts)
        
    return CPI

#print("401.bzip2",calculate_CPI("401.bzip2"))
#print("429.mcf", calculate_CPI("429.mcf"))
#print("456.hmmer", calculate_CPI("456.hmmer"))
#print("458.sjeng", calculate_CPI("458.sjeng"))
#print("470.lbm", calculate_CPI("470.lbm"))
#results = []
#for i in range(1, 100):
 #   results.append(    (i,calculate_CPI("429.mcf", L1D_ASSOC=str(i), L1I_ASSOC=str(i) ))   )
    
#print(results)
    
benchmarks = ["401.bzip2","429.mcf", "456.hmmer", "458.sjeng", "470.lbm"]
import os 

#test_block_size
"""
block_results = []
for benchmark in benchmarks:
    result = [benchmark]
    block_sizes = ["32","64","128"]
    for block_size in block_sizes:
        cpi = calculate_CPI(benchmark, CACHE_LINE=block_size)
        result.append(cpi)
    block_results.append(result)
print("BLOCK RESULTS")
print(block_results)
with open("tradeoff_results.txt", "w") as file:
    file.write("BLOCK RESULTS\n")

    for row in block_results:
        file.write(",".join(map(str, row)) + "\n")
    

l2assoc_results = []
for benchmark in benchmarks:
    result = [benchmark]
    assoc_sizes = ["1","2","4","8"]
    for assoc_size in assoc_sizes:
        cpi = calculate_CPI(benchmark, L2_ASSOC=assoc_size)
        result.append(cpi)
    l2assoc_results.append(result)
    
print("L2 ASSOC RESULTS")
print(["1","2","4","8"])
print(l2assoc_results)
with open("tradeoff_results.txt", "a") as file:
    file.write("L2 ASSOC RESULTS\n")
    for row in l2assoc_results:
        file.write(",".join(map(str, row)) + "\n")

l1dassoc_results = []
for benchmark in benchmarks:
    result = [benchmark]
    assoc_sizes = ["1","2","4","8"]
    for assoc_size in assoc_sizes:
        cpi = calculate_CPI(benchmark, L1D_ASSOC=assoc_size)
        result.append(cpi)
    l1dassoc_results.append(result)
print("L1D ASSOC RESULTS")
print(["1","2","4","8"])
print(l1dassoc_results)
with open("tradeoff_results.txt", "a") as file:
    file.write("L1D ASSOC RESULTS\n")
    file.write(",".join(["1","2","4","8"]))
    for row in l1dassoc_results:
        file.write(",".join(map(str, row)) + "\n")

l1iassoc_results = []
for benchmark in benchmarks:
    result = [benchmark]
    assoc_sizes = ["1","2","4","8"]
    for assoc_size in assoc_sizes:
        cpi = calculate_CPI(benchmark, L1I_ASSOC=assoc_size)
        result.append(cpi)
    l1iassoc_results.append(result)
print("L1i ASSOC RESULTS")
print(l1iassoc_results)
with open("tradeoff_results.txt", "a") as file:
    file.write("L1I ASSOC RESULTS\n")
    file.write(",".join(["1","2","4","8"]))
    for row in l1iassoc_results:
        file.write(",".join(map(str, row)) + "\n")



l2size_results = []
for benchmark in benchmarks:
    result = [benchmark]
    sizes = ["512kB", "1MB", "2MB", "4MB"]
    for size in sizes:
        cpi = calculate_CPI(benchmark, L2_ASSOC="4", L2_SIZE=size)
        result.append(cpi)
    l2size_results.append(result)
print("L2 SIZE RESULTS")
print(l2size_results)
with open("tradeoff_results.txt", "a") as file:
    file.write("L2 SIZE RESULTS\n")
    file.write(",".join(["512kB", "1MB", "2MB", "4MB"]))
    for row in l2size_results:
        file.write(",".join(map(str, row)) + "\n")
        
"""
l1size_results = []
for benchmark in benchmarks:
    result = [benchmark]
    sizes = sizes = [
    ("128kB", "128kB"),
    ("256kB", "128kB"),
    ("256kB", "256kB")
]
    for size in sizes:
        cpi = calculate_CPI(benchmark, L1D_SIZE=size[0], L1I_SIZE=size[1])
        result.append(cpi)
    l1size_results.append(result)

print("L1 Icache and Dcache SIZE RESULTS")
print([("128kB", "384kB"), ("256kB", "256kB"),("384kB", "128kB")])
print(l1size_results)
with open("tradeoff_results.txt", "a") as file:
    file.write("L1 SIZE RESULTS\n")
    for row in l1size_results:
        file.write(",".join(map(str, row)) + "\n")
"""

print("BLOCK RESULTS")
print(["16","32","64","128"])
print(block_results)

print("L2 ASSOC RESULTS")
print(["1","2","4","8"])
print(l2assoc_results)

print("L1D ASSOC RESULTS")
print(["1","2","4","8"])
print(l1dassoc_results)    

print("L1I ASSOC RESULTS")
print(["1","2","4","8"])
print(l1dassoc_results)  
    
print("L2 SIZE RESULTS")
print(["512Kb", "1MB", "2MB", "4MB"])
print(l2size_results)    
    
print("L1 Icache and Dcache SIZE RESULTS")
print([("128kB", "384kB"), ("256kB", "256kB"),("384kB", "128kB")])
print(l1size_results)

benchmarks = ["401.bzip2","429.mcf", "456.hmmer", "458.sjeng", "470.lbm"]
results = []
for benchmark in benchmarks:
    cpi = calculate_CPI(benchmark, L1D_SIZE="256kB", L1I_SIZE="128kB", CACHE_LINE="128")
    results.append([benchmark,cpi])
print("optimized cpi", results)
"""   
#print(calculate_CPI("456.hmmer", L1D_SIZE="256kB", L1I_SIZE="4MB", CACHE_LINE="128")) 






    
        
        
