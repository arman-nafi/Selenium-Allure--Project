import os
import allure
import pytest
import logging
from seleniumbase import BaseCase
import time


@pytest.mark.usefixtures()
class LoginTest(BaseCase):
    def setUp(self):
        super().setUp()

        log_directory = "Logs Report"
        os.makedirs(log_directory, exist_ok=True)
        log_file_path = os.path.join(log_directory, "Branch Status.txt")

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        file_handler.setFormatter(log_formatter)

        logger.addHandler(file_handler)

    @allure.severity(allure.severity_level.MINOR)
    def test_branch_status(self):
        logging.info("*********************** Start Home Page Test ********************")
        self.open("https://hem.mikrof.com/login")
        self.maximize_window()
        self.assert_title("Login | Mikrof")
        logging.info("******************** Home Page Open Successfully ******************")

        # Add the login logic here
        logging.info("************ Start Login Functionality ************")
        username = "#email"
        password = "#password"
        btnLogin = "input[value='Login']"
        branch_status = "//a[normalize-space()='Branch status']"

        self.type(username, "username")
        self.type(password, "password")
        self.click(btnLogin)

        self.assert_title("Dashboard")
        logging.info("*************** Login Successful ****************")

        self.wait(5)

        # Branch Status Loading time
        logging.info("********** Start Branch Status Test ************")
        start_time = time.time()

        self.click(branch_status)

        self.wait_for_element_present('//*[@id="DivIdToPrint"]/h1')

        logging.info("********* Branch Status Open Successfully *************")

        self.save_screenshot("Branch Status.png", "screenshots")
        screenshot_path = os.path.join("screenshots", "Branch Status.png")
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

        end_time = time.time()
        loading_time = end_time - start_time

        logging.info(f"Branch Status Loading time: {loading_time} seconds")

    def tearDown(self):
        super().tearDown()

        logger = logging.getLogger()
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
