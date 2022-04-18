"""

Module for combinatorial webscraping of MLS property websites and automated posting to the Facebook Marketplace.

Uses the Selenium Python library to automate these processes.
Created for CS 321 Section 004, Group 5. George Mason University, Spring 2022.

Authors: Christopher Yi and Mohammed Bhuiyan
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.edge.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from getpass import getpass
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.keys import Keys
from urllib.request import Request, urlopen
import shutil
import csv
import os
import sys
import random

class MLSBot:
    """

    Creates a web scraper for MLS listings from Bright, Redfin, and Zillow.

    Users must be realtors or those with similar credentials to access MLS websites.
    Utilizes the Selenium Python library to automate its processes.
    Users must enter login credentials, browser, target website, and a path for data.
    This Data directory will hold CSVs for available listings and images of the properties.
    """
    def __init__(self, username, password, browser, site_id, data_path):
        """

        Inits necessary variables for the MLS Bot.

        Parameter username: The email/username/equivalent for a particular MLS website.

        Parameter password: The password for a particular MLS website.

        Parameter browser: The selected browser for the Selenium webdriver.
        Precondition: Limited to Chrome, Edge, or Firefox

        Parameter site_id: The selected MLS website for scraping.
        Precondition: Limited to Bright, Redfin, or Zillow

        Parameter data_path: The targeted repository to save MLS listings and images.
        Precondition: blank to default to project repository
        """
        self.username = username
        self.password = password
        self.browser = browser
        self.site_id = site_id
        self.data_path = data_path
        if not self.data_path:
            self.data_path = ""

    def try_find_element(self, type, target):
        """

        Wrapper method for finding elements.

        Implements an in-built wait function. Searches for elements for 10 seconds.
        Exits and prints error message if not found in time, returns if successful.

        Parameter type: The type of element being searched for.
        Precondition: Must comply with the selected types supported by the find_element Selenium function

        Parameter target: The target element being searched for.
        Precondition: Must be an existing web element or search will fail
        """
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((type, target))
        )
        if elem is None:
            self.driver.quit()
            sys.exit("ERROR. Element couldn't be found. Check credentials, website, and connection.")
        return elem

    def initDriver(self):
        """

        Initializes the Selenium webdriver based on user parameters.

        Sets up data path based on user input. Defaults to within the project directory.
        Initializes webdriver for Chrome, Edge, or Firefox with settings to suppress popup notifications.
        Invalid choices will exit and print error.
        """
        if self.data_path == "":
            self.data_path = os.getcwd() + "\\Data\\"
        else:
            self.data_path = self.data_path + "\\Data\\"
        dirExists = os.path.exists(self.data_path)
        if not dirExists:
            os.makedirs(self.data_path)
        prefs = {"download.default_directory" : self.data_path}
        if self.browser == 'Chrome':
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--disable-infobars")
            chromeOptions.add_argument("start-maximized")
            chromeOptions.add_argument("--disable-extensions")
            chromeOptions.add_argument("--disable-notifications")
            chromeOptions.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(options = chromeOptions, executable_path = "WebDrivers/chromedriver.exe")
        elif self.browser == 'Edge':
            # self.driver = webdriver.Edge("WebDrivers/msedgedriver.exe")
            edgeOptions = webdriver.EdgeOptions()
            edgeOptions.add_argument("--disable-infobars")
            edgeOptions.add_argument("start-maximized")
            edgeOptions.add_argument("--disable-extensions")
            edgeOptions.add_argument("--disable-notifications")
            edgeOptions.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Edge(options = edgeOptions, executable_path = "WebDrivers/msedgedriver.exe")
        elif self.browser == 'Firefox':
            # self.driver = webdriver.Firefox("WebDrivers/geckodriver.exe")
            firefoxOptions = Options()
            firefoxOptions.add_argument("--disable-infobars")
            firefoxOptions.add_argument("start-maximized")
            firefoxOptions.add_argument("--disable-extensions")
            firefoxOptions.add_argument("--disable-notifications")
            firefoxOptions.set_preference("browser.download.folderList", 2)
            firefoxOptions.set_preference("browser.download.dir", self.data_path)
            self.driver = webdriver.Firefox(options = firefoxOptions, executable_path = "WebDrivers/geckodriver.exe")
        else:
            sys.exit("Invalid browser!")

    def loginMLS(self):
        """

        Logs in to selected MLS website with user's credentials.
        """
        if self.site_id == 'Bright':
            bright_login = self.driver.get("https://login.brightmls.com/login")
            user = self.try_find_element(By.ID, "username")
            pw = self.try_find_element(By.ID, "password")
            user.send_keys(self.username)
            pw.send_keys(self.password)
            login = self.try_find_element(By.CSS_SELECTOR, ".MuiButton-label").click()
            wait = WebDriverWait(self.driver, 10).until(
                EC.title_is('Dashboard | Bright MLS')
            )

    def getListings(self,priceRange,zipcode):
        """

        Searches for and retrives listings from selected MLS website.
        """
        if self.site_id == 'Bright':
            old_file = os.path.join(self.data_path, 'Agent One-Line.csv')
            if os.path.exists(old_file):
                os.remove(old_file)

            search = self.driver.get("https://matrix.brightmls.com/Matrix/Search/ResidentialSale/Residential")

            self.try_find_element(By.ID, "Fm6_Ctrl36_TextBox").click()
            self.try_find_element(By.ID, "Fm6_Ctrl36_TextBox").send_keys(zipcode)
           ## self.driver.find_element(By.ID, "Fm6_Ctrl40_TB").click()
            self.try_find_element(By.ID, "Fm6_Ctrl40_TB").send_keys(priceRange)

            elem = self.try_find_element(By.CSS_SELECTOR, "option[title='VA']")
            elem.click()

            elem = self.try_find_element(By.CSS_SELECTOR, "#m_ucSearchButtons_m_clblCount")
            elem.click()

            elem = self.try_find_element(By.CSS_SELECTOR, ".linkIcon.icon_search")
            elem.click()

            elem = self.try_find_element(By.ID, "m_lnkCheckAllLink")
            elem.click()

            elem = self.try_find_element(By.CSS_SELECTOR, ".icon_export")
            elem.click()

            elem = self.try_find_element(By.ID, "m_btnExport")
            elem.click()

    def replacer(self, s, newstring, index, nofail=False):
        # raise an error if index is outside of the string
        if not nofail and index not in range(len(s)):
            raise ValueError("index outside given string")

        # if not erroring, but the index is still not in the correct range..
        if index < 0:  # add it to the beginning
            return newstring + s
        if index > len(s):  # add it to the end
            return s + newstring

        # insert the new string between "slices" of the original
        return s[:index] + newstring + s[index + 1:]

    #git test

    def img_downloader(self, image_url, MLS_NUM, imgcount,path):

    ## Set up the image URL and filename
        filename = MLS_NUM + "-" + str(imgcount)

    # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
        if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
            with open(path + "/" + filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ',filename)
            return 1
        else:
            print('Image Couldn\'t be retreived')
            return 0

    def addListings(self,priceRange,zipcode,num):

        self.getListings(priceRange,zipcode)

        # rnumber = random.sample(range(0,int(listNum)),int(num))

        time.sleep(10)
        # newList = csv.DictReader(open(self.data_path + 'Agent One-Line.csv', 'r'))
        # print(newList[2])

        with open(self.data_path + 'Agent One-Line.csv', 'r') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj)
            iterable = list(csv_dict_reader)
            rnumber = random.sample(range(0,int(len(iterable))), int(num))

            for randList in rnumber:
                self.pullListingImg(iterable[randList]['MLS #'])


    def pullListingImg(self, MLS_NUM):
        self.driver.get("https://matrix.brightmls.com/Matrix/Search/ResidentialSale/Residential")
        image_dir = self.data_path + '\\Pictures\\'
        dirExists = os.path.exists(image_dir)
        if not dirExists:
            os.makedirs(image_dir)

        elem = self.try_find_element(By.XPATH, "//input[@id='ctl01_m_ucSpeedBar_m_tbSpeedBar']")
        elem.clear()
        elem.send_keys(MLS_NUM)
        elem.send_keys(Keys.RETURN)

        time.sleep(2)

        content = self.try_find_element(By.XPATH, "//a[normalize-space()='" + str(MLS_NUM) + "']")

        content.click()

        time.sleep(1)

        try:
            elem = self.try_find_element(By.XPATH, "//img[@src='/Matrix/Images/cammulti.gif']")
        except:
            elem = self.try_find_element(By.XPATH, "//img[@src='/Matrix/Images/cam.gif']")

        elem.click()


        elem = self.try_find_element(By.XPATH, "//*[contains(@src,'Type=1&Size=4&')]")


        img_url = str(elem.get_attribute('src'))


        elem = self.try_find_element(By.CSS_SELECTOR, "td[class='d115m5'] span[class='formula field NoPrint']")

        img_count = str(elem.text).replace('(','')
        img_count = img_count.replace(')','')
        print(img_count)



        img_url = self.replacer(img_url,'',len(str(img_url)) - 1)


        #create new directory for new listing
        path = os.path.join(image_dir,MLS_NUM)

        #check if path exists
        if os.path.isdir(path) != True:
            os.mkdir(path)
        #Download the image
        for x in range (int(img_count)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.img_downloader(img_url + str(x),MLS_NUM, str(x),path)

    def checkListings(self):
        new_file = os.path.join(self.data_path, 'Current Listings.csv')
        if not os.path.exists(new_file):
            file = open(self.data_path + 'Current Listings.csv', 'w+')
            file.close()
        newList = csv.DictReader(open(self.data_path + 'Agent One-Line.csv', 'r'))
        # Add code to create/overwrite current listings
        curList = csv.DictReader(open(self.data_path + 'Current Listings.csv','r'))

        # Only active MLS numbers
        new_list_active = []
        new_list_comingsoon = []
        cur_list_active = []
        cur_list_comingsoon = []

        #new list
        for line in newList:

            if line['Status'] == 'ACT':
                new_list_active.append(line['MLS #'])

            if line['Status'] == 'C/S':
                new_list_comingsoon.append(line['MLS #'])

        #current list
        for line in curList:

            if line['Status'] == 'ACT':
                cur_list_active.append(line['MLS #'])

            if line['Status'] == 'C/S':
                cur_list_comingsoon.append(line['MLS #'])


        #New Listings
        new_list_active = list(set(new_list_active).difference(set((cur_list_active))))
        new_list_comingsoon = list(set(new_list_comingsoon).difference(set(cur_list_comingsoon)))

        #Listings that need to be removed
        remove_list_active = list(set(cur_list_active).difference(set((new_list_active))))
        remove_list_comingsoon = list(set(cur_list_comingsoon).difference(set((new_list_comingsoon))))

        #Listings that are the same
        cur_list_active = list(set(new_list_active) & set(cur_list_active))
        cur_list_comingsoon = list(set(new_list_comingsoon) & set(cur_list_comingsoon))

        for mls_num in new_list_active:
            addListing(mls_num.replace("'",""))


        for mls_num in new_list_comingsoon:
            addListing(mls_num.replace("'",""))


        for mls_num in remove_list_active:
            removeListing(mls_num.replace("'",""))


        for mls_num in remove_list_comingsoon:
            removeListing(mls_num.replace("'",""))


        print(len(new_list_active))
        print(len(new_list_comingsoon))

        old_file = os.path.join(self.data_path, 'Current Listings.csv')
        if os.path.exists(old_file):
            os.remove(old_file)
        os.rename(self.data_path + "\\Agent One-Line.csv", self.data_path + "\\Current Listings.csv")


class MarketBot:
    """

    Creates a web scraper to automate posting and editing Facebook Marketplace listings for MLS properties.

    Designed to work with the MLS Bot after automated scraping of MLS listings.
    """
    def __init__(self, email, password, browser):
        """

        Initializes the Selenium webdriver based on user parameters.

        Parameter email: The email for the user's Facebook account.

        Parameter password: The password for the user's Facebook account.

        Parameter browser: The selected browser for the Selenium webdriver.
        Precondition: Limited to Chrome, Edge, or Firefox
        """
        self.email = email
        self.password = password
        self.browser = browser
        self.fb_url = "https://www.facebook.com/"
        self.marketplace_url = "https://www.facebook.com/marketplace"

    def try_find_element(self, type, target):
        """

        Wrapper method for finding elements.

        Implements an in-built wait function. Searches for elements for 10 seconds.
        Exits and prints error message if not found in time, returns if successful.

        Parameter type: The type of element being searched for.
        Precondition: Must comply with the selected types supported by the find_element Selenium function

        Parameter target: The target element being searched for.
        Precondition: Must be an existing web element or search will fail
        """
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((type, target))
        )
        if elem is None:
            self.driver.quit()
            sys.exit("ERROR. Element couldn't be found. Check credentials, website, and connection.")
        return elem

    def initDriver(self):
        """

        Initializes the Selenium webdriver based on user parameters.

        Initializes webdriver for Chrome, Edge, or Firefox with settings to suppress popup notifications.
        Invalid choices will exit and print error.
        """
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
        """

        Logs in to Facebook with user's credentials.
        """
        fb_navigate = self.driver.get(self.fb_url)
        email_fill = self.try_find_element(By.ID, "email").send_keys(self.email)
        pass_fill = self.try_find_element(By.ID, "pass").send_keys(self.password)
        login_click = self.try_find_element(By.NAME, "login").click()

    def createListingFromMLS(self, MLS_NUM, structure_type, num_beds, num_baths, price, address):
        """

        Creates Facebook Marketplace listing from given parameters.
        """
        self.driver.get("https://www.facebook.com/marketplace/create/rental")
        image_folder = os.getcwd() + "\\Data\\" + "\\Pictures\\" + MLS_NUM
        for path in os.listdir(image_folder):
            photos_click = self.try_find_element(By.CSS_SELECTOR, "label:nth-child(2) > .mkhogb32").send_keys(os.path.join(image_folder, path))
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

# Init variables
browser_choice = input("Enter your browser (Chrome, Edge, or Firefox): ")
MLS_username = input("Enter your MLS username: ")
MLS_pw = getpass("Enter your MLS password: ")
MLS_choice = input("Enter the MLS site you are accessing (Bright, Zillow, Redfin): ")
FB_email = input("Enter your Facebook email: ")
FB_pw = getpass("Enter your Facebook password: ")
data_path = input("Enter which directory you would like to save listings/images to (leave blank for default): ")

# MLS Test
MLS_test = MLSBot(MLS_username, MLS_pw, browser_choice, MLS_choice, data_path)
MLS_test.initDriver()
MLS_test.loginMLS()
# MLS_test.getListings()
MLS_test.addListings("300-400","20111",3)
time.sleep(5000)

# MarketBot Test
# FB_test = MarketBot(FB_email, FB_pw, browser_choice)
# FB_test.initDriver()
# FB_test.loginFB()
# time.sleep(5)
# FB_test.createListingFromMLS("VAFX1160980", "Unit/Flat/Apartment", 2, 2, 339900, "12957 Centre Park Cir #206, Herndon, VA")
# time.sleep(5000)
