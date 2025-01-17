#!/bin/bash

# This script is used to configure and run all 5 requested benchmarks 
# based on a specific configuration. The results are stored in the file
# correspoding to each run.
# Usage: ./run_benchmarks.sh [cpu-clock] [ddr_mem]

cpu_clock="$1"
ddr_mem="$2"



# Location of gem5 in system
gem5_dir="/home/chris/Documents/repos/gem5"
# The directory of the repo
repo_dir="/home/chris/Documents/programms/aca/aca-gem5"
# Location of results storage
res_folder="$base_dir/part2/results"
# Location of benchmark binaries and data
benchmarks_base_folder="$repo_dir/spec_cpu2006"
folder401="$benchmarks_base_folder/401.bzip2"
folder429="$benchmarks_base_folder/429.mcf"
folder456="$benchmarks_base_folder/456.hmmer"
folder458="$benchmarks_base_folder/458.sjeng"
folder470="$benchmarks_base_folder/470.lbm"

cd "$gem5_dir"
pwd

./build/ARM/gem5.opt -d "$res_folder/clk_$cpu_clock/mem_$ddr_mem/401" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=$cpu_clock \
  --caches --l2cache -c $folder401/src/specbzip -o \
  "$folder401/data/input.program 10" -I 100000000 &


./build/ARM/gem5.opt -d "$res_folder/clk_$cpu_clock/mem_$ddr_mem/429" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=$cpu_clock \
  --caches --l2cache -c $folder429/src/specmcf -o \
  "$folder429/data/inp.in" -I 100000000 &


./build/ARM/gem5.opt -d "$res_folder/clk_$cpu_clock/mem_$ddr_mem/456" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=$cpu_clock \
  --caches --l2cache -c $folder456/src/spechmmer -o \
  "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 $folder456/data/bombesin.hmm" \
  -I 100000000 &


./build/ARM/gem5.opt -d "$res_folder/clk_$cpu_clock/mem_$ddr_mem/458" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=$cpu_clock \
  --caches --l2cache -c $folder458/src/specsjeng -o \
  "$folder458/data/test.txt" -I 100000000 &


./build/ARM/gem5.opt -d "$res_folder/clk_$cpu_clock/mem_$ddr_mem/470" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=$cpu_clock \
  --caches --l2cache -c $folder470/src/speclibm -o \
  "20 $folder470/data/lbm.in 0 1 $folder470/data/100_100_130_cf_a.of" -I 100000000 &

wait
