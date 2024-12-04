# Recovery Score Calculations: CSV_helper Script
# Script created  8/10/2024
# Last revision 12/1/2024

import csv
import pandas as pd
from datetime import datetime

class CSV:
    CSV_FILE:str = 'RS_output.csv'
    COLUMNS: list[str] = ['Date', 'Case_Number', 'Number_Failed_Attempts', 'sa_2axes_py', 'sumua_py', 'rs_2axes_py']
    FORMAT:str = '%m-%d-%Y'
    
    @classmethod
    def initialize_csv(cls) -> None:
        '''Initializes the CSV file. If the file does not exist, it creates a new CSV file
        with the specified columns.
        
        Raises:
            FileNotFoundError: If the CSV file does not exist.
        '''
        
        try:
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index = False)

    @classmethod
    def add_entry(cls, date, case_number, number_of_failed_attempts, sa_2axes, sumua, rs_2axes_py) -> None:
        '''Adds a new entry to the CSV file.
            
        Args:
            date (str): The date of the entry.
            case_number (int): The case number associated with the entry.
            number_of_failed_attempts (int): The number of failed attempts.
            sa_2axes (float): The value for sa_2axes.
            sumua (float or None): The value for sumua. If None, it will be replaced with an empty string.
            rs_2axes_py (float): The value for rs_2axes_py.     
         
        Returns:
            None
        '''
        new_entry:dict = {
            'Date': date,
            'Case_Number': case_number,
            'Number_Failed_Attempts': number_of_failed_attempts,
            'sa_2axes_py': sa_2axes,
            'sumua_py': sumua,
            'rs_2axes_py': rs_2axes_py,
            
        }

        with open(cls.CSV_FILE, 'a', newline = '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = cls.COLUMNS)
            #Replace None with empty string if sumua is None
            sumua = '' if sumua is None else sumua
            writer.writerow(new_entry)
        print('Entry added successfully')      

def add_ua(file_path :str, number_of_failed_attempts: int, sa_2axes: float, sumua: float, rs_2axes_py: float) -> None:
    '''_summary_

    Args:
        file_path (str): _description_
        number_of_failed_attempts (int): _description_
        sa_2axes (float): _description_
        sumua (float): _description_
        rs_2_axes_py:
    '''
    CSV.initialize_csv()
    date:str = get_date()
    case_number: str = rename(file_path)
    CSV.add_entry(date, case_number, number_of_failed_attempts, sa_2axes, sumua, rs_2axes_py)

def add_sa(file_path :str, number_of_failed_attempts: int, sa_2axes: float, rs_2axes_py: float) -> None:
    '''_summary_

    Args:
        file_path (str): _description_
        number_of_failed_attempts (int): _description_
        sa_2axes (float): the score for when there is only one successful attempt
        sumua (None): in a single and successful attempt, there is no value for sumua
        rs_2axes_py (float): _description_
    '''
    CSV.initialize_csv()
    date:str = get_date()
    case_number: str = rename(file_path)
    sumua = None
    CSV.add_entry(date, case_number, number_of_failed_attempts, sa_2axes, sumua, rs_2axes_py)

def get_date() -> str:
    '''Generates a timestamp for the backup file

    Returns:
        str: 
    '''
    start_time: str = datetime.now().strftime('%Y-%m-%d_%H.%M')

    return start_time

def rename(file_path:str) -> str:
    '''Renames the file's name by removing the .csv

    Args:
        file_path (str): _description_

    Returns:
        str:new file name
    '''
    case_number:str = file_path.replace('.csv', '')

    return case_number

