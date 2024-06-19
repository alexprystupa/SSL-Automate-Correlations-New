#!/bin/bash

files=(./utilities/fold_creation/julia-as-training-all-folds-V3/lung_lymph_node/*.pkl)

for filename in "${files[@]}"
do
	v=$(echo $filename | cut -d "f" -f 3 | cut -d "/" -f 3)
	#echo ${v::-1}
	#echo $v
	sbatch Correlations.sh ${v::-1} 1
done

