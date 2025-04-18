# RS: Main Script
# Script created 3/25/2024
# Last revision 4/9/2025
# Notes: Use derivative method to detect the peaks in either jerk or snap 
#        and then go 0.5sec before and after to characterize regions of interest. 
#        Use those indexes on the original Acc_Z, Acc_X, Acc_Y dataset

import pandas as pd
import numpy as np

from acceleration_helper import get_max_accelerations_x, get_max_accelerations_y, get_max_accelerations_z, get_sa_2axes, get_sumua
from attempt_detection_helper import get_roi_derivative,  get_attempts, set_jerk_threshold, set_snap_threshold, detect_regions
from derivative_helper import calculate_derivatives
from file_helper import read_csv_file, initial_filter, apply_moving_average, clean_data, apply_kalman_filter
from graph_helper import plot_acceleration_data, get_plot_jerk_snap
from numpy.typing import NDArray
from region_helper import extract_roi_values
from output_results_helper import process_recovery
#from velocity_helper import get_auc_x, get_auc_y, get_auc_z

def main() -> None:

    # acceleration threshold value to signal sternal recumbency for initial filter
    target_value: float = 9.0 
    
    # variables for moving average filter
    target_moving_avg: int = 10 # moving average window_size (4)
    
    # variables for Kalman filter
    process_variance = 1e-4  # Q
    measurement_variance = 1e-2  # R
    estimated_measurement_variance = 0.5  # P   
    
    # variables for ROI_Derivative method
    factor: float = 30.0  # Factor to set jerk threshold (56.55)
    percentile: float = 99.0    # Percentile to set jerk threshold  
    jerk_threshold: float = 1.0-5 #1.578626493498403e-08 #5.7209199129367875e-12  Threshold for significant jerk
    snap_threshold: float = 1  # Threshold for significant snap
    sampling_rate: int = 200  # Sampling rate of the accelerometer200
       
    file_path: str = input('Enter case number: ')
        
    df: pd.DataFrame = read_csv_file(file_path)

    if df is not None:
        print('File read successfully...')
        print('Columns in DataFrame: ', df.columns)
        
    else:
        print('Failed to load DataFrame')
        return # exit if the file cannot be loaded
    
    # Creates new df in which Z_axis values are ignored until values reach 'target_value' 
    # signaling horse getting onto sternal recumbency
    df_filtered: pd.DataFrame = initial_filter(df, target_value)
    print('Initial filter applied successfully')
       
    # Apply moving average filter with a specified 'target_moving_avg' value
    df_moving_avg: pd.DataFrame = apply_moving_average(df_filtered, target_moving_avg)
    print('Moving average applied successfully')
    
    df_kalman: pd.DataFrame = apply_kalman_filter(df_filtered, process_variance, measurement_variance, estimated_measurement_variance)
    print('Kalman filter applied successfully')
    
    # Plot data to review application of filters
    #plot_acceleration_data(df_filtered, df_moving_avg, df_kalman)
          
    # Creates new DataFrame after applying avg filter with Acc_Z and timeStamp values only 
    df_avg = pd.DataFrame({'timeStamp': df_moving_avg['timeStamp'], 'Acc_Z': df_moving_avg['Acc_Z']})
        
    # Creates new DataFrame with Acc_Z and timeStamp values only (Kalman filter applied)
    kalman_df = pd.DataFrame({'Acc_Z': df_kalman['Acc_Z'], 'timeStamp': df_kalman['timeStamp']})   
        
    # Calculates first and second derivatives (jerk and snap) from the avg filtered dataset
    jerk, snap = calculate_derivatives(kalman_df)
    print('Jerk and Snap calculated successfully')

    # Plot jerk and snap
    #get_plot_jerk_snap(jerk, snap, regions_indexes, df_avg)
       
    # Set Jerk threshold and calculate mean Jerk to be able to re calibrate the threshold
    mean_jerk, std_jerk, jerk_threshold_cal = set_jerk_threshold(jerk, factor, percentile)
    print('Jerk threshold calculated successfully')
    
    # Set Snap threshold and calculate mean Snap to be able to re calibrate the threshold
    mean_snap, std_snap, snap_threshold_cal = set_snap_threshold(snap, factor, percentile)
    print('Snap threshold calculated successfully')
    
    # Detect regions in the jerk and snap signals
    regions_indexes: list[float] = detect_regions(jerk, snap, jerk_threshold_cal, snap_threshold_cal, sampling_rate)
    print('Regions calculated successfully')
         
    # Get regions of interest for Jerk and Snap
    #roi_indices_df: list[float] = get_roi_derivative(jerk, snap, jerk_threshold_cal, snap_threshold)
    
    # Get indices of regions of interest for Jerk and Snap  
    #roi_indices_df: pd.DataFrame = get_roi_indices(jerk, snap, jerk_threshold_cal, snap_threshold)
    #print('ROI indices obtained successfully')
    #print(f'ROI indices {roi_indices_df}')
        
    # Plot jerk and snap with flagged spikes
    get_plot_jerk_snap(jerk, snap, regions_indexes, df_avg)

    # Plot jerk and snap with regions of interest using sd method
    #get_plot_sd_with_roi(jerk, df_avg, roi_sd, window_size, step_size, file_path)
            
    number_failed_attempts: int = get_attempts(regions_indexes)
    print('Number of Failed Attempts calculated successfully')
    
    # Extract ROI values for each axis
    
    roi_values_df: pd.DataFrame = extract_roi_values(df_filtered, regions_indexes)
    print('ROI values extracted successfully')
    #print(roi_values_df)
    #print(f'ROI_Values_length = {len(roi_values_df)}')
    
    # Ensure consistent use of roi_values_df as a DataFrame
    amax_x_list: list[float] = get_max_accelerations_x(roi_values_df)
    amax_y_list: list[float] = get_max_accelerations_y(roi_values_df)
    amax_z_list: list[float] = get_max_accelerations_z(roi_values_df)
                
    sa_2axes: float = get_sa_2axes(amax_x_list, amax_y_list)
    #print(f'sa_2axes = {sa_2axes}')
                
    sumua:float = get_sumua(amax_x_list, amax_y_list, amax_z_list)
    #print(f'ua_list = {ua_list}')
    #print(f'sumua = {sumua}')
            
    rs_2axes_py: float = process_recovery(file_path, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, snap_threshold_cal, number_failed_attempts, sa_2axes, sumua)

    # display output_results in terminal
    print(f'results are:')
    print(f'file name: {file_path}')
    print(f'jerk_threshold: {jerk_threshold}')
    print(f'mean_jerk: {mean_jerk}')
    print(f'std_jerk:{std_jerk}')
    print(f'jerk_threshold_cal: {jerk_threshold_cal}')
    print(f'snap_threshold_cal: {snap_threshold_cal}')
    print(f'Number of failed attempts: {number_failed_attempts}')
    print(f'sa_2axes= {sa_2axes}')
    print(f'sumua= {sumua}')
    print(f'rs_2axes_py= {rs_2axes_py}')
 
if __name__ == "__main__":
    
    main()