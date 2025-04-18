# Recovery Score Calculations: Derivativet helper
# Script created  11/7/2024
# Last revision 12/13/2024

import numpy as np

from numpy.typing import NDArray
from typing import Tuple

def calculate_derivatives(df) -> Tuple:
    '''Converts pandas DataFrame to a NumPy array and then calculates the first (jerk) and second derivatives (snap) of the acceleration data

    Args:
    df (pd.DataFrame): DataFrame with acceleration (Acc_Z) and TimeStamp values
        
    Returns:
        Tuple[NDArray[np.float64], NDArray[np.float64]]: A tuple containing the jerk and snap arrays
    '''
    # Converts to a numpy array for derivative calculations
    acc_z_np, time_stamp_np = convert_to_np(df)
    print('Data converted to numpy array successfully')
    
    # Calculates time differences
    dt: NDArray[np.float64] = np.diff(time_stamp_np)  
    
    # Handles potential division by zero in dt
    if np.any(dt <= 0):
        raise ValueError('Timestamps must be strictly increasing')
    
    # Calculates first derivative (jerk)
    jerk: NDArray[np.float64] = np.diff(acc_z_np) / dt
    
    # Calculates second derivative (snap)
    snap: NDArray[np.float64] = np.diff(jerk) / dt[1:]  # Corrected to use dt[1:] to match the length
    
    #print(f'jerk length is {len(jerk)}')
    #print(f'snap length is {len(snap)}')
    
    # Checks lengths of arrays
    if len(jerk) != (len(snap) + 1):
        raise ValueError('The "jerk" and "snap" arrays must have the correct lengths')
    
    if len(jerk) == 0:
        return np.array([], dtype=np.float64), np.array([], dtype=np.float64)  # Return empty arrays if input is empty

    return jerk, snap

def convert_to_np(df_avg) -> Tuple:
    '''Converts pandas DataFrame to a tuple of NumPy arrays
    
    Args:
        df_avg (pd.DataFrame): DataFrame with acceleration (Acc_Z)) and TimeStamp values
    Returns:
        Tuple[NDArray[np.float64], NDArray[np.float64]]: Tuple of numpy arrays with acceleration and timestamp values
    '''
    # Converts Acc_Z and time_stamp to numpy arrays
    acc_z_np: NDArray = np.array(df_avg['Acc_Z'], dtype=np.float64)
    time_stamp_np: NDArray = np.array(df_avg['timeStamp'], dtype=np.float64)
          
    return acc_z_np, time_stamp_np

