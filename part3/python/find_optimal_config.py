import numpy as np 
import os

base_folder="/home/chris/Documents/programms/aca/aca-gem5/part3/results/extracted"
benchmarks=["401","429","456","458","470"]


def getCsvFromResults(results_file: str):
    data=np.genfromtxt(results_file,delimiter="\t",dtype="str",skip_header=1)
    data[:,0]=np.arange(0,data.shape[0]).astype(str)
    data=data.astype(float)
    data=data[:,1:]
    return data


def CostfromStats(
    l1d_mr,
    l1i_mr,
    l2_inst_mr,l2_inst_avg_lat,
    l2_data_mr,l2_data_avg_lat):
    # Constants
    l1_hit_cycles=6
    l2_hit_cycles=60
    ticks_per_cycle=1000
    # Start from L2 and compute mean delay for data and instr,
    # all values below are in cycles
    tl2_d=l2_hit_cycles+l2_data_mr*(l2_data_avg_lat/ticks_per_cycle)
    tl2_i=l2_hit_cycles+l2_inst_mr*(l2_inst_avg_lat/ticks_per_cycle)
    # CPI_{data} constributes to base CPI
    tl1_d=l1_hit_cycles+l1d_mr*tl2_d
    # CPI_{instr} formula ommits the base latency 
    # due to cache line prefetching.
    tl1_i=l1i_mr*tl2_i
    # Return CPI_{base}+CPI_{instr}+CPI_{data}
    return 1+tl1_d+tl1_i


def fine_tune_runs():


    for benchmark in benchmarks:
# Get simulation results for each search
        results_folder=base_folder+"/"+benchmark
        l1d_results=getCsvFromResults(results_folder+"/results_l1d.txt")
        l1i_results=getCsvFromResults(results_folder+"/results_l1i.txt")
        l2_results=getCsvFromResults(results_folder+"/results_l2.txt")
# Each simulation holds the results that count
        l1d_mrs=l1d_results[:,1]
        l1i_mrs=l1i_results[:,2]
# For l2 its Inst_mr,Inst_lat,Data_mr,Data_lat
        l2_stats=l2_results[:,[5,7,4,6]]

# Find optimal
        cost_opt=np.inf
        config_opt=()
        for l1d_idx,l1d_mr in enumerate(l1d_mrs):
            for l1i_idx,l1i_mr in enumerate(l1i_mrs):
                for l2_idx,l2_stat in enumerate(l2_stats):
                    l2_inst_mr=l2_stat[0]
                    l2_inst_avg_lat=l2_stat[1]
                    l2_data_mr=l2_stat[2]
                    l2_data_avg_lat=l2_stat[3]
                    cost=CostfromStats(l1d_mr,l1i_mr,
                                    l2_inst_mr,l2_inst_avg_lat,
                                    l2_data_mr,l2_data_avg_lat) 
                    if cost < cost_opt:
                        cost_opt=cost
                        config_opt=(l1d_idx,l1i_idx,l2_idx)
        print(f"For benchmark: {benchmark}\tCPI_opt: {cost_opt}\tOptimal config: {config_opt}")

            

fine_tune_runs()
def getBestCPI():
    fine_tuned_foler="/home/chris/Documents/programms/aca/part3/tuned_runs/401/"

    for benchmark in benchmarks:
        for root, dirs, files in os.walk(path):













