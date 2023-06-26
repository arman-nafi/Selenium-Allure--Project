import os
import allure
from seleniumbase import BaseCase
import pytest
import random
import string
import logging


username = '//*[@id="email"]'
password = '//*[@id="password"]'
btnLogin = "/html/body/section/div/div/div[3]/div/div[3]/form/div/div[3]/input"
errormgs = '/html/body/section/div/div/div[3]/div/div[3]/form/div/span/strong'

@pytest.mark.usefixtures()
class LoginTest(BaseCase):

    def setUp(self):
        super().setUp()

        log_directory = "Logs Report"
        os.makedirs(log_directory, exist_ok=True)
        log_file_path = os.path.join(log_directory, "Login.txt")

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        file_handler.setFormatter(log_formatter)

        logger.addHandler(file_handler)

    @allure.severity(allure.severity_level.MINOR)
    def test_home_page_title(self):
        logging.info("******************* Start Home Page Test **********************")
        self.open("https://hem.mikrof.com/")
        self.maximize_window()
        title = self.get_title()
        logging.info("Home Page Title: %s", title)
        self.assert_title("Login | Mikrof")
        logging.info("********** Home Page Open Successfully ************")

        self.save_screenshot("Homepage.png", "Screenshots")
        screenshot_path = os.path.join("screenshots", "Homepage.png")
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.severity(allure.severity_level.MINOR)
    def test_valid_username_password(self):
        logging.info("************ Start Login Valid Username Password Test ***************")
        self.open("https://hem.mikrof.com/")
        self.maximize_window()
        self.type(username, "mikrof")
        self.type(password, "@#$imikrof@2022")
        self.click(btnLogin)

        self.save_screenshot("Login page.png", "Screenshots")
        screenshot_path = os.path.join("screenshots", "Login Page.png")
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

        title = self.get_title()
        logging.info("Login Page Title: %s", title)
        self.assert_title("Dashboard")



    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_username(self):
        logging.info("************ Start Invalid Username Test ****************")
        self.open("https://hem.mikrof.com/")
        self.maximize_window()
        random_name = ''.join(random.choices(string.ascii_letters, k=10))
        self.type(username, random_name)
        self.type(password, "@#$imikrof@2022")
        self.click(btnLogin)

        self.save_screenshot("Invalid Username.png", "Screenshots")
        screenshot_path = os.path.join("screenshots", "Invalid Username.png")
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

        if self.is_element_visible(errormgs):
            error_text = self.get_text(errormgs)
            if "Invalid Password ! Please Try Again" in error_text:
                logging.info("Invalid username test passed")
            else:
                logging.error("Unknown error occurred")
        else:
            logging.error("Login successful test failed")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_password(self):
        logging.info("************ Start Invalid Password Test ****************")
        self.open("https://hem.mikrof.com/")
        self.maximize_window()
        random_password = ''.join(random.choices(string.ascii_letters, k=10))
        self.type(username, "mikrof")
        self.type(password, random_password)
        self.click(btnLogin)

        self.save_screenshot("Invalid Password.png", "Screenshots")
        screenshot_path = os.path.join("screenshots", "Invalid Password.png")
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

        if self.is_element_visible(errormgs):
            error_text = self.get_text(errormgs)
            if "Invalid Password ! Please Try Again" in error_text:
                logging.info("********* Invalid Password test passed ************")
            else:
                logging.error("************* Unknown error occurred **************")
        else:
            logging.error("*********** Login successful test failed **************")

    def tearDown(self):
        super().tearDown()

        logger = logging.getLogger()
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)