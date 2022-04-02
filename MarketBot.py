from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class FB:
    def __init__(self, email, password, webdriver_path):
        self.email = email
        self.password = password
        self.webdriver_path = webdriver_path
        self.driver = webdriver.Chrome(executable_path=self.webdriver_path)
        self.fb_url = "https://www.facebook.com/"
        self.marketplace_url = "https://www.facebook.com/marketplace"
        self.driver.get(self.fb_url)
        self.login()
        self.marketplace()

    def login(self):
        try:
            email_fill = self.driver.find_element(By.ID, "email").send_keys(self.email)
            pass_fill = self.driver.find_element(By.ID, "pass").send_keys(self.password)
            login_click = self.driver.find_element(By.NAME, "login").click()
        except Exception:
            print("Something went wrong logging in.")

    def marketplace(self):
        try:
            marketplace_navigate = self.driver.get(self.marketplace_url)
            create_listing_click = self.driver.find_element(By.NAME, "Create new listing").click()
        except Exception:
            print("Something went wrong in the Marketplace.")
