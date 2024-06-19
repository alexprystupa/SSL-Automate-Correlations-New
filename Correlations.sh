#!/usr/bin/bash
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=Aleksandr.Prystupa@nyulangone.org
#SBATCH --partition=cpu_short
#SBATCH --time=4:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=80G
#SBATCH --job-name=Custom_Correlations
#SBATCH --output=Custom_Correlations_%A_%a.out
#SBATCH --error=Custom_Correlations_%A_%a.err

unset PYTHONPATH
module load condaenvs/gpu/pathgan_SSL37

#python3 models/custom_correlations/main.py \
#--meta_folder Julia_As_Training_Clustering \
#--meta_field $1 \
#--matching_field samples \
#--folds_pickle /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/utilities/fold_creation/julia-as-training-all-folds-V2/$1_folds.pkl \
#--h5_complete_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_Julia_External_Cohort_20X_he_complete_small_bio_and_resections_all_labels.h5 \
#--h5_additional_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_TCGA_External_Cohort_40X_he_complete_all_labels.h5 \
#--fold_number $2

python3 models/custom_correlations/main.py \
--meta_folder Julia_As_Training_Clustering_lung_lymph_node \
--meta_field $1 \
--matching_field samples \
--folds_pickle /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/utilities/fold_creation/julia-as-training-all-folds-V3/lung_lymph_node/$1_folds.pkl \
--h5_complete_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_Julia_External_Cohort_20X_he_complete_labels_Matija_detail_small_bio_and_resections_lung_lymph_node_all_labels.h5 \
--h5_additional_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_TCGA_External_Cohort_40X_he_complete_all_labels.h5 \
--fold_number $2
