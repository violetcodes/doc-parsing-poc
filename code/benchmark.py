import pandas as pd
import numpy as np


def get_recall_for_column(df, column_name):
    target = df[col_name+'_target'].values
    predicted = df[col_name+'_predicted'].values
    found = (target == predicted).sum()
    count = np.count_nonzero(target)
    return found/count

def get_precision_for_column(df, column_name):
    target = df[col_name+'_target'].values
    predicted = df[col_name+'_predicted'].values
    found = (predicted == target).sum()
    count = np.count_nonzero(predicted)
    return found/count
    
    
    

def evaluate_results(target_csv, predicted_csv):
    # join two csvs on file names
    columns = target_csv.columns
    print(columns)
    
    combined_csv = target_csv.join(predicted_csv, on='File Name', lsuffix='_target', rsuffix='_predicted')
    
    # recall for each columns 
    precision, recall = [], []
    for col in columns:
        recall.append(get_recall_for_column(combined_csv, col))
        precision.append(get_recall_for_column(combined_csv, col))
        
    result = pd.DataFrame([columns, precision, recall], colname=['columns name', 'precision', 'recall'])
        
        
    