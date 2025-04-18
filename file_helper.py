# Recovery Score Calculations: file_helper Script
# Script created  3/25/2024
# Last revision 12/13/2024

import pandas as pd
import numpy as np

def read_csv_file(file_path) -> pd.DataFrame:
    '''Adds .csv extension and the reads the first four columns (timeStamp, Acc_X, Acc_Y, Acc_Z) from the csv file
        using the read_csv function.
        skips the first row (Sep = ,)
        Uses the second row as header
        only reads the first 4 columns to speed up file reading time

    Args:
        file_path: case number (file_name) entered by user

    Returns:
        Pandas DataFrame
    '''

    file_path_csv: str  = add_csv_extension(file_path)

    try:
        print('reading csv file...')

        df: pd.DataFrame = pd.read_csv(
            file_path_csv,
            skiprows = 3, # skip the first 3 rows (separator, headers, units)
            sep = ',',
            header = None, # No header in the remaining rows
            names = ['timeStamp', 'Acc_X', 'Acc_Y', 'Acc_Z'],
            usecols = [0, 1, 2, 3],
            dtype = {'timeStamp': str, 'Acc_X': float, 'Acc_Y': float, 'Acc_Z': float},
            encoding ='utf-8',
            low_memory = False,
        )
        
        # Convert 'TimeStamp' column to datetime format
        df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    
        return df

    except Exception as e:

        print('An error occurred:', str(e))
        
        return pd.DataFrame()
    
def add_csv_extension(file_path: str) -> str:
    '''adds '.csv' to the file number

    Args:
        file_path (str): Case Number

    Returns:
        str: the Case Number (entered) plus the csv extension (.csv)
    '''

    file_path_csv: str = file_path + '.csv'

    return file_path_csv
 
def initial_filter(df, target_value) -> pd.DataFrame:
    '''Filters initial csv file and creates a new df ignoring initial acceleration values.
       Looks into AccZ column (Z axis). Filters out initial values until it finds
       the first acceleration value on the Z axis that is greater than the 'target value'
       Signals when horse gains sternal recumbency for the first time.
        
    Args:
        df (pd.DataFrame): first four columns of the initial csv file with formated timeStamp in column 0

    Returns:
        Pandas DataFrame: A new filtered DataFrame starting from when 'AccZ' exceeds the target value
    '''
    
    try:
   
        # Finds the index of the first occurrence of the target value in column 'Acc_Z'
        start_index: int = df[df['Acc_Z'] > target_value].index[0]
        
        # Create the new DataFrame starting from that index
        filtered_df = df.iloc[start_index:].reset_index(drop = True)
        
        return filtered_df
    
    except IndexError:
        # If the target value is not found, return the same dataFrame
        print(f'No values in "Acc_Z" greater than {target_value} could be found. Returning the original DataFrame')

        return df
    
def clean_data(df, target_value) -> pd.DataFrame:
    '''Cleans the Acc_Z column in a DataFrame by setting values lower than the threshold to NaN.
    
     Args:
        df (pandas.DataFrame): The input DataFrame that contains an 'Acc_Z' column.
        target_value (float): The threshold below which values are considered invalid.
    
    Returns:
    pandas.DataFrame: The cleaned DataFrame with values below the threshold set to NaN.
    '''
    # Ensure the AccZ column exists
    if 'Acc_Z' in df.columns:
        df['Acc_Z'] = df['Acc_Z'].apply(lambda x: x if x >= target_value else np.nan)

    else:
        raise KeyError('The "Acc_Z" column is not present in the DataFrame.')
    
    return df   
 
def apply_moving_average(df_filtered, target_moving_avg) -> pd.DataFrame:
    '''Applies a moving average filter to the acceleration data (Acc_X, Acc_Y, Acc_Z) in the DataFrame.

    Args:
        df_filtered (pd.DataFrame): DataFrame containing the raw acceleration data.
        target_moving_avg (int): The window size for the moving average filter.

    Returns:
        pd.DataFrame: DataFrame with the filtered acceleration data.
    '''
    df_moving_avg = df_filtered.copy()
    
    df_moving_avg['Acc_X'] = df_filtered['Acc_X'].rolling(window = target_moving_avg, min_periods=1).mean()
    df_moving_avg['Acc_Y'] = df_filtered['Acc_Y'].rolling(window = target_moving_avg, min_periods=1).mean()
    df_moving_avg['Acc_Z'] = df_filtered['Acc_Z'].rolling(window = target_moving_avg, min_periods=1).mean()
    
    return df_moving_avg

def apply_kalman_filter(df: pd.DataFrame, process_variance: float, measurement_variance: float, estimated_measurement_variance: float) -> pd.DataFrame:
    '''Applies a Kalman filter to the Acc_X, Acc_Y, and Acc_Z columns of the input DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing Acc_X, Acc_Y, and Acc_Z columns.
        process_variance (float): The process variance (Q).
        measurement_variance (float): The measurement variance (R).
        estimated_measurement_variance (float): The estimated measurement variance (P).

    Returns:
        pd.DataFrame: The DataFrame with Kalman filtered Acc_X, Acc_Y, and Acc_Z columns.
    '''
    def kalman_filter(data):
        n = len(data)
        xhat = np.zeros(n)       # a posteri estimate of x
        P = np.zeros(n)          # a posteri error estimate
        xhatminus = np.zeros(n)  # a priori estimate of x
        Pminus = np.zeros(n)     # a priori error estimate
        K = np.zeros(n)          # gain or blending factor

        # initial guesses
        xhat[0] = data[0]
        P[0] = estimated_measurement_variance

        for k in range(1, n):
            # time update
            xhatminus[k] = xhat[k-1]
            Pminus[k] = P[k-1] + process_variance

            # measurement update
            K[k] = Pminus[k] / (Pminus[k] + measurement_variance)
            xhat[k] = xhatminus[k] + K[k] * (data[k] - xhatminus[k])
            P[k] = (1 - K[k]) * Pminus[k]

        return xhat

    df_filtered = df.copy()
    df_filtered['Acc_X'] = kalman_filter(df['Acc_X'].values)
    df_filtered['Acc_Y'] = kalman_filter(df['Acc_Y'].values)
    df_filtered['Acc_Z'] = kalman_filter(df['Acc_Z'].values)

    return df_filtered