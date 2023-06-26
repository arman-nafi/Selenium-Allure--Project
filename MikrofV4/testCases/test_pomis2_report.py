import logging
import os
import allure
from seleniumbase import BaseCase
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

set_report_level = "Branch"
set_month = "January"
set_year = "2023"
set_loan_option = "Loan Product"


class Pomis2Report(BaseCase):

    def setUp(self):
        super().setUp()

        log_directory = "Logs Report"
        os.makedirs(log_directory, exist_ok=True)
        log_file_path = os.path.join(log_directory, "Pomis2 All Branch.txt")

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        file_handler.setFormatter(log_formatter)

        logger.addHandler(file_handler)

    def test_pomis2(self):

        logging.info("******************* Start Open Url *******************")

        self.open("https://hem.mikrof.com/login")
        # Add the login logic here
        username = "#email"
        password = "#password"
        btnLogin = "input[value='Login']"

        self.type(username, "mikrof")
        self.type(password, "@#$imikrof@2022")
        self.click(btnLogin)

        logging.info("********** Login Successful ***********")

        report_level = "#report_level"
        branch = "#filter_bazr_info"
        month = "select[name='cbo_month']"
        year = "select[name='cbo_year']"
        loan_option = "select[name='cbo_loan_type']"
        show = "button[type='submit']"

        # Pomis-2 Reports

        start_time = time.time()
        logging.info("******************* Start Test Pomis2 Report *******************")
        logging.info("********* Navigate Pomis-2 Report **********")

        self.open_url("https://hem.mikrof.com/reports/pomis-2")
        self.type(report_level, set_report_level)
        self.wait(1)
        self.type(branch, "All")
        self.type(month, set_month)
        self.type(year, set_year)
        self.type(loan_option, set_loan_option)
        self.click(show)

        # Wait for the element to be present
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="DivIdToPrint"]/div/div/div/h2/div'))
            )
        except NoSuchElementException:
            logging.info("Element not found after 10 seconds")

        #self.wait(30)

        self.assert_text("POMIS-2 Report (with Service Charge)", '//*[@id="DivIdToPrint"]/div/div/div/h2/div')

        self.save_screenshot("Pomis2 All Branch.png", "screenshots")
        screenshot_path = os.path.join("screenshots", "Pomis2 All Branch.png")
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

        logging.info("************ Report Open Successfully ***************")

        end_time = time.time()
        loading_time = end_time - start_time

        logging.info(f"Loading time: {loading_time} seconds")

    def tearDown(self):
        super().tearDown()

        logger = logging.getLogger()
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)