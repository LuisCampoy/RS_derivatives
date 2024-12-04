# Recovery Score Calculations: Derivativet helper
# Script created  11/7/2024
# Last revision 12/1/2024

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from typing import Tuple

def convert_to_np(acc_z: pd.Series, time_stamp: pd.Series) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    '''Converts two pandas Series to NumPy arrays
    
    Args:
        acc_z (pd.Series): Series of accelerations on Z axis values
        time_stamp (pd.Series): Series of timestamp values

    Returns:
        Tuple[NDArray[np.float64], NDArray[np.float64]]: Tuple of numpy arrays with acceleration and timestamp values
    '''
    # Convert acc_z and time_stamp to numpy arrays
    acc_z_np = np.array(acc_z, dtype=np.float64)
    time_stamp_np = np.array(time_stamp, dtype=np.float64)
          
    return acc_z_np, time_stamp_np

def calculate_derivatives(acc_z_np: NDArray[np.float64], timeStamp_np: NDArray[np.float64]) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    '''Calculates the first derivative (jerk) and second derivative (snap) of the acceleration data.

    Args:
        acc_z_np (NDArray[np.float64]): Array of acceleration values
        time_stamp_np (NDArray[np.float64]): Array of timestamps

    Returns:
        Tuple[NDArray[np.float64], NDArray[np.float64]]: A tuple containing the jerk and snap arrays.
    '''
    dt: NDArray[np.float64] = np.diff(timeStamp_np)  # Calculate time differences
    
    # Handle potential division by zero in dt
    if np.any(dt <= 0):
        raise ValueError('Timestamps must be strictly increasing.')
    
    # Calculate first derivative (jerk)
    jerk: NDArray[np.float64] = np.diff(acc_z_np) / dt
    
    # Calculate second derivative (snap)
    snap: NDArray[np.float64] = np.diff(jerk) / dt[1:]  # Corrected to use dt[1:] to match the length
    
    print(f'jerk length is {len(jerk)}')
    print(f'snap length is {len(snap)}')
    
    # Check lengths of arrays
    if len(jerk) != (len(snap) + 1):
        raise ValueError("The 'jerk' and 'snap' arrays must have the correct lengths.")
    
    return jerk, snap
   
