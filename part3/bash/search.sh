#./run_benchmarks.sh "--l1d_size=32kB --l1i_size=64kB --l2_size=512kB --l1i_assoc=1 --l1d_assoc=1 --l2_assoc=2 --cacheline_size=64" test


l1_size_list=("128kB" "64kB" "32kB" "16kB")
l1d_ass_list=("4" "8" "16")
l1i_ass_list=("2" "4" "8")

l2_size_list=("2MB" "1MB" "512kB" "256kB")
l2_ass_list=("4" "8" "16")

cache_line_list=("32" "64" "128")


l1d_cnt="0"
l1i_cnt="0"
l2_cnt="0"
# L1 opt
for i in "${!l1_size_list[@]}"; do
  for cache_line in "${cache_line_list[@]}"; do
    l1d_size="${l1_size_list[$i]}"
    l1i_size="${l1_size_list[$i]}"
    l2_size="${l2_size_list[$i]}"
    echo $l1d_size $l1i_size $l2_size
    # Default values for this loop
    l1d_ass="4"
    l1i_ass="2"
    l2_ass="4"
    # Data cache
    for l1d_ass in "${l1d_ass_list[@]}"; do 
      store_path="l1d_$l1d_cnt"
      l1d_cnt=$(($l1d_cnt+1))
      config="--l1d_size=$l1d_size \
        --l1i_size=$l1i_size \
        --l2_size=$l2_size \
        --l1i_assoc=$l1i_ass \
        --l1d_assoc=$l1d_ass \
        --l2_assoc=$l2_ass \
        --cacheline_size=$cache_line"
      ./run_benchmarks.sh "$config" "$store_path" &
    done
    # Instr cache
    for l1i_ass in "${l1i_ass_list[@]}"; do 
      store_path="l1i_$l1i_cnt"
      l1i_cnt=$(($l1i_cnt+1))
      config="--l1d_size=$l1d_size \
        --l1i_size=$l1i_size \
        --l2_size=$l2_size \
        --l1i_assoc=$l1i_ass \
        --l1d_assoc=$l1d_ass \
        --l2_assoc=$l2_ass \
        --cacheline_size=$cache_line"
      ./run_benchmarks.sh "$config" "$store_path" &
    done
    # L2 cache
    for l2_ass in "${l2_ass_list[@]}"; do 
      store_path="l2_$l2_cnt"
      l2_cnt=$(($l2_cnt+1))
      config="--l1d_size=$l1d_size \
        --l1i_size=$l1i_size \
        --l2_size=$l2_size \
        --l1i_assoc=$l1i_ass \
        --l1d_assoc=$l1d_ass \
        --l2_assoc=$l2_ass \
        --cacheline_size=$cache_line"
      ./run_benchmarks.sh "$config" "$store_path" &
    done
    wait
  done
done

