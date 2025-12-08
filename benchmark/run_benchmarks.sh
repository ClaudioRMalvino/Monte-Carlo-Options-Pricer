#!/usr/bin/bash
cd data
rm benchmark_results_per_iter.dat benchmark_results_num_paths.dat
cd ..

python comparing_impls_per_iter.py
python comparing_impls_per_num_sims.py 
