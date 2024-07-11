# utilsResultsDict.py

import sys
import pandas as pd
import numpy as np
import math
import glob
import h5py
import os
from sklearn import metrics

main_path = '/gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/'
sys.path.append(main_path)

from models.clustering.logistic_regression_leiden_clusters import *
from models.evaluation.folds import load_existing_split
from models.clustering.correlations import *
from models.clustering.data_processing import *
from models.clustering.leiden_representations import include_tile_connections_frame
from data_manipulation.utils import store_data

def get_clr_vals(filtered_complete_df):
    
    """
    @param filtered_complete_df[dict[pd.DataFrame]]: Output of get_filtered_complete_df_dict (iterate over keys)
    
    @return[dict[pd.DataFrame]]: CLR values data frame dictionary
    """
        
    return [filtered_complete_df[col].to_list() for col in filtered_complete_df.columns if col.isdigit()]


def get_clr_dict(filtered_complete_df_dict, list_of_resolutions):

    """
    @param filtered_complete_df[dict[pd.DataFrame]]: Output of get_filtered_complete_df_dict (iterate over keys)
    @param list_of_resolutions[list[str]]:
    
    @return[dict[pd.DataFrame]]: filtered data frame dictionary
    """

    return {leiden_res:get_clr_vals(filtered_complete_df_dict[leiden_res]) for leiden_res in list_of_resolutions}


def get_results_dict(clr_list, complete_df, meta_field, corr_type):

    """
    @param clr_list[list]: clr_dict[leiden_res]
    @param complete_df: filtered_complete_df_dict[leiden_res]
    @param response_type[str]: "pos" or "neg"

    @return:
    """
    
    results_dict = {}

    response_type = f"{meta_field}_{corr_type}"
    
    for i, clr_vals in enumerate(clr_list):
    
        # 1. Get Correlation & p-value
        corr, p_val = pearsonr(clr_vals, complete_df[response_type].to_list())

        # 2. Get ROC Stats
        clr_arr = np.array(clr_vals)
        response_arr = np.array(complete_df[response_type].to_list())
        fpr, tpr, _ = metrics.roc_curve(response_arr, clr_arr, pos_label=1)

        # 3. Get AUC Score
        auc = metrics.auc(fpr, tpr)

        # 4. Save In Results Dict
        results_dict[f"Cluster_{i}"] = {"corr": corr, "p_val": p_val, "auc": auc}
        
    return results_dict


def get_results_clusters_dict(clr_dict, filtered_complete_df_dict, meta_field, corr_type, list_of_resolutions):
    
    """
    @param clr_dict:
    @param filtered_complete_df_dict:
    @param list_of_resolutions:

    @return[dict[dict]]: 
    """

    return {leiden_res:get_results_dict(clr_dict[leiden_res], filtered_complete_df_dict[leiden_res], meta_field=meta_field, corr_type=corr_type) for leiden_res in list_of_resolutions}


def find_num_samples_in_cluster(leiden_res, cluster_num, adatas_path, matching_field, fold_number, fold, h5_complete_path, h5_additional_path):

    """
    @param leiden_res[str]: Leiden Resolution
    @param cluster_num[str]: ex. "leiden_0.25"
    @param adatas_path:
    @param matching_field:
    @param fold_number:
    @param fold:
    @param h5_complete_path:
    @param h5_additional_path:

    @return:
    """

    folds = load_existing_split(fold)

    final_fold = folds[fold_number]
    
    _, df, _ = read_csvs(adatas_path, matching_field, leiden_res, 
          fold_number, final_fold, h5_complete_path, h5_additional_path, 
          additional_as_fold=False, force_fold=None)
    
    return len(set(df[df[leiden_res] == cluster_num]["samples"]))


def get_significant_clusters_df(results_dict, adatas_path, matching_field, fold_number, fold, h5_complete_path, h5_additional_path, sig_p=0.1, sig_auc=0.6):

    """
    @param results_dict:
    @param sig_p:
    @param sig_auc:
    @param adatas_path:
    @param matching_field:
    @param fold_number:
    @param fold:
    @param h5_complete_path:
    @param h5_additional_path:

    @return:
    """
    results_list = []

    for key in results_dict.keys():
        for next_key in results_dict[key].keys():
            if results_dict[key][next_key]['p_val'] < sig_p and results_dict[key][next_key]['auc'] > sig_auc:

                leiden_res = key
                cluster_num = next_key
                corr_val = results_dict[key][next_key]['corr']
                p_val = results_dict[key][next_key]['p_val']
                auc_score = results_dict[key][next_key]['auc']
                patients_in_cluster = find_num_samples_in_cluster(leiden_res, int(cluster_num.split("_")[1]), adatas_path, matching_field, fold_number, fold, h5_complete_path, h5_additional_path)

                results_list.append([leiden_res, cluster_num, corr_val, p_val, auc_score, patients_in_cluster])

    return pd.DataFrame(results_list, columns=['leiden_res', 'cluster_num', 
                                                                 'corr_val', 'p_val', 'auc_score', 'patients_in_cluster'])

