# Recovery Score Calculations: Calculation helper
# Script created  3/25/2024
# Last revision 4/9/2025

import pandas as pd

def extract_roi_values(df: pd.DataFrame, roi_indices: list) -> pd.DataFrame:
    '''Extracts the values within each region of interest (ROI) for each specified axis from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        roi_indices (list): List containing the indices of regions of interest.
       
    Returns:
        pd.DataFrame: DataFrame containing the values within each ROI for each axis.
    '''
    
    axes: list[str] = ['Acc_Z', 'Acc_X', 'Acc_Y'] # List of axis names to extract values for
    roi_values: dict = {axis: [] for axis in axes}
    roi_values['ROI_Index'] = []

    for index in roi_indices:
        for axis in axes:
            roi_values[axis].append(df[axis].iloc[index])
        roi_values['ROI_Index'].append(index)

    return pd.DataFrame(roi_values)

