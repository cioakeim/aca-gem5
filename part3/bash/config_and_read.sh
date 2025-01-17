#!/bin/bash

# This script is used to display the results of each simulation 
# for independant exploration
# Usage: ./config_and_read.sh [target_cache] [target_benchmark]

# Check if there are no arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <target_cache> <target_benchmark>"
    exit 1
fi

target_cache="$1"
target_benchmark="$2"
results_base="../results/search_run"
start="0"
end="23"


mkdir -p configs
conf_file=configs/conf_"$target_cache"_"$target_benchmark".ini
echo $conf_file
echo "" > $conf_file
echo "[Benchmarks]" >> $conf_file

for i in $(seq $start $end); do
  read_path="$results_base"/"$target_cache"_"$i"/"$target_benchmark"
  echo "$read_path" >> $conf_file
done

echo "" >> $conf_file
echo "[Parameters]" >> $conf_file
echo -e "\
system.cpu.cpi
system.cpu.dcache.overallMissRate::total
system.cpu.icache.overallMissRate::total
system.l2.overallMissRate::total
system.l2.overallMissRate::cpu.data
system.l2.overallMissRate::cpu.inst
system.l2.overallAvgMissLatency::cpu.data
system.l2.overallAvgMissLatency::cpu.inst
system.cpu.dcache.overallAvgMissLatency::total
system.cpu.icache.overallAvgMissLatency::total
" >> $conf_file

echo "[Output]" >> $conf_file

store_folder=../extracted/"$target_benchmark"
mkdir -p extracted/$target_benchmark
echo $store_folder
res_file=$store_folder/results_"$target_cache".txt
echo $res_file >> $conf_file


./read_results.sh $conf_file
