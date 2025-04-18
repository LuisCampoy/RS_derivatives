# Recovery Score Calculations: output_results_helper Script
# Script created  5/30/2024
# Last revision 12/13/2024

from recovery_score_helper import get_rs_ua, get_rs_sa
from CSV_helper import add_sa, add_ua

def process_recovery(file_path: str, jerk_threshold: float, mean_jerk: float, std_jerk: float, jerk_threshold_cal: float, threshold: float, number_failed_attempts: int, sa_2axes: float, sumua: float) -> float:
    '''Processes recovery scores depending whether it is one or more attempts and
    Logs them to a CSV file.

    Args:
    file_path (str): The file path to the CSV file.
    jerk_threshold (float): The jerk threshold value from the fuction used to calibrate.
    mean_jerk (float): The mean jerk value.
    std_jerk (float): The standard deviation of the jerk.
    jerk_threshold_cal (float): The jerk threshold value from the function used to calculate.
    threshold (float): The threshold value.
    number_failed_attempts (int): The number of failed attempts.
    sa_2axes (float): The value for sa_2axes.
    sumua (float): The value for sumua.
        
    Returns: 
    rs_2axes_py (float): Recovery Score (whether there was one or more than one attempts)
    '''

    if number_failed_attempts >= 1: 
        recovery_score_ua: float = get_rs_ua(sumua)
        add_ua(file_path, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, threshold, number_failed_attempts, sa_2axes, sumua, recovery_score_ua)        
        return recovery_score_ua
            
    else:
        recovery_score_sa: float = get_rs_sa(sa_2axes)
        add_sa(file_path, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, threshold, number_failed_attempts, sa_2axes, recovery_score_sa)
        return recovery_score_sa
            
