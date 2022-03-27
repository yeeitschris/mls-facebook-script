from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class FB:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome(executable_path="D:\Chris\Downloads\chromedriver_win32\chromedriver.exe")
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


test = FB('djy159357@gmail.com', 'krnpriide5dongju')
test.login()
test.marketplace()
