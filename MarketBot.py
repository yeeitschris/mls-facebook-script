from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys

class FB:
    def __init__(self):
        self.email = input("Enter your Facebook email: ")
        self.password = input("Enter your Facebook password: ")
        self.browser = input("Enter your browser (Chrome, Edge, or Firefox): ")
        self.fb_url = "https://www.facebook.com/"
        self.marketplace_url = "https://www.facebook.com/marketplace"

    def try_find_element(self, type, target):
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((type, target))
        )
        if elem is None:
            self.driver.quit()
            sys.exit("ERROR. Element couldn't be found. Check credentials, website, and connection.")
        return elem

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
        email_fill = self.try_find_element(By.ID, "email").send_keys(self.email)
        pass_fill = self.try_find_element(By.ID, "pass").send_keys(self.password)
        login_click = self.try_find_element(By.NAME, "login").click()

    def createListingFromMLS(self, site_id):
        self.driver.get("https://www.facebook.com/marketplace/create/rental")
        if site_id == 'Bright':
            property_type = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Home for Sale or Rent']")))
            property_type.click()
