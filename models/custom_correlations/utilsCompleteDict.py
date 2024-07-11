# utilsCompleteDict.py

import sys
main_path = '/gpfs/data/naiklab/Alex/AI_Histopathology/Lung-Mutations/Histomorphological-Phenotype-Learning/'
sys.path.append(main_path)
from models.clustering.logistic_regression_leiden_clusters import *
from models.evaluation.folds import load_existing_split
from models.clustering.correlations import *
from models.clustering.data_processing import *
from models.clustering.leiden_representations import include_tile_connections_frame
from data_manipulation.utils import store_data

def get_list_resolutions(adatas_path):
    
    """
    @param adatas_path[str]:
    
    @return[list[str]]: sorted list of resolutions ex. ["leiden_0.5", "leiden_1.0" ...] 
    """
    
    resolutions = [float(file.split("_")[-3].replace("p", ".")) for file in os.listdir(adatas_path) if file.endswith("fold0.csv")]
    group_by_list = [f"leiden_{res}" for res in resolutions]
    
    return sorted(list(set(group_by_list)))


def get_raw_complete_df(meta_folder, meta_field, matching_field, group_by_res, folds_pickle, h5_complete_path, h5_additional_path, fold_number, external_cohort=False):

    """
    @param meta_folder:
    @param meta_field:
    @param matching_field:
    @param group_by_res:
    @param folds_pickle:
    @param h5_complete_path:
    @param: h5_additional_path
    @param: fold_number
    @param: external_cohort  

    @return: 
    """

    complete_df, additional_df, _, _, _ = build_cohort_representations(meta_folder, meta_field, matching_field, group_by_res, 
                                      fold_number, folds_pickle, h5_complete_path, h5_additional_path, 'clr', 100)
    
    if external_cohort:
        return additional_df
    
    return complete_df


def clean_complete_df(complete_df, meta_field):
    
    """
    @param complete_df[pd.Dataframe]:
    @param meta_field[str]:

    @return[pd.DataFrame]: Data frame of clusters and their composition (filtered if value had -1)
    """
    
    # 1. Reset Index
    complete_df = complete_df.reset_index(drop=True)
    
    # 2. Set Column as strings
    complete_df.columns = complete_df.columns.astype(str)
        
    # 3. Make Columns Separate for Complete Response vs Residual Disease, set 1 as positive predictor
    complete_df = complete_df[complete_df[meta_field] != -1] # Remove any rows with -1 (not present)
        
    complete_df = complete_df.rename(columns={f"{meta_field}":f"{meta_field}_pos"})
    
    complete_df[f"{meta_field}_neg"] = complete_df[f"{meta_field}_pos"]
    
    complete_df[f"{meta_field}_neg"] = np.where(complete_df[f"{meta_field}_pos"] == 0, 1, 0)
    
    complete_df[f"{meta_field}_neg"].iloc[0] = "nan"

    return complete_df


def get_complete_df(meta_folder, meta_field, matching_field, group_by_res, folds_pickle, h5_complete_path, h5_additional_path, fold_number, external_cohort=False):

    """
    @param meta_folder:
    @param meta_field:
    @param matching_field:
    @param group_by_res:
    @param folds_pickle:
    @param h5_complete_path:
    @param: h5_additional_path
    @param: fold_number
    @param: external_cohort  

    @return: 
    """
    
    # 1. Get Raw Complete Data Frame
    raw_complete_df = get_raw_complete_df(meta_folder, meta_field, matching_field, group_by_res, folds_pickle, h5_complete_path, h5_additional_path, fold_number, external_cohort)

    # 2. Clean Complete Data Frame
    return clean_complete_df(complete_df=raw_complete_df, meta_field=meta_field)


def get_complete_df_dict(meta_folder, matching_field, meta_field, folds_pickle, h5_complete_path, h5_additional_path, fold_number, list_of_resolutions, external_cohort):
    
    """
    @param meta_folder[str]:
    @param matching_field[str]:
    @param meta_field[str]:
    @param folds_pickle[str]:
    @param h5_complete_path[str]:
    @param h5_additional_path[str]:
    @param fold_number[int]:
    @parma list_of_resolutions[list[str]]:
    
    @return: 
    """

    complete_df_dict = {leiden_res:get_complete_df(meta_folder, meta_field, matching_field, leiden_res, folds_pickle, h5_complete_path, h5_additional_path, fold_number, external_cohort) for leiden_res in list_of_resolutions}

    return complete_df_dict

def filter_complete_df(df):
    df = df.loc[:, ~(df == "0.0").any()]
    
    return df.tail(-1)

def get_filtered_dict(complete_df_dict, list_of_resolutions):

    """
    @param complete_df_dict[dict[pd.DataFrame]]:
    @param list_of_resolutions[list[str]]:
    
    @return[dict[pd.DataFrame]]: filtered data frame dictionary
    """

    return {leiden_res:filter_complete_df(complete_df_dict[leiden_res]) for leiden_res in list_of_resolutions}
