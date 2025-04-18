# Recovery Score Calculations: CSV_helper Script
# Script created  8/10/2024
# Last revision 12/23/2024

import csv
import pandas as pd
from datetime import datetime

class CSV:
    CSV_FILE:str = 'RS_output.csv'
    COLUMNS: list[str] = ['Date', 'Case_Number', 'jerk_threshold', 'mean_jerk', 'std_jerk', 'jerk_threshold_cal', 'snap_threshold_cal', 'Number_failed_attempts', 'sa_2axes_py', 'sumua_py', 'rs_2axes_py']
    FORMAT:str = '%m-%d-%Y'
    
    @classmethod
    def initialize_csv(cls) -> None:
        '''Initializes the CSV file. If the file does not exist, it creates a new CSV file
        with the specified columns. If the file exists, it reads the file
        
        Raises:
            FileNotFoundError: If the CSV file does not exist.
        '''
        
        try:
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            # Creates a new CSV file with the specified columns
            df = pd.DataFrame(columns = cls.COLUMNS)
            # Saves the new CSV file
            df.to_csv(cls.CSV_FILE, index = False)

    @classmethod
    def add_entry(cls, date, case_number, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, snap_threshold_cal, number_failed_attempts, sa_2axes, sumua, rs_2axes_py) -> None:
        '''Adds a new entry to the CSV file
            
        Args:
            date (str): The date of the entry
            case_number (int): The case number associated with the entry
            jerk_threshold (float): The jerk threshold value
            mean_jerk (float): The mean jerk value
            std_jerk (float): The standard deviation of the jerk
            jerk_threshold_cal (float): The jerk threshold value from the function used to calculate
            snap_threshold_cal (float): The snap threshold value
            number_failed_attempts (int): The number of failed attempts
            sa_2axes (float): The value for sa_2axes
            sumua (float or None): The value for sumua. If None, it will be replaced with an empty string.
            rs_2axes_py (float): The value for rs_2axes_py    
         
        Returns:
            None
        '''
        new_entry:dict = {
            'Date': date,
            'Case_Number': case_number,
            'jerk_threshold': jerk_threshold,
            'mean_jerk': mean_jerk,
            'std_jerk': std_jerk,
            'jerk_threshold_cal': jerk_threshold_cal,
            'snap_threshold_cal': snap_threshold_cal,
            'Number_failed_attempts': number_failed_attempts,
            'sa_2axes_py': sa_2axes,
            'sumua_py': sumua,
            'rs_2axes_py': rs_2axes_py   
        }

        with open(cls.CSV_FILE, 'a', newline = '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = cls.COLUMNS)
            # Replaces with empty string if sumua does not exist
            sumua = '' if sumua is None else sumua
            # Writes the new entry to the CSV file
            writer.writerow(new_entry)
        print('Entry added successfully')      

def add_ua(file_path: str, jerk_threshold: float, mean_jerk: float, std_jerk: float, jerk_threshold_cal: float, snap_threshold_cal: float, number_failed_attempts: int, sa_2axes: float, sumua: float, rs_2axes_py: float) -> None:
    '''Adds new UA entry to a CSV file

    Args:
        file_path (str): name of the file
        jerk_threshold (float): threshold for jerk
        mean_jerk (float): mean jerk value
        std_jerk (float): standard deviation of jerk
        jerk_threshold_cal (float): jerk threshold value from the function used to calculate
        snap_threshold_cal (float): snap threshold value
        number_failed_attempts (int): number of failed attempts (jerk method)
        sa_2axes (float): calculated score using data from 2 axes (X and Y)
        sumua (float): calculated score using data from all axes
        rs_2_axes_py: calculated recovery score for 2 axes
    '''
    CSV.initialize_csv()
    date:str = get_date()
    case_number: str = rename(file_path)
    CSV.add_entry(date, case_number, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, snap_threshold_cal, number_failed_attempts, sa_2axes, sumua, rs_2axes_py)

def add_sa(file_path :str, jerk_threshold: float, mean_jerk: float, std_jerk: float, jerk_threshold_cal: float, snap_threshold_cal: float, number_failed_attempts: int, sa_2axes: float, rs_2axes_py: float) -> None:
    '''Adds entry for a single and successful attempt to a CSV file

    Args:
        file_path (str): name of the file
        jerk_threshold (float): threshold for jerk
        mean_jerk (float): mean jerk value
        std_jerk (float): standard deviation of jerk
        jerk_threshold_cal (float): jerk threshold value from the function used to calculate
        snap_threshold_cal (float): threshold value
        number_failed_attempts_sd (int): number of failed attempts
        sa_2axes (float): the score for when there is only one successful attempt
        sumua (None): in a single and successful attempt, there is no value for sumua
        rs_2axes_py (float): recovery score for 2 axes
    '''
    CSV.initialize_csv()
    date:str = get_date()
    case_number: str = rename(file_path)
    sumua = None
    #number_failed_attempts_jerk = number_failed_attempts_jerk
    CSV.add_entry(date, case_number, jerk_threshold, mean_jerk, std_jerk, jerk_threshold_cal, snap_threshold_cal, number_failed_attempts, sa_2axes, sumua, rs_2axes_py)

def get_date() -> str:
    '''Generates a timestamp for the backup file

    Returns:
        str: 
    '''
    start_time: str = datetime.now().strftime('%Y-%m-%d_%H.%M')

    return start_time

def rename(file_path:str) -> str:
    '''Renames the file's name by removing the ".csv" extension

    Args:
        file_path (str): name of the file

    Returns:
        str:new file name without the .csv extesion
    '''
    case_number:str = file_path.replace('.csv', '')

    return case_number

