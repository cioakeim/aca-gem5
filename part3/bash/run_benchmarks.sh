#!/bin/bash

# This script is used to configure and run all 5 requested benchmarks 
# based on a specific configuration. The results are stored in the file
# correspoding to each run.
# Usage: ./run_benchmarks.sh [config] [store_subfolder]


config=$1
store_subfolder=$2

# Repo folder
repo_folder="/home/chris/Documents/programs/aca/aca-gem5"
# Location of benchmark binaries and data
benchmarks_base_folder="$repo_folder/spec_cpu2006"
folder401="$benchmarks_base_folder/401.bzip2"
folder429="$benchmarks_base_folder/429.mcf"
folder456="$benchmarks_base_folder/456.hmmer"
folder458="$benchmarks_base_folder/458.sjeng"
folder470="$benchmarks_base_folder/470.lbm"
# Location of results storage
res_folder="$repo_folder/part3/search_run/$store_subfolder"
# Location of gem5 in system
gem5_dir="/home/chris/Documents/repos/gem5"

cd "$gem5_dir"
pwd

./build/ARM/gem5.opt -d "$res_folder/401/clk_$cpu_clock/mem_$ddr_mem" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=1GHz \
  --caches --l2cache \
  $config \
  -c $folder401/src/specbzip -o \
  "$folder401/data/input.program 10" -I 100000000


./build/ARM/gem5.opt -d "$res_folder/429/clk_$cpu_clock" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=1GHz \
  --caches --l2cache \
  $config \
  -c $folder429/src/specmcf -o \
  "$folder429/data/inp.in" -I 100000000


./build/ARM/gem5.opt -d "$res_folder/456/clk_$cpu_clock" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=1GHz \
  --caches --l2cache \
  $config \
  -c $folder456/src/spechmmer -o \
  "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 $folder456/data/bombesin.hmm" \
  -I 100000000


./build/ARM/gem5.opt -d "$res_folder/458/clk_$cpu_clock" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=1GHz \
  --caches --l2cache \
  $config \
  -c $folder458/src/specsjeng -o \
  "$folder458/data/test.txt" -I 100000000


./build/ARM/gem5.opt -d "$res_folder/470/clk_$cpu_clock" configs/deprecated/example/se.py --cpu-type=MinorCPU \
  --cpu-clock=1GHz \
  --caches --l2cache \
  $config \
  -c $folder470/src/speclibm -o \
  "20 $folder470/data/lbm.in 0 1 $folder470/data/100_100_130_cf_a.of" -I 100000000
