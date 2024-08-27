from datetime import datetime
import pandas as pd

def read_test_cases(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

def update_test_case_status(file_path, index, result, actual_result):
    
    df = pd.read_excel(file_path, engine='openpyxl')
    df.at[index, 'Result'] = result
    df.at[index, 'Actual_Result'] = actual_result
    df.at[index, 'DateTimeTested'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(file_path, index=False)