# Recovery Score Calculations: Graph_Helper Script
# Script created  3/25/2024
# Last revision 12/13/2024

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

from numpy.typing import NDArray

def plot_acceleration_data(df_filtered: pd.DataFrame, df_moving_avg: pd.DataFrame, df_kalman: pd.DataFrame) -> None:
    '''Plots three graphs for df_filtered, df_moving_avg, and df_kalman.

    Args:
        df_filtered (pd.DataFrame): DataFrame with filtered acceleration data.
        df_moving_avg (pd.DataFrame): DataFrame with moving average filtered acceleration data.
        df_kalman (pd.DataFrame): DataFrame with Kalman filtered acceleration data.
    '''
    plt.figure(figsize=(15, 10))

    # Plot df_filtered
    plt.subplot(3, 1, 1)
    plt.plot(df_filtered['timeStamp'], df_filtered['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df_filtered['timeStamp'], df_filtered['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df_filtered['timeStamp'], df_filtered['Acc_Z'], label='Acc_Z', color='red')
    plt.title('Filtered Acceleration Data')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    # Plot df_moving_avg
    plt.subplot(3, 1, 2)
    plt.plot(df_moving_avg['timeStamp'], df_moving_avg['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df_moving_avg['timeStamp'], df_moving_avg['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df_moving_avg['timeStamp'], df_moving_avg['Acc_Z'], label='Acc_Z', color='red')
    plt.title('Moving Average Filtered Acceleration Data')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    # Plot df_kalman
    plt.subplot(3, 1, 3)
    plt.plot(df_kalman['timeStamp'], df_kalman['Acc_X'], label='Acc_X', color='blue')
    plt.plot(df_kalman['timeStamp'], df_kalman['Acc_Y'], label='Acc_Y', color='green')
    plt.plot(df_kalman['timeStamp'], df_kalman['Acc_Z'], label='Acc_Z', color='red')
    plt.title('Kalman Filtered Acceleration Data')
    plt.xlabel('Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def get_plot_jerk_snap(jerk: np.ndarray, snap: np.ndarray, regions_indexes: list, df_avg: pd.DataFrame) -> None:
    '''Plots jerk and snap

    Args:
        jerk (np.ndarray): The first derivative of acceleration (jerk)
        snap (np.ndarray): The second derivative of acceleration (snap)
        regions_indexes: list: Indices of regions of interest
        df_avg: provides TimeStamp list for the X axis
    '''
    time_stamp = df_avg['timeStamp']
    
    # Adjust timeStamp to match the length of jerk and snap
    timeStamp_jerk = time_stamp[:-1]
    timeStamp_snap = time_stamp[:-2]
    
    # Plot size
    plt.figure(figsize=(12, 6))
    
    # Jerk plot
    plt.subplot(2, 1, 1)
    plt.plot(timeStamp_jerk, jerk, label='Jerk', color='blue')
    
    # Convert timestamps to numerical values
    #timeStamp_jerk_num = mdates.date2num(timeStamp_jerk)
    
    # Highlight ROIs
    #for i in regions_indexes:
    #   plt.axvspan(regions_indexes[i] - 0.5, regions_indexes[i] + 0.5, color='grey', alpha=0.3, label='ROI' if i == regions_indexes[0] else '')
        
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title('Jerk')
    plt.xlabel('TimeStamp')
    plt.ylabel('Jerk')
    plt.legend()
    plt.grid(True)

    # Snap plot
    plt.subplot(2, 1, 2)
    plt.plot(timeStamp_snap, snap, label='Snap', color='blue')
    #plt.scatter(timeStamp_snap[roi_indices], snap[roi_indices], color="red", label="ROI", zorder=5)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title('Snap')
    plt.xlabel('Time')
    plt.ylabel('Snap')
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()

def get_plot_jerk_snap_with_roi(jerk: np.ndarray, snap: np.ndarray, regions_indexes: list, df: pd.DataFrame) -> None:
    '''Plots jerk and snap, highlighting regions of interest (ROIs).

    Args:
        jerk (np.ndarray): The first derivative of acceleration (jerk).
        snap (np.ndarray): The second derivative of acceleration (snap).
        regions_indexes: list: Indices of regions of interest.
        df_avd: pd.DataFrame: Time array corresponding to jerk and snap.
    '''
    time_stamp_np: NDArray = np.array(df['timeStamp'], dtype=np.float64)
     # Adjust timeStamp to match the length of jerk and snap
    timeStamp_jerk = time_stamp_np[:-1]
    timeStamp_snap = time_stamp_np[:-2]
    
    # Plot jerk
    plt.figure(figsize=(12, 6))
    
    # Jerk plot
    plt.subplot(2, 1, 1)
    plt.plot(timeStamp_jerk, jerk, label="Jerk", color="blue")
    plt.scatter(timeStamp_jerk[regions_indexes], jerk, color="red", label="ROI", zorder=5)
    
    # Convert timestamps to numerical values
    #timeStamp_jerk_num = mdates.date2num(timeStamp_jerk)
    # Highlight ROIs
    #for i in roi_indices['ROI_Indices']:
    #   plt.axvspan(float(timeStamp_jerk_num[i] - 0.5), float(timeStamp_jerk_num[i] + 0.5), color='grey', alpha=0.3, label="ROI" if i == roi_indices[0] else "")
        
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Jerk with Highlighted ROIs")
    plt.xlabel("Time")
    plt.ylabel("Jerk")
    plt.legend()
    plt.grid(True)

    # Snap plot
    plt.subplot(2, 1, 2)
    plt.plot(timeStamp_snap, snap, label="Snap", color="blue")
    #plt.scatter(timeStamp_snap[roi_indices], snap[roi_indices], color="red", label="ROI", zorder=5)
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Snap with Highlighted ROIs")
    plt.xlabel("Time")
    plt.ylabel("Snap")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()

def get_plot_sd_with_roi(jerk:np.ndarray, df_avg:pd.DataFrame, roi_sd:list, window_size:int, step_size:int, file_path:str) -> None:
    '''Creates a plot of the Z axis only with the detected Regions of Interest
    
    Args:
        jerk: np.ndarray with the jerk values
        df_avg: pd.DataFrame with the timeStamp and Acc_Z values
        roi_sd: list with the regions of interest detected
        window_size: int with the size of the window
        step_size: int with the step size
        file_path: string with the name of the file

    Returns:
        None
    '''
    time_stamp_np: NDArray = np.array(df_avg['timeStamp'])
    # Adjust timeStamp to match the length of jerk and snap
    timeStamp_jerk = time_stamp_np[:-1]
    #timeStamp_snap = time_stamp_np[:-2]

    plt.figure(figsize=(10, 6))
    
    plt.plot(timeStamp_jerk, jerk, label="Jerk", color="blue")
    
    for k in range(len(roi_sd)):
        plt.vlines(
            timeStamp_jerk[roi_sd[k][0] * step_size],
            -1e-06,
            1e-06,
            colors= 'r',
            linestyles= 'dashed',
            label= 'ROI',
        )

        plt.vlines(
            df_avg['timeStamp'][roi_sd[k][0] * step_size + window_size],
            -1e-06,
            1e-06,
            colors=  'r',
            linestyles= 'dashed',
        )
    plt.xlabel('timeStamp')
    plt.ylabel('jerk')
    plt.title(file_path)
    plt.grid(which='both')
    plt.legend()
    plt.show()

