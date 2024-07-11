# main.py
import argparse
import pandas as pd
import numpy as np
import pickle
#import math
#import glob
#import h5py
import sys
import os
from sklearn import metrics

main_path = '/gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/'
sys.path.append(main_path)

from models.custom_correlations.utilsCompleteDict import get_complete_df_dict
from models.custom_correlations.utilsCompleteDict import get_filtered_dict
from models.custom_correlations.utilsCompleteDict import get_list_resolutions
from models.custom_correlations.utilsResultsDict import get_clr_dict
from models.custom_correlations.utilsResultsDict import get_results_clusters_dict
from models.custom_correlations.utilsResultsDict import get_significant_clusters_df


def arg_parser():

    parser = argparse.ArgumentParser(description='Custom Correlations for every single meta data column across all resolutions.')

    parser.add_argument('--meta_folder', type=str)
    parser.add_argument('--matching_field', type=str)
    parser.add_argument('--meta_field', type=str)
    parser.add_argument('--folds_pickle', type=str)
    parser.add_argument('--h5_complete_path', type=str)
    parser.add_argument('--h5_additional_path', type=str)
    parser.add_argument('--fold_number', type=int, default=0)
    parser.add_argument('--sig_p', type=float, default=0.1)
    parser.add_argument('--sig_auc', type=float, default=0.6)

    return parser.parse_args()

def run_cluster_correlations(meta_folder, matching_field, meta_field, folds_pickle, h5_complete_path, h5_additional_path, fold_number, list_of_resolutions, adatas_path, sig_p, sig_auc, external_cohort):
    
    """
    @param:
    @param:
    @param:
    @param:

    @return:
    """

    # 1. Get Complete DF Dict
    complete_df_dict = get_complete_df_dict(meta_folder, matching_field, meta_field, folds_pickle, h5_complete_path, h5_additional_path, fold_number, list_of_resolutions, external_cohort)

    # 2. Get Filtered DF Dict
    filtered_complete_df_dict = get_filtered_dict(complete_df_dict=complete_df_dict, list_of_resolutions=list_of_resolutions)

    # 3. Get CLR Dict
    clr_dict = get_clr_dict(filtered_complete_df_dict=filtered_complete_df_dict, list_of_resolutions=list_of_resolutions)

    # 4. Get Results Dict
    results_dict_pos = get_results_clusters_dict(clr_dict=clr_dict, filtered_complete_df_dict=filtered_complete_df_dict, meta_field=meta_field, corr_type="pos", list_of_resolutions=list_of_resolutions)
    results_dict_neg = get_results_clusters_dict(clr_dict=clr_dict, filtered_complete_df_dict=filtered_complete_df_dict, meta_field=meta_field, corr_type="neg", list_of_resolutions=list_of_resolutions)

    # 5. Get Significant Clusters
    sig_results_df_pos = get_significant_clusters_df(results_dict=results_dict_pos, adatas_path=adatas_path, matching_field=matching_field, fold_number=fold_number, 
                                               fold=folds_pickle, h5_complete_path=h5_complete_path, h5_additional_path=h5_additional_path, sig_p=sig_p, sig_auc=sig_auc)
    
    sig_results_df_neg = get_significant_clusters_df(results_dict=results_dict_neg, adatas_path=adatas_path, matching_field=matching_field, fold_number=fold_number, 
                                               fold=folds_pickle, h5_complete_path=h5_complete_path, h5_additional_path=h5_additional_path, sig_p=sig_p, sig_auc=sig_auc)
    
    return sig_results_df_pos, sig_results_df_neg


def main():
    print("Start")
    args = arg_parser()

    meta_folder = args.meta_folder
    meta_field = args.meta_field
    matching_field = args.matching_field
    folds_pickle = args.folds_pickle
    h5_complete_path = args.h5_complete_path
    h5_additional_path = args.h5_additional_path
    fold_number = args.fold_number
    sig_p = args.sig_p
    sig_auc = args.sig_auc

    # 1. Get Paths
    main_cluster_path = os.path.join(h5_complete_path.split('hdf5_')[0], meta_folder)
    adatas_path       = os.path.join(main_cluster_path, 'adatas')

    # 2. Get List of Resolutions 
    list_of_resolutions = get_list_resolutions(adatas_path)

    # 3. Run Cluster Correlations on Data and External Cohort
    sig_results_pos_main_cohort, sig_results_neg_main_cohort = run_cluster_correlations(meta_folder, matching_field, meta_field, folds_pickle, h5_complete_path, h5_additional_path, fold_number, list_of_resolutions, adatas_path, sig_p, sig_auc, external_cohort=False)
    sig_results_pos_ext_cohort, sig_results_neg_ext_cohort = run_cluster_correlations(meta_folder, matching_field, meta_field, folds_pickle, h5_complete_path, h5_additional_path, fold_number, list_of_resolutions, adatas_path, sig_p, sig_auc, external_cohort=True)
    
    # 4. Save Results
    save_path = f"{main_cluster_path}/custom_correlations_output/{meta_field}"

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    sig_results_pos_main_cohort.to_csv(f"{save_path}/significant_positively_correlated_clusters_main_cohort.csv")
    sig_results_neg_main_cohort.to_csv(f"{save_path}/significant_negatively_correlated_clusters_main_cohort.csv")
    sig_results_pos_ext_cohort.to_csv(f"{save_path}/significant_positively_correlated_clusters_external_cohort.csv")
    sig_results_neg_ext_cohort.to_csv(f"{save_path}/significant_negatively_correlated_clusters_external_cohort.csv")


if __name__ == "__main__":

    # Test params
    ## meta_folder = Julia_External_Cohort_20X
    ## meta_field = EGFR
    ## matching_field = samples
    ## folds_pickle = /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/utilities/fold_creation/julia-as-training-all-folds-V2/EGFR_folds.pkl
    ## h5_complete_path = /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_Julia_External_Cohort_20X_he_complete_small_bio_and_resections_all_labels.h5
    ## h5_addtional_path = /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_TCGA_External_Cohort_40X_he_complete_all_labels.h5
    ## fold_number = 1
    ## sig_p = 0.1
    ## sig_auc = 0.6

    # python main.py --meta_folder Julia_As_Training_Clustering --meta_field EGFR --matching_field samples --folds_pickle /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/utilities/fold_creation/julia-as-training-all-folds-V2/EGFR_folds.pkl --h5_complete_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_Julia_External_Cohort_20X_he_complete_small_bio_and_resections_all_labels.h5 --h5_additional_path /gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/results/BarlowTwins_3/Julia_External_Cohort_20X/h224_w224_n3_zdim128/hdf5_TCGA_External_Cohort_40X_he_complete_all_labels.h5 --fold_number 1

    main()
