# RS: Main Script
# Script created 3/25/2024
# Last revision 12/3/2024
# Notes: needs CSV_helper re done to add new data
#        needs to create class with decorator to calculate the max acceleration with the different datasets (different filters)

# Importing libraries
import pandas as pd

from datetime import datetime
from derivative_helper import convert_to_np, calculate_derivatives
from acceleration_helper import get_max_accelerations_x, get_max_accelerations_y, get_max_accelerations_z, get_sa_2axes, get_sumua
from attempt_detection_helper import calculate_window_sd, detect_roi_sd, get_roi_derivative, get_roi_indices, get_attempts_sd, get_attempts_jerk, get_attempts_snap
from file_helper import read_csv_file, add_csv_extension, initial_filter, apply_moving_average, clean_data, apply_kalman_filter
from graph_helper import plot_acceleration_data, get_plot_sd_with_roi, get_plot_jerk_snap_with_roi
from region_helper import get_number_roi_sd
from output_results_helper import process_recovery
#from velocity_helper import get_auc_x, get_auc_y, get_auc_z

def main() -> None:
   
    start_time: str = datetime.now().strftime('%Y-%m-%d_%H.%M')
    
    # variables for ROI_SD method
    # values that can be changed  to increase/ decrease sensitivity
    window_size: int = 10000 # each cell is 5ms 10000 cells represent 2secs
    step_size: int = 2000 # 2000 cells are 400ms (0.4secs)
    target_value: float = 9.0 # acceleration value
    threshold: float = 1.5 # default value for SD threshold
    
    # variables for moving average filter
    target_moving_avg: int = 4 # moving average window_size
    
    # variables for Kalman filter
    process_variance = 1e-5  # Q
    measurement_variance = 1e-1  # R
    estimated_measurement_variance = 1.0  # P   
    
    # variables for ROI_Derivative method
    jerk_threshold: float = 4e-6  # Define threshold for significant jerk
    snap_threshold: float = 4e-13  # Define threshold for significant snap
    
    file_path: str = input('Enter file name: ')
    file_path_csv: str = add_csv_extension(file_path)
    
    df: pd.DataFrame = read_csv_file(file_path_csv)

    if df is not None:
        print('File read successfully...')
        print("Columns in DataFrame:", df.columns)
        
    else:
        print('Failed to load DataFrame')
        return # exit if the file cannot be loaded
    
    # Creates new df in which Z values are ignored until Z values reach target_value 
    # corresponding with horse getting onto sternal recumbency
    df_filtered: pd.DataFrame = initial_filter(df, target_value)
    print('Initial filter applied successfully')
       
    # Apply moving average filter with a specified target_value
    df_moving_avg: pd.DataFrame = apply_moving_average(df_filtered, target_moving_avg)
    print('Moving average applied successfully')
    
    df_kalman: pd.DataFrame = apply_kalman_filter(df_filtered, process_variance, measurement_variance, estimated_measurement_variance)
    print('Kalman filter applied successfully')
    
    # Plot data to review application of filters
    plot_acceleration_data(df_filtered, df_moving_avg, df_kalman)

    while True:
               
        # Calculates standard deviation for each window using Acc_Z column only
        AccZ_sd: list[float] = calculate_window_sd(df_filtered['Acc_Z'][1:], window_size, step_size)
        print('sd_list calculated succesfully')
        #print(f'Accz_sd is {AccZ_sd}')
        
        # Creates new DataFrame with TimeStamp values only
        #timeStamp: pd.Series = df_filtered["TimeStamp"][1:]
        #print('TimeStamp extracted successfully')
        
        # Detects regions of interest based on standard deviation method
        roi_sd: list[float] = detect_roi_sd(AccZ_sd, threshold)   
        print('Regions of Interest (SD method) detected successfully')
        #print(f'Regions of interest {roi_sd}')
        
        # Plot standard deviation with regions of interest                
        get_plot_sd_with_roi(df_filtered, roi_sd, window_size, step_size, file_path)
        
        # I can do it as a DataFrame at once        
        # Creates new DataFrame with AccZ values only (moving average filter applied)
        #Acc_Z_avg: pd.Series = df_moving_avg['AccZ'][1:]
        
        # Creates new DataFrame with TimeStamp values only (moving average)
        #timeStamp_avg: pd.Series = df_moving_avg["TimeStamp"][1:]
        
        # Creates new DataFrame with Acc_Z and timeStamp values only (moving average filter applied)
        df_avg = pd.DataFrame({'Acc_Z': df_moving_avg['Acc_Z'], 'timeStamp': df_moving_avg['timeStamp']})
        
        # Creates new DataFrame with Acc_Z and timeStamp values only (Kalman filter applied)
        df_kalman = pd.DataFrame({'Acc_Z': df_kalman['Acc_Z'], 'timeStamp': df_kalman['timeStamp']})
        
        # Converts to numpy array for next derivative calculations
        Acc_Z_avg_np, timeStamp_avg_np = convert_to_np(df_avg['Acc_Z'], df_avg['timeStamp'])
        print('Data converted to numpy array successfully')
        
        # Calculates Jerk and Snap (first and second derivatives) from avg filtered data
        jerk, snap = calculate_derivatives(Acc_Z_avg_np, timeStamp_avg_np)
        print('Jerk and Snap calculated successfully')
              
        # Converts onto pandas DataFrame
        #jerkdf = pd.DataFrame({'TimeStamp':timeStamp_np,'Jerk':jerk})
        #print('Jerk DataFrame created successfully')
        #snapdf = pd.DataFrame(snap, columns=['TimeStamp','Jerk'])
        #print('Snap DataFrame created successfully')
        
        # Get regions of interest for Jerk and Snap
        roi_derivative: list[float] = get_roi_derivative(jerk, snap, jerk_threshold, snap_threshold)
        print('ROI (Derivative method) calculated successfully')
        #print(f'ROI Derivative {roi_derivative}')
    
        # Get indices of regions of interest for Jerk and Snap  
        roi_indices_derivative = get_roi_indices(jerk, snap, jerk_threshold, snap_threshold)
        print('ROI indices (derivative method) obtained successfully')
        #print(f'ROI indices {roi_indices_derivative}')
        
        # Plot jerk and snap with regions of interest
        get_plot_jerk_snap_with_roi(jerk, snap, roi_indices_derivative, timeStamp_avg_np)
        
        redo: str = input('continue or re calculate with different threshold? (C/R) ').lower()

        if redo == 'c':
                
            # Process and calculate data based on initial default parameters for threshold
            number_of_failed_attempts_sd: int = get_attempts_sd(roi_sd)
            print(f'Number of Failed Attempts_sd = {number_of_failed_attempts_sd}')
            
            number_of_failed_attempts_jerk: int = get_attempts_jerk(roi_indices_derivative)
            print(f'Number of Failed Attempts_jerk = {number_of_failed_attempts_jerk}')
            
            number_of_failed_attempts_snap: int = get_attempts_snap(roi_indices_derivative)
            print(f'Number of Failed Attempts_snap = {number_of_failed_attempts_snap}')
            
            selected_data_list_sd_method:list = get_number_roi_sd(df_filtered, roi_sd, window_size, step_size)
            #print(selected_data)
            #print('Data printed successfully')
            #print(selected_data_list)
            #print('Selected Data list')
            
            #selected_data_list_jerk_method: list = get_regions_jerk(jerk, roi_indices)
            #selected_data_list_snap_method: list = get_regions_snap(snap, roi_indices)
                            
            amax_x_list: list[float] = get_max_accelerations_x(selected_data_list_sd_method)
            #print(f'amax_x_list is {amax_x_list}')
                    
            amax_y_list: list[float] = get_max_accelerations_y(selected_data_list_sd_method)
            #print(f'amax_y_list is {amax_y_list}')
                
            amax_z_list: list[float] = get_max_accelerations_z(selected_data_list_sd_method)
            #print(f'amax_z_list is {amax_z_list}')
                
            #sa: float = get_sa(amax_x_list, amax_y_list, amax_z_list)
            #print(f'sa = {sa}')

            sa_2axes: float = get_sa_2axes(amax_x_list, amax_y_list)
            #print(f'sa_2axes = {sa_2axes}')
                
            sumua:float = get_sumua(amax_x_list, amax_y_list, amax_z_list)
            #print(f'ua_list = {ua_list}')
            #print(f'sumua = {sumua}')
                
            '''
            velocity_x = get_auc_x(time_readings, acceleration_readings, index)
            velocity_y = get_auc_y
            velocity_z = get_auc_z
            '''  
            rs_2axes_py: float = process_recovery(file_path, number_of_failed_attempts_sd, sa_2axes, sumua)

            # output_results: pd.DataFrame = get_output_results(file_path, number_of_failed_attempts, sa_2axes, sumua)
            print(f'results are')
            print(f'file name: {file_path}')
            print(f'Number of failed attempts: {number_of_failed_attempts_sd}')
            print(f'sa_2axes= {sa_2axes}')
            print(f'sumua= {sumua}')
            print(f'rs_2axes_py= {rs_2axes_py}')
    
            break # exit loop after processing results

        elif redo == 'r':
         # Set a new value for Threshold
            try:
                recalibrate_threshold_str: str = input('Enter new threshold ')
                recalibrate_threshold: float = float(recalibrate_threshold_str)
                threshold: float = recalibrate_threshold
                print(f'Threshold recalibrated to {threshold}')

            except ValueError:
                print('invalid entry. Enter a float value')
        
        else:
            print('invalid option. Enter either "c" to continue or "r" to recalculate')

if __name__ == "__main__":
    
    main()