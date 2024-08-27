from .excel_utils import read_test_cases, update_test_case_status
from config.settings import EXCEL_FILE_PATH
import logging
from src.cases.test_case import * 

from selenium import webdriver #by this we can access the webdriver which is inbuild method of selenium
from selenium.webdriver.chrome.service import Service   #This is selenium 4 new feature in which we import service 

from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import math


# test
def driver_initlise():
    logging.info("Initiating the wev driver")
    # ser_Obj = Service("C:\\Users\\91635\\Desktop\\drivers\\chrome\\chromedriver.exe")
    ser_obj = Service("C:\\Users\\91635\\Desktop\\drivers\\firefox\\geckodriver.exe")
    drivers = webdriver.Firefox(service= ser_obj)
    # drivers = webdriver.Chrome(ChromeDriverManager().install())
    drivers.implicitly_wait(30)
    
    return drivers


def run_tests():
    # driver = driver_initlise()
    # testcase_10(driver)
    
    # time.sleep(5)
    # driver.quit()
    logging.info("reading test cases from excel file")
    test_cases = read_test_cases(EXCEL_FILE_PATH)

    for cases in test_cases['TestCaseID']:
        if pd.isna(cases) or cases == "NaN":  # Check if the value is NaN or a string "NaN"
            cases = 0  # Assign 0 if it's NaN
        else:
            cases = int(cases) 
        logging.info(f"executing the case id : {cases}" )
        function_name = f"testcase_{cases}"
        
        if function_name in globals() and callable(globals()[function_name]):
            driver = driver_initlise()
            logging.info(f"calling function according the test casse id: {cases}" )
            function_to_call = globals()[function_name]
            actual_result,status = function_to_call(driver)
            update_test_case_status(EXCEL_FILE_PATH, cases-1, status, actual_result)
            
            driver.quit()
        else:
            logging.info(f"Function {function_name} does not exist or is not callable.")