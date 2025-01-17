#!/bin/bash

# This script is used to do all the runs of part 2 of the GEM5 project.
# Usage of the script ./run_benchmarks.sh [cpu-clock] [ddr_mem] runs through all
# possible combinations

clocks=("1GHz" "3GHz" "1GHz")
mems=("DDR3_1600_8x8" "DDR3_1600_8x8" "DDR3_2133_8x8")

for i in "${!clocks[@]}"; do
  clk="${clocks[$i]}"
  mem="${mems[$i]}"
  echo $i $clk $mem
  ./run_benchmarks.sh $clk $mem

done

