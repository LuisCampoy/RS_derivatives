# Recovery Score Calculations: Graph_Helper Script
# Script created  3/25/2024
# Last revision 12/3/2024

from types import NoneType
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

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

def get_plot_sd_with_roi(df, regions_of_interest_sd, window_size, step_size, file_path) -> None:
    '''Creates a plot of the Z axis only with the detected Regions of Interest
    
    Args:
        df: list with the all the regions that have a standad deviation greater or equal to our threshold
        regions_of_interest_sd: list with the regions of interest detected
        window_size:
        step_size: 
        file_path: string with the name of the file

    Returns:
        None
    '''
    
    plt.figure(figsize=(10, 6))
    plt.plot(
    df['timeStamp'][0:],
    df['Acc_X'][0:],
    label= "Acc_X",
    )
    plt.plot(
    df['timeStamp'][0:],
    df['Acc_Y'][0:],
    label= 'Acc_Y',
    )
    plt.plot(
    df['timeStamp'][0:],
    df['Acc_Z'][0:],
    label= 'Acc_Z',
    )

    for k in range(len(regions_of_interest_sd)):
        plt.vlines(
            df['timeStamp'][regions_of_interest_sd[k][0] * step_size],
            -30,
            30,
            colors= ['r'],
            linestyles= 'dashed',
            label= 'ROI',
        )

        plt.vlines(
            df['timeStamp'][regions_of_interest_sd[k][0] * step_size + window_size],
            -30,
            30,
            colors= ['r'],
            linestyles= 'dashed',
        )
    plt.xlabel('timeStamp')
    plt.ylabel('Accelerations (m/s^2)')
    plt.title(file_path)
    plt.grid(which='both')
    plt.legend()
    plt.show()

def get_plot_jerk_snap_with_roi(jerk: np.ndarray, snap: np.ndarray, roi_indices: np.ndarray, timeStamp_avg_np) -> None:
    '''Plots jerk and snap, highlighting regions of interest (ROIs).

    Args:
        jerk (np.ndarray): The first derivative of acceleration (jerk).
        snap (np.ndarray): The second derivative of acceleration (snap).
        roi_indices (np.ndarray): Indices of regions of interest.
        timeStamp (np.ndarray): Time array corresponding to jerk and snap.
    '''
    # Adjust timeStamp to match the length of jerk and snap
    timeStamp_jerk = timeStamp_avg_np[:-1]
    timeStamp_snap = timeStamp_avg_np[:-2]
    
    # Plot jerk
    plt.figure(figsize=(12, 6))
    
    # Jerk plot
    plt.subplot(2, 1, 1)
    plt.plot(timeStamp_jerk, jerk, label="Jerk", color="blue")
    plt.scatter(timeStamp_jerk[roi_indices], jerk[roi_indices], color="red", label="ROI", zorder=5)
    
    # Convert timestamps to numerical values
    #timeStamp_jerk_num = mdates.date2num(timeStamp_jerk)

    #for i in roi_indices:
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
    plt.scatter(timeStamp_snap[roi_indices], snap[roi_indices], color="red", label="ROI", zorder=5)
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Snap with Highlighted ROIs")
    plt.xlabel("Time")
    plt.ylabel("Snap")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()
