#!/bin/bash

# Script for extracting all of the results from the initial simulations

for cache in "l1d" "l1i" "l2"; do
  for benchmark in "401" "429" "456" "458" "470"; do
    ./config_and_read.sh "$cache" "$benchmark"
  done
done
