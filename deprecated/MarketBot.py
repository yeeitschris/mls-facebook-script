from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import sys

class FB:
    def __init__(self):
        self.email = input("Enter your Facebook email: ")
        self.password = getpass("Enter your Facebook password: ")
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

    def initDriver(self):
        if self.browser == 'Chrome':
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--disable-infobars")
            chromeOptions.add_argument("start-maximized")
            chromeOptions.add_argument("--disable-extensions")
            chromeOptions.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(options = chromeOptions, executable_path = "WebDrivers/chromedriver.exe")
        elif self.browser == 'Edge':
            edgeOptions = webdriver.EdgeOptions()
            edgeOptions.add_argument("--disable-infobars")
            edgeOptions.add_argument("start-maximized")
            edgeOptions.add_argument("--disable-extensions")
            edgeOptions.add_argument("--disable-notifications")
            self.driver = webdriver.Edge(options = edgeOptions, executable_path = "WebDrivers/msedgedriver.exe")
        elif self.browser == 'Firefox':
            firefoxOptions = Options()
            firefoxOptions.add_argument("--disable-infobars")
            firefoxOptions.add_argument("start-maximized")
            firefoxOptions.add_argument("--disable-extensions")
            firefoxOptions.add_argument("--disable-notifications")
            self.driver = webdriver.Firefox(options = firefoxOptions, executable_path = "WebDrivers/geckodriver.exe")
        else:
            sys.exit("Invalid browser!")

    def loginFB(self):
        fb_navigate = self.driver.get(self.fb_url)
        email_fill = self.try_find_element(By.ID, "email").send_keys(self.email)
        pass_fill = self.try_find_element(By.ID, "pass").send_keys(self.password)
        login_click = self.try_find_element(By.NAME, "login").click()

    def createListingFromMLS(self, structure_type, num_beds, num_baths, price, address):
        self.driver.get("https://www.facebook.com/marketplace/create/rental")
        sale_or_rent = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Home for Sale or Rent"]').click()
        sale_types = self.driver.find_elements(By.CSS_SELECTOR, '[aria-selected="false"]')
        sale_click = sale_types[1].click()
        property_type = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Property type"]').click()
        property_types = self.driver.find_elements(By.CSS_SELECTOR, '[aria-selected="false"]')
        if "Apartment" in structure_type:
            apartment_click = property_types[0].click()
        beds_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Number of bedrooms"]').send_keys(num_beds)
        baths_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Number of bathrooms"]').send_keys(num_baths)
        price_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Price"]').send_keys(price)
        address_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Property address"]').send_keys(address)
        suggestion_click = self.try_find_element(By.CSS_SELECTOR, '[aria-selected="false"]').click()
