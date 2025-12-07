#!/usr/bin/bash
rm benchmark_results_per_iter.dat benchmark_results_num_sims.dat

python comparing_impls_per_iter.py
python comparing_impls_per_num_sims.py 
