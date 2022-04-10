from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys

class FB:
    def __init__(self):
        self.email = input("Enter your Facebook email: ")
        self.password = input("Enter your Facebook password: ")
        self.browser = input("Enter your browser (Chrome, Edge, or Firefox): ")
        self.fb_url = "https://www.facebook.com/"
        self.marketplace_url = "https://www.facebook.com/marketplace"

    def launchBrowser(self):
        if self.browser == 'Chrome':
            self.driver = webdriver.Chrome("WebDrivers/chromedriver.exe")
        elif self.browser == 'Edge':
            self.driver = webdriver.Edge("WebDrivers/msedgedriver.exe")
        elif self.browser == 'Firefox':
            self.driver = webdriver.Firefox("WebDrivers/geckodriver.exe")
        else:
            sys.exit("Invalid browser!")
        self.driver.get(self.fb_url)

    def login(self):
        try:
            email_fill = self.driver.find_element(By.ID, "email").send_keys(self.email)
            pass_fill = self.driver.find_element(By.ID, "pass").send_keys(self.password)
            login_click = self.driver.find_element(By.NAME, "login").click()
        except Exception:
            print("Something went wrong logging in.")

    # def createListingFromMLS(self, site_id):
        # self.driver.get("https://www.facebook.com/marketplace/create")
        # if site_id == 'Bright':
