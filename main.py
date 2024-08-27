import logging
from src.test_runner import run_tests
from src.email_utils import send_email
from config.settings import REPORT_FILE_PATH, LOG_FILE_PATH
from datetime import datetime
from src.cases.constants import BASE_URL

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

if __name__ == "__main__":
    logging.info("Starting test automation")
    run_tests()
    date = datetime.now().strftime("%Y-%m-%d")
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # send_email(f"Test Automation Report, tested at {date}", f"Find the attached test report. The cases are tested on site {BASE_URL} at {date_time}")
    logging.info("Test automation completed")
