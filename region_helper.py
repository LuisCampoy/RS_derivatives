# Recovery Score Calculations: Calculation helper
# Script created  3/25/2024
# Last revision 12/1/2024

def get_number_roi_sd(filtered_df, regions_of_interest_sd, window_size, step_size)-> list:
    '''Provides number of regions_of_interest. DataFrames with the selected regions of interest
    
    Args:
        filtered_df: pd.DataFrame provided
        regions_of_interest_sd: list of tuples with the start and the end of each of the regions that have a standad deviation > set threshold
        window_size (int): size of each window
        step_size (int):step_size for the window
        
    Returns:
        Tuple: Containing a list of DataFrames, each DataFrame contains a specific region of interest, 
               and three lists with maximum absolute values of AccX, AccY, and AccZ for each region.
               Selected_Data_list is a list with a dataframe with AccX, AccY and AccZ per event
    '''
    # Store data from each reion of interest
    selected_data_list: list = [] 
    
    # Loop through each region of interest (ROI)
    for i, roi in enumerate(regions_of_interest_sd):
        start_index:int = roi[0] * step_size
        end_index = start_index + window_size
        
        # Ensure the end index does not exceed the dataframe length
        if end_index > len(filtered_df):
            end_index: int = len(filtered_df)
            
        # Select rows using iloc and columns using column names
        selected_data = filtered_df.iloc[start_index:end_index][['Acc_X', 'Acc_Y', 'Acc_Z']]
    
        selected_data_list.append(selected_data)
           
    return selected_data_list

