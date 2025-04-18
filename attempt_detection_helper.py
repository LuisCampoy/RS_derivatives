# Recovery Score Calculations: Identification of Regions of Interest helper
# Script created  3/25/2024
# Last revision 12/24/2024

import numpy as np
import pandas as pd
from numpy.typing import NDArray

def set_jerk_threshold(jerk: NDArray[np.float64], factor: float, percentile: float) -> tuple:
    '''Sets the jerk threshold based on the mean and standard deviation of the jerk values

    Args:
    jerk (NDArray[np.float64]): Array of jerk values
    factor (float): Multiplication factor for the standard deviation
    percentile (int): Percentile value to use for setting the threshold

    Returns:
        tuple: The calculated jerk threshold
    '''
    mean_jerk = np.mean(jerk)
    std_jerk = np.std(jerk)
    percentile_jerk = np.percentile(jerk, percentile)
    jerk_threshold_cal = max(mean_jerk + factor * std_jerk, percentile_jerk)
   
    return mean_jerk, std_jerk, jerk_threshold_cal

def set_snap_threshold(snap: NDArray[np.float64], factor: float, percentile: float) -> tuple:
    '''Sets the snap threshold based on the mean and standard deviation of the snap values

    Args:
    snap (NDArray[np.float64]): Array of snap values
    factor (float): Multiplication factor for the standard deviation
    percentile (int): Percentile value to use for setting the threshold

    Returns:
        tuple: The calculated snap threshold
    '''
    mean_snap = np.mean(snap)
    std_snap = np.std(snap)
    percentile_snap = np.percentile(snap, percentile)
    snap_threshold_cal = max(mean_snap + factor * std_snap, percentile_snap)
    
    return mean_snap, std_snap, snap_threshold_cal

def detect_regions(jerk: NDArray[np.float64], snap: NDArray[np.float64], jerk_threshold: float, snap_threshold: float, sampling_rate: int) -> list[int]:
    '''Detects spikes in jerk and snap signals and returns a list of indices 0.5 seconds before and after the max value of each spike.

    Args:
        jerk (NDArray[np.float64]): Array of jerk values
        snap (NDArray[np.float64]): Array of snap values
        jerk_threshold (float): Threshold for jerk values
        snap_threshold (float): Threshold for snap values
        sampling_rate (float): Sampling rate of the signals in Hz

    Returns:
        list[int]: List of indices 0.5 seconds before and after the max value of each spike
    '''
    # Ensure both arrays have the same length
    min_length = min(len(jerk), len(snap))
    jerk = jerk[:min_length]
    snap = snap[:min_length]

    # Detect spikes where either jerk or snap exceed thresholds
    spike_mask = (np.abs(jerk) > jerk_threshold) | (np.abs(snap) > snap_threshold)
    spike_indices = np.where(spike_mask)[0]  # Get indices of true values in the mask

    # Initialize list to store indices of interest
    roi_indices = []

    # Define the window size in terms of number of samples (0.5 seconds before and after)
    window_size = int(0.5 * sampling_rate)

    # Iterate through detected spikes
    for idx in spike_indices:
        # Get the window around the spike
        start_idx = max(0, idx - window_size)
        end_idx = min(len(jerk), idx + window_size + 1)

        # Find the max value within the window
        max_idx = np.argmax(np.abs(jerk[start_idx:end_idx]) + np.abs(snap[start_idx:end_idx])) + start_idx

        # Get indices 0.5 seconds before and after the max value
        roi_start_idx = max(0, max_idx - window_size)
        roi_end_idx = min(len(jerk), max_idx + window_size + 1)

        # Append the indices to the list
        roi_indices.extend(range(roi_start_idx, roi_end_idx))

    # Remove duplicates and sort the indices
    roi_indices = sorted(set(roi_indices))

    return roi_indices

def get_attempts(regions_indexes) -> int:
    ''' Counts the number of identified regions of interest. Since the last region will always be
        the successful attempt, it substracts 1 to the final count

    Args:
        roi_indices: list with the all the regions that have a jerk > set threshold

    Returns:
        int with Number of failed Attempts
    '''

    number_failed_attempts: int = len(regions_indexes) - 1

    return number_failed_attempts


def get_roi_derivative(jerk, snap, jerk_threshold_cal, snap_threshold) -> list:
    ''' Identifies Regions of Interest in the data based on a threshold criterion 
        applied to the Jerk and Snap values
        It filters out regions where the Jerk and Snap are greater than or equal to the threshold value.
        These regions are stored in the filtered list along with their indexes.

    Args:
        jerk: list with the all the regions that have a jerk greater or equal to the threshold
        snap: list with the all the regions that have a snap greater or equal to the threshold
        jerk_threshold_cal: threshold value for Jerk after re calibration
        snap_threshold: threshold value for Snap
        
    Returns:
        list with the regions of interest for Jerk and Snap
    '''
    filtered = list()
    for i in range(len(jerk)):
        if jerk[i] > jerk_threshold_cal:
            filtered.append((i, jerk[i]))
    
    for i in range(len(snap)):
        if snap[i] > snap_threshold:
            filtered.append((i, snap[i]))

    roi_derivative = list() #
    big = 0
    index = 0
    for j in range(len(filtered) - 1):
        if filtered[j][0] + 1 == filtered[j + 1][0]:
            if filtered[j][1] > big:
                big = filtered[j][1]
                index = filtered[j][0]
            elif filtered[j + 1][1] > big:
                big = filtered[j + 1][1]
                index = filtered[j + 1][0]
        elif big > 0:
            roi_derivative.append((index, big))
            big = 0
            index = 0
        
    roi_derivative.append((index, big))
    
    return roi_derivative
