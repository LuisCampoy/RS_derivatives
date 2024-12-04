# Recovery Score Calculations: save_data_helper Script
# Script created  5/30/2024
# Last revision 8/10/2024

import os
import pandas as pd

from CSV_helper import rename
from recovery_score_helper import get_rs_ua, get_rs_sa
from CSV_helper import add_sa, add_ua

def process_recovery(file_path: str, number_of_failed_attempts: int, sa_2axes: float,
                         sumua: float) -> float:
    """Processes recovery scores depending whether it is one or more attempts.
    Logs them to a CSV file.

    Args:

    Returns: float: Recovery Score (rs_py) (whether there was one or more than one attempts)
    """

    if number_of_failed_attempts >= 1: 
        recovery_score_ua: float = get_rs_ua(sumua)
        add_ua(file_path, number_of_failed_attempts, sa_2axes, sumua, recovery_score_ua)
        return recovery_score_ua
            
    else:
        recovery_score_sa: float = get_rs_sa(sa_2axes)
        add_sa(file_path, number_of_failed_attempts, sa_2axes, recovery_score_sa)
        return recovery_score_sa
            
