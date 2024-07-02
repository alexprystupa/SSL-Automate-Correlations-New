# SSL Histopathology Automate Correlations
## Description
Scripts designed to run correlations based on SSL Histomorphological Phenotype Learning workflow. 
Correlations are adapted from Step 10 of SSL HPL workflow at https://github.com/AdalbertoCq/Histomorphological-Phenotype-Learning/blob/master/README_HPL.md.
The workflow is designed to correlate any meta data column of your choosing across all clusters, across all resolutions that were ran when clustering results.
This is accomplished using the Correlations.sh script. Addtionally, correlations across all meta data columns can be automated using the Correlations-All-Meta-Column.sh script.

## Usage
### 1. Correlations.sh
#### Step Inputs:
#### Step Outputs:
#### Usage:
#### Command Example:
#### Scripts:

### 2. Correlations-All-Meta-Columns.sh
#### Step Inputs:
#### Step Outputs:
#### Command Example:
        python3 models/custom_correlations/main.py \
--meta_folder Julia_As_Training_Clustering_lung_lymph_node \
--meta_field $1 \
--matching_field samples \
--folds_pickle /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/utilities/fold_creation/julia-as-training-all-folds-V3/lung_lymph_node/$1_folds.pkl \
--h5_complete_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_Julia_External_Cohort_20X_he_complete_labels_Matija_detail_small_bio_and_resections_lung_lymph_node_all_labels.h5 \
--h5_additional_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_TCGA_External_Cohort_40X_he_complete_all_labels.h5 \
--fold_number $2

## Directory Structure
## H5 File Content Specification
