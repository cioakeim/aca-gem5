"""
This script is used to explore near the estimated region 
and fine tune each benchmark's result.
"""
import numpy as np
import re
import subprocess as sp
import os
import sys
import random
from pathlib import Path
import configparser as cp


# Const variables
base_folder=os.path.abspath("../spec_cpu2006")
tuned_base="/home/chris/Documents/programms/aca/part3/results/tuned_runs/"
results_base=tuned_base
benchmarks=["401","429","456","458","470"]

# Extract the CPI from a certain run
def getCPI(results_folder:str):
    pattern = r"system\.cpu\.cpi\s+([\d\.]+)"
    filename=results_folder+"/stats.txt"
    cpi=np.inf
    with open(filename, 'r') as file:
        for line in file:
            if "system.cpu.cpi" in line:
                match = re.search(pattern, line)
                if match:
                    cpi = float(match.group(1))
                    break;
    return cpi


# Config string for a certain run
def configList(l1dsz,l1dass,
               l1isz,l1iass,
               l2sz,l2ass,
               clsz):
    list=["--l1d_size="+l1dsz,
        "--l1d_assoc="+l1dass,
        "--l1i_size="+l1isz,
        "--l1i_assoc="+l1iass,
        "--l2_size="+l2sz,
        "--l2_assoc="+l2ass,
        "--cacheline_size="+clsz]
    return list


# Wrapper of the above function for index based configs
def configFromIndices(idx):
    l1_szs=["4kB","8kB","16kB","32kB","64kB","128kB"]
    l2_szs=["64kB","128kB","256kB","512kB","1MB","2MB"]
    assoc=["2","4","8","16","32","64"]
    cache_lines=["32","64","128","256","512"]
    # Out of bounds check 
    if idx[0] not in range(len(l1_szs)):
        return []
    if idx[1] not in range(len(assoc)):
        return []
    if idx[2] not in range(len(l1_szs)):
        return []
    if idx[3] not in range(len(assoc)):
        return []
    if idx[4] not in range(len(l2_szs)):
        return []
    if idx[5] not in range(len(assoc)):
        return []
    if idx[6] not in range(len(cache_lines)):
        return []
    # From indices to config list
    return configList(l1_szs[idx[0]],
                      assoc[idx[1]],
                      l1_szs[idx[2]],
                      assoc[idx[3]],
                      l2_szs[idx[4]],
                      assoc[idx[5]],
                      cache_lines[idx[6]])



# Common command part for everyone 
def getGem5Start(results_folder):
    list=[
        "./build/ARM/gem5.opt",
        "-d",
        results_folder,
        "configs/deprecated/example/se.py",
        "--cpu-type=MinorCPU",
        "--cpu-clock=1GHz",
        "--caches",
        "--l2cache"
    ]
    return list


# The benchmark specific part of the command
def getBenchmarkCommandPart(base_folder,benchmark):
    res=["-c"]
    benchmark=str(benchmark)
    match benchmark:
        case "401":
            res.append(base_folder+"/401.bzip2/src/specbzip")
            res.append("-o")
            res.append(base_folder+"/401.bzip2/data/input.program 10")
        case "429":
            res.append(base_folder+"/429.mcf/src/specmcf")
            res.append("-o")
            res.append(base_folder+"/429.mcf/data/inp.in")
        case "456":
            res.append(base_folder+"/456.hmmer/src/spechmmer")
            res.append("-o")
            res.append("--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 "\
                +base_folder+"/456.hmmer/data/bombesin.hmm")
        case "458":
            res.append(base_folder+"/458.sjeng/src/specsjeng")
            res.append("-o")
            res.append(base_folder+"/458.sjeng/data/test.txt")
        case "470":
            res.append(base_folder+"/470.lbm/src/speclibm")
            res.append("-o")
            res.append("20 "+base_folder+"/470.lbm/data/lbm.in 0 1 "+\
                       base_folder+"/470.lbm/data/100_100_130_cf_a.of")
    res=res+["-I","100000000"]
    return res


# Combine all of the above to run a gem5 script 
def runGem5(results_folder,
            config_list,
            base_folder,
            benchmark):
    command=getGem5Start(results_folder)
    command=command+config_list
    command=command+getBenchmarkCommandPart(base_folder,benchmark)
    print(command)
    gem5_dir="/home/chris/Documents/repos/gem5"
    os.makedirs(results_folder,exist_ok=True)
    proc=sp.Popen(command,cwd=gem5_dir)
    return proc


def genPermutation(config,mask,mult):
    upper_bound=[5,5,5,5,5,5,4]
    lower_bound=[0,0,0,0,0,0,0]
    list_size=7
    probabilities = [0.8, 0.1, 0.1]
    perm = random.choices([0, -1, 1], probabilities, k=list_size)
    perm = [a&b for a,b in zip(perm,mask)]
    config= [mult*a+b for a,b in zip(perm,config)]
    config= [min(a,b) for a,b in zip(config,upper_bound)]
    config= [max(a,b) for a,b in zip(config,lower_bound)]
    return config.copy()
    

def fine_tune():
    start_dict={
        "401":[6,3,6,0,6,3,2],
        "429":[6,3,6,0,4,3,2],
        "456":[6,2,6,1,4,3,2],
        "458":[6,3,6,1,4,3,2],
        "470":[6,1,6,0,4,3,2]
    }
    benchmark=sys.argv[1]

    masks=[
        [0,0,0,0,0,0,1],
        [-1,-1,0,0,-1,-1,0],
        [0,0,-1,-1,-1,-1,0],
        [0,0,0,0,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1],
        ]

    ran_configs=[]
    run_idx=0 # For saving at appropriate folder
    mask_idx=0 # For searching at specific domains each time
    runs_per_mask=3 # For switching masks
    mult=1
    old_sample=start_dict[benchmark].copy()
    sample=start_dict[benchmark].copy()
    opt_cpi=np.inf
    while(True):
        # Prepare the run
        results_folder=results_base+"/"+str(benchmark)+"/"+f"run_{run_idx}"
        print(results_folder)
        config_list=configFromIndices(sample)
        # If the config idx if valid, run it
        if config_list!=[]:
            mult=1
            run_idx=run_idx+1
            proc=runGem5(results_folder,config_list,base_folder,
                       benchmark)
            proc.wait()
            # Compare the CPI to the current best cpi
            cpi=getCPI(results_folder)
            ran_configs.append(sample.copy())
            if cpi<opt_cpi:
                old_sample=sample.copy()
                opt_cpi=cpi
        while True:
            # Permutate the old sample
            sample=genPermutation(old_sample,masks[mask_idx],mult)
            # If it's not configuration that has been tried
            mask_idx=(mask_idx+1)%runs_per_mask
            # This is done for increasing the range of the search when stuck
            mult=mult+1 
            if sample not in ran_configs:
                break


def getRunParameters(run_folder):
    config_file=run_folder+"/config.ini"
    config=cp.ConfigParser()
    config.read(config_file)
    res={}
    res["l1d_ass"]=config["system.cpu.dcache"]["assoc"]
    res["l1d_sz"]=config["system.cpu.dcache"]["size"]
    res["l1i_ass"]=config["system.cpu.icache"]["assoc"]
    res["l1i_sz"]=config["system.cpu.icache"]["size"]
    res["l2_sz"]=config["system.l2"]["size"]
    res["l2_ass"]=config["system.l2"]["assoc"]
    res["cl"]=config["system"]["cache_line_size"]
    return res


def costOfCache(size,assoc,cache_line):
    size=float(size)
    assoc=float(assoc)
    cache_line=float(cache_line)
    return 0.8*size+0.01*(size/cache_line)**2+0.1*(size/cache_line)*assoc**2


def getCost(run_folder):
    cpi=getCPI(run_folder)
    par=getRunParameters(run_folder)
    l1d_cost=1e-3*costOfCache(par["l1d_sz"],par["l1d_ass"],par["cl"])
    l1i_cost=1e-3*costOfCache(par["l1i_sz"],par["l1i_ass"],par["cl"])
    l2_cost=1e-4*costOfCache(par["l2_sz"],par["l2_ass"],par["cl"])
    return float(cpi)*(l1d_cost+l1i_cost+l2_cost)


def getBestCPI():
    
    opt_configs=[]
    opt_cpis=[]
    for benchmark in benchmarks:
        cpi_opt=np.inf
        opt_config=-1
        base_folder = Path(tuned_base+"/"+benchmark)
        # Get best cpi
        for folder in base_folder.iterdir():
            if folder.is_dir() and folder.name.startswith("run_") and folder.name[4:].isdigit():
                # Construct the path to stats.txt
                run_number = folder.name[4:]
                stats_file = folder / "stats.txt"
                if stats_file.exists() and stats_file.stat().st_size>0:
                    #print(f"Found: {stats_file}")
                    # Do something with the stats.txt file
                    #cpi=getCPI(str(folder))
                    cpi=getCost(str(folder))
                    #print(f"CPI: {cpi} of run {run_number}")
                    if cpi<cpi_opt:
                        cpi_opt=cpi
                        opt_config=run_number
        # Append to final list
        opt_cpis.append(cpi_opt)
        opt_configs.append(opt_config)

    print(opt_cpis)
    print(opt_configs)
    for idx,benchmark in enumerate(benchmarks):
        folder=tuned_base+"/"+benchmark+"/run_"+opt_configs[idx]
        config=getRunParameters(folder)
        print(getCPI(folder))
        print(folder)
        print(config)
        




getBestCPI()











