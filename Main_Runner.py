"""

Module for combinatorial webscraping of MLS property websites and automated posting to the Facebook Marketplace.

Uses the Selenium Python library to automate these processes.
Created for CS 321 Section 004, Group 5. George Mason University, Spring 2022.

Authors: Christopher Yi and Mohammed Bhuiyan
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.edge.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from getpass import getpass
import time
import requests
import urllib.request
from urllib.request import Request, urlopen
import shutil
import csv
import os
import sys
import random
import shutil

remove_list = []

class MLSBot:
    """

    Creates a web scraper for MLS listings from Bright, Redfin, and Zillow.

    Users must be realtors or those with similar credentials to access MLS websites.
    Utilizes the Selenium Python library to automate its processes.
    Users must enter login credentials, browser, target website, and a path for data.
    This Data directory will hold CSVs for available listings and images of the properties.
    """
    def __init__(self, username, password, browser, site_id, data_path, price_range, zip_code, num_properties):
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
        # Default data path if left blank
        self.data_path = data_path
        if not self.data_path:
            self.data_path = ""
        # Price range is optional
        self.price_range = price_range
        if not self.price_range:
            self.price_range = ""
        # ZIP code is optional
        self.zip_code = zip_code
        if not self.zip_code:
            self.zip_code = ""
        # Number of properties is optional
        self.num_properties = num_properties
        if not self.num_properties:
            self.num_properties = 0

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
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((type, target))
            )
        except:
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
            driver_path = ChromeService("WebDrivers/chromedriver.exe")
            self.driver = webdriver.Chrome(service = driver_path, options = chromeOptions)
        elif self.browser == 'Edge':
            # self.driver = webdriver.Edge("WebDrivers/msedgedriver.exe")
            edgeOptions = webdriver.EdgeOptions()
            edgeOptions.add_argument("--disable-infobars")
            edgeOptions.add_argument("start-maximized")
            edgeOptions.add_argument("--disable-extensions")
            edgeOptions.add_argument("--disable-notifications")
            edgeOptions.add_experimental_option("prefs", prefs)
            driver_path = EdgeService("WebDrivers/msedgedriver.exe")
            self.driver = webdriver.Edge(service = driver_path, options = edgeOptions)
        elif self.browser == 'Firefox':
            # self.driver = webdriver.Firefox("WebDrivers/geckodriver.exe")
            firefoxOptions = Options()
            firefoxOptions.add_argument("--disable-infobars")
            firefoxOptions.add_argument("start-maximized")
            firefoxOptions.add_argument("--disable-extensions")
            firefoxOptions.add_argument("--disable-notifications")
            firefoxOptions.set_preference("browser.download.folderList", 2)
            firefoxOptions.set_preference("browser.download.dir", self.data_path)
            driver_path = FirefoxService("WebDrivers/geckodriver.exe")
            self.driver = webdriver.Firefox(service = driver_path, options = firefoxOptions)
        else:
            sys.exit("Invalid browser!")
        self.driver.minimize_window()

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
            try:
                wait = WebDriverWait(self.driver, 10).until(
                    EC.title_is('Dashboard | Bright MLS')
                )
            except selenium.common.exceptions.TimeoutException:
                if self.driver.title == "SSO | Bright MLS":
                    self.driver.quit()
                    sys.exit("Bright MLS login failed. Check credentials or connection.")
                else:
                    try:
                        deprecated_login_leave = self.driver.get("https://www.brightmls.com/dashboard")
                        wait = WebDriverWait(self.driver, 10).until(
                            EC.title_is('Dashboard | Bright MLS')
                        )
                    except selenium.common.exceptions.TimeoutException:
                        self.driver.quit()
                        sys.exit("Bright MLS login failed. Check credentials or connection.")

    def getListingsCSV(self):
        """

        Searches for and retrives listings from selected MLS website.
        """
        if self.site_id == 'Bright':
            # Deletes old Bright CSV.
            old_file = os.path.join(self.data_path, 'Agent One-Line.csv')
            if os.path.exists(old_file):
                os.remove(old_file)
            # Navigate to residential search page.
            search = self.driver.get("https://matrix.brightmls.com/Matrix/Search/ResidentialSale/Residential")
            # Designate ZIP code, if any.
            if self.zip_code != "":
                self.try_find_element(By.ID, "Fm6_Ctrl36_TextBox").click()
                self.try_find_element(By.ID, "Fm6_Ctrl36_TextBox").send_keys(self.zip_code)
            # Designate price range, if any.
            if self.price_range != "":
                self.try_find_element(By.ID, "Fm6_Ctrl40_TB").send_keys(self.price_range)
            # Designate Virginia properties.
            elem = self.try_find_element(By.CSS_SELECTOR, "option[title='VA']")
            elem.click()
            # Search for properties.
            elem = self.try_find_element(By.CSS_SELECTOR, "#m_ucSearchButtons_m_clblCount")
            elem.click()
            # Show search results.
            elem = self.try_find_element(By.CSS_SELECTOR, ".linkIcon.icon_search")
            elem.click()
            # Select all listings.
            elem = self.try_find_element(By.ID, "m_lnkCheckAllLink")
            elem.click()
            # Choose to export listings.
            elem = self.try_find_element(By.CSS_SELECTOR, ".icon_export")
            elem.click()
            # Open drag down
            elem = self.try_find_element(By.ID, "m_ddExport")
            elem.click()
            # Select Agent One-Line
            elem = self.try_find_element(By.XPATH, "//option[. = 'Agent One-Line']")
            elem.click()
            # Export listings.
            elem = self.try_find_element(By.ID, "m_btnExport")
            elem.click()

    def getDefaultCSV(self):
        """

        Searches for and retrives listings from selected MLS website.
        """
        if self.site_id == 'Bright':
            # Deletes old Bright CSV.
            old_file = os.path.join(self.data_path, 'Agent One-Line.csv')
            if os.path.exists(old_file):
                os.remove(old_file)
            # Navigate to residential search page.
            search = self.driver.get("https://matrix.brightmls.com/Matrix/Search/ResidentialSale/Residential")
            # Designate Virginia properties.
            elem = self.try_find_element(By.CSS_SELECTOR, "option[title='VA']")
            elem.click()
            # Search for properties.
            elem = self.try_find_element(By.CSS_SELECTOR, "#m_ucSearchButtons_m_clblCount")
            elem.click()
            # Show search results.
            elem = self.try_find_element(By.CSS_SELECTOR, ".linkIcon.icon_search")
            elem.click()
            # Select all listings.
            elem = self.try_find_element(By.ID, "m_lnkCheckAllLink")
            elem.click()
            # Choose to export listings.
            elem = self.try_find_element(By.CSS_SELECTOR, ".icon_export")
            elem.click()
            # Open drag down
            elem = self.try_find_element(By.ID, "m_ddExport")
            elem.click()
            # Select Agent One-Line
            elem = self.try_find_element(By.XPATH, "//option[. = 'Agent One-Line']")
            elem.click()
            # Export listings.
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

    def img_downloader(self, image_url, MLS_NUM, imgcount,path):

        # Set up the image URL and filename
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
            print('Image could not be retrieved')
            return 0

    def updateListings(self):
        """

        Parses the existing prior listings against all listings. Updates and replaces list.
        """
        current_listings = os.path.join(self.data_path, 'Current Listings.csv')
        # If current listings does not exist, program is running fresh. Create file with headers and return.
        if not os.path.exists(current_listings):
            file = open(self.data_path + 'Current Listings.csv', 'w+')
            fileWriter = csv.writer(file)
            fileWriter.writerow(['MLS #', 'Cat', 'Status', 'Address', 'City', 'County', 'Beds', 'Baths', 'Structure Type', 'Status Contractual Search Date', 'List Office Name', 'Current Price'])
            file.close()
            self.assertTrue(os.path.exists(current_listings),"CSV Generation Error")
            return
        else:
            # Current listings exists. Download all state listings and parse to update attributes.
            self.getDefaultCSV()
            file_wait = 0
            while not os.path.exists(self.data_path + 'Agent One-Line.csv'):
                time.sleep(1)
                file_wait += 1
                if file_wait > 10:
                    break
            # Parse both the current and all listings and write to new file.
            allListingsFile = open(self.data_path + 'Agent One-Line.csv', 'r')
            allListingsDict = csv.DictReader(allListingsFile)

            currentListingsFile = open(self.data_path + 'Current Listings.csv', 'r')
            currentListingsDict = csv.DictReader(currentListingsFile)

            updatedListingsFile = open(self.data_path + 'Updated Listings.csv', 'w+', newline='')
            updateWriter = csv.writer(updatedListingsFile)

            updateWriter.writerow(['MLS #', 'Cat', 'Status', 'Address', 'City', 'County', 'Beds', 'Baths', 'Structure Type', 'Status Contractual Search Date', 'List Office Name', 'Current Price'])
            updateDictWriter = csv.DictWriter(updatedListingsFile, fieldnames=['MLS #', 'Cat', 'Status', 'Address', 'City', 'County', 'Beds', 'Baths', 'Structure Type', 'Status Contractual Search Date', 'List Office Name', 'Current Price'])

            for oldListingLine in currentListingsDict:
                for newListingLine in allListingsDict:
                    if oldListingLine['MLS #'] == newListingLine['MLS #']:
                        updateDictWriter.writerow(newListingLine)
                        break

            for curLine in currentListingsDict:
                flag = 0
                for allLine in allListingsDict:
                    if curLine['MLS #'] == allLine['MLS #']:
                        flag = 1
                        break
                if flag == 1:
                    continue
                remove_list.append(curLine['MLS #'])

            updatedListingsFile.close()
            allListingsFile.close()
            currentListingsFile.close()
            # Delete old files, designate new current listings.
            old_current_listings = os.path.join(self.data_path, 'Current Listings.csv')
            os.remove(old_current_listings)
            all_listings = os.path.join(self.data_path, 'Agent One-Line.csv')
            os.remove(all_listings)
            os.rename(self.data_path + "\\Updated Listings.csv", self.data_path + "\\Current Listings.csv")
            listings_as_dict = csv.DictReader(open(self.data_path + 'Current Listings.csv', 'r'))
            for listing in listings_as_dict:
                self.pullListingImg(listing['MLS #'])

    def pullListings(self):

        self.getListingsCSV()
        file_wait = 0
        while not os.path.exists(self.data_path + 'Agent One-Line.csv'):
            time.sleep(1)
            file_wait += 1
            if file_wait > 10:
                break
        if os.path.exists(self.data_path + 'Agent One-Line.csv'):
            listings_as_file = open(self.data_path + 'Agent One-Line.csv', 'r')
            listings_as_dict = csv.DictReader(listings_as_file)
            iterable = list(listings_as_dict)

            updatedListingsFile = open(self.data_path + 'Updated Listings.csv', 'w+', newline='')
            updateWriter = csv.writer(updatedListingsFile)
            updateWriter.writerow(['MLS #', 'Cat', 'Status', 'Address', 'City', 'County', 'Beds', 'Baths', 'Structure Type', 'Status Contractual Search Date', 'List Office Name', 'Current Price'])
            updateDictWriter = csv.DictWriter(updatedListingsFile, fieldnames=['MLS #', 'Cat', 'Status', 'Address', 'City', 'County', 'Beds', 'Baths', 'Structure Type', 'Status Contractual Search Date', 'List Office Name', 'Current Price'])

            if int(self.num_properties) < len(iterable):
                if self.num_properties != 0:
                    rnumber = random.sample(range(0,int(len(iterable))), int(self.num_properties))
                else:
                    self.driver.quit()
                    sys.exit("You selected 0 properties.")
            else:
                rnumber = random.sample(range(0,int(len(iterable))), len(iterable))

            for randList in rnumber:
                self.pullListingImg(iterable[randList]['MLS #'])
                updateDictWriter.writerow(iterable[randList])
            listings_as_file.close()
            updatedListingsFile.close()
            new_listings = os.path.join(self.data_path, 'Agent One-Line.csv')
            os.remove(new_listings)
            os.rename(self.data_path + "\\Updated Listings.csv", self.data_path + "\\Agent One-Line.csv")
        else:
            self.driver.quit()
            sys.exit("Error. CSV file failed to download. Check search parameters or internet connection.")

    def addNewListings(self):
        newListingsFile = open(self.data_path + 'Agent One-Line.csv', 'r')
        newListingsDict = csv.DictReader(newListingsFile)
        currentListingsFile = open(self.data_path + 'Current Listings.csv', 'r')
        currentListingsDict = csv.DictReader(currentListingsFile)
        shutil.copyfile(self.data_path + 'Current Listings.csv', self.data_path + 'Updated Listings.csv')
        updatedListingsFile = open(self.data_path + 'Updated Listings.csv', 'a', newline='')
        updateDictWriter = csv.DictWriter(updatedListingsFile, fieldnames=['MLS #', 'Cat', 'Status', 'Address', 'City', 'County', 'Beds', 'Baths', 'Structure Type', 'Status Contractual Search Date', 'List Office Name', 'Current Price'])
        for newListingLine in newListingsDict:
            match = False
            for oldListingLine in currentListingsDict:
                if oldListingLine['MLS #'] == newListingLine['MLS #']:
                    match = True
                    break
            if match is False:
                updateDictWriter.writerow(newListingLine)
        updatedListingsFile.close()
        newListingsFile.close()
        currentListingsFile.close()
        old_current_listings = os.path.join(self.data_path, 'Current Listings.csv')
        os.remove(old_current_listings)
        new_listings = os.path.join(self.data_path, 'Agent One-Line.csv')
        os.remove(new_listings)
        os.rename(self.data_path + "\\Updated Listings.csv", self.data_path + "\\Current Listings.csv")

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
            elem = self.driver.find_element(By.XPATH, "//img[@src='/Matrix/Images/cammulti.gif']")
        except:
            try:
                elem = self.driver.find_element(By.XPATH, "//img[@src='/Matrix/Images/cam.gif']")
            except:
                return

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
        self.month_num_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

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
            driver_path = ChromeService("WebDrivers/chromedriver.exe")
            self.driver = webdriver.Chrome(service = driver_path, options = chromeOptions)
        elif self.browser == 'Edge':
            edgeOptions = webdriver.EdgeOptions()
            edgeOptions.add_argument("--disable-infobars")
            edgeOptions.add_argument("start-maximized")
            edgeOptions.add_argument("--disable-extensions")
            edgeOptions.add_argument("--disable-notifications")
            driver_path = EdgeService("WebDrivers/msedgedriver.exe")
            self.driver = webdriver.Edge(service = driver_path, options = edgeOptions)
        elif self.browser == 'Firefox':
            firefoxOptions = Options()
            firefoxOptions.add_argument("--disable-infobars")
            firefoxOptions.add_argument("start-maximized")
            firefoxOptions.add_argument("--disable-extensions")
            firefoxOptions.add_argument("--disable-notifications")
            driver_path = FirefoxService("WebDrivers/geckodriver.exe")
            self.driver = webdriver.Firefox(service = driver_path, options = firefoxOptions)
        else:
            sys.exit("Invalid browser!")
        self.driver.minimize_window()

    def loginFB(self):
        """

        Logs in to Facebook with user's credentials.
        """
        fb_navigate = self.driver.get(self.fb_url)
        email_fill = self.try_find_element(By.ID, "email").send_keys(self.email)
        pass_fill = self.try_find_element(By.ID, "pass").send_keys(self.password)
        login_click = self.try_find_element(By.NAME, "login").click()
        # Log into Facebook
        try:
            wait = WebDriverWait(self.driver, 10).until(
                EC.title_is('Facebook')
            )
        except:
            self.driver.quit()
            sys.exit("Facebook login failed. Check credentials or connection.")

    def createListingFromMLS(self, bot, MLS_NUM, structure_type, num_beds, num_baths, price, address, description):
        """

        Creates Facebook Marketplace listing from given parameters.
        """
        self.driver.get("https://www.facebook.com/marketplace/create/rental")
        image_folder_name = bot.data_path + "\\Pictures\\" + MLS_NUM
        image_folder = os.listdir(image_folder_name)
        image_list = ""
        image_count = 0
        for i in range(len(image_folder)):
            if i == len(image_folder) - 1 or image_count == 19:
                image_list += (image_folder_name + "\\" + image_folder[i])
            else:
                image_list += (image_folder_name + "\\" + image_folder[i] + '\n')
            if image_count == 19:
                break
            else:
                image_count += 1
        photo_send = self.try_find_element(By.CSS_SELECTOR, "label:nth-child(2) > .mkhogb32").send_keys(image_list)
        sale_or_rent = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Home for Sale or Rent"]').click()
        sale_types = self.driver.find_elements(By.CSS_SELECTOR, '[aria-selected="false"]')
        sale_click = sale_types[1].click()
        property_type = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Property type"]').click()
        property_types = self.driver.find_elements(By.CSS_SELECTOR, '[aria-selected="false"]')
        if "Apartment" in structure_type:
            apartment_click = property_types[0].click()
        if "Detached" in structure_type:
            apartment_click = property_types[1].click()
        if "Townhouse" in structure_type:
            apartment_click = property_types[3].click()
        beds_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Number of bedrooms"]').send_keys(num_beds)
        baths_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Number of bathrooms"]').send_keys(num_baths)
        price_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Price"]').send_keys(price)
        address_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Property address"]').send_keys(address)
        suggestion_click = self.try_find_element(By.CSS_SELECTOR, '[aria-selected="false"]').click()
        description_enter = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Property description"]').send_keys(description)
        next_click = self.try_find_element(By.CSS_SELECTOR, '[aria-label="Next"]').click()
        time.sleep(20)
        try:
            publish_wait =  WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Publish"]'))
            )
        except:
            self.driver.quit()
            sys.exit("ERROR. Publishing on Facebook Marketplace took too long. Check listing or connection.")
        publish_wait.click()
        try:
            listing_posted_wait = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Create new listing"]'))
            )
        except:
            self.driver.quit()
            sys.exit("ERROR. Facebook posting took too long. Check the listing or connection.")

    def readFromCSV(self, mls_bot):
        data_path = mls_bot.data_path
        currentListingsFile = open(data_path + 'Current Listings.csv', 'r')
        currentListingsDict = csv.DictReader(currentListingsFile)
        for listing in currentListingsDict:

            mls_num = listing['MLS #']
            structure = str(listing['Structure Type'])
            beds = listing['Beds']
            baths = listing['Baths']
            if str(baths).isnumeric() == False:
                baths = 1
            price = listing['Current Price']
            address = str(listing['Address'] + ', ' + listing['City'] + ', VA')
            description = "If interested, please contact! \n\n" + "MLS: " + str(mls_num) + "\nAddress: " + str(address)

            if self.checkIfListed(mls_num) == False:
              self.createListingFromMLS(mls_bot, mls_num, structure, beds, baths, price, address, description)

        currentListingsFile.close()

    def checkIfListed(self, mls_num):
      self.driver.get("https://www.facebook.com/marketplace/you/selling?referral_surface=seller_hub")

      try:
        self.try_find_element(By.CSS_SELECTOR, "input[placeholder='Search your listings']").click()
        self.try_find_element(By.CSS_SELECTOR, "input[placeholder='Search your listings']").send_keys(str(mls_num))
      except:
          return False

      time.sleep(1)

      try:
        self.driver.find_element(By.XPATH, "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 ns63r2gh iv3no6db o3w64lxj b2s5l15y hnhda86s m9osqain oqcyycmt']")
        time.sleep(3)
        return False
      except:
        return True

    def deleteListings(self):

        for mls_num in remove_list:
          self.driver.get("https://www.facebook.com/marketplace/you/selling?referral_surface=seller_hub")
          self.try_find_element(By.CSS_SELECTOR, "input[placeholder='Search your listings']").click()
          self.try_find_element(By.CSS_SELECTOR, "input[placeholder='Search your listings']").send_keys(str(mls_num))
          time.sleep(1)
          self.try_find_element(By.CSS_SELECTOR, '[aria-label="More"]').click()
          self.try_find_element(By.XPATH,"//*[ text() = 'Delete Listing']").click()
          self.try_find_element(By.XPATH,"//*[ text() = 'Delete']").click()

################################################################################
######################### Execution begins below ###############################
################################################################################

# Electron input
browser_choice = sys.argv[1]
MLS_username = sys.argv[2]
MLS_pw = sys.argv[3]
MLS_choice = sys.argv[4]
FB_email = sys.argv[5]
FB_pw = sys.argv[6]
data_path = sys.argv[7]
price_range = sys.argv[8]
zip_code = sys.argv[9]
num_properties = sys.argv[10]
sys.stdout.flush()

MLS_test = MLSBot(MLS_username, MLS_pw, browser_choice, MLS_choice, data_path, price_range, zip_code, num_properties)
FB_test = MarketBot(FB_email, FB_pw, browser_choice)
MLS_test.initDriver()
FB_test.initDriver()
MLS_test.loginMLS()
FB_test.loginFB()
# BEGIN LOOP HERE
MLS_test.updateListings()
MLS_test.pullListings()
MLS_test.addNewListings()
FB_test.readFromCSV(MLS_test)
#FB_test.deleteListings()

# MLS_test = MLSBot("mobhuiyan98", "Iloverealestate4!", "Chrome", "Bright", "D:\Chris\Code\Git\mls-facebook-script", "700-800", "22152", "10")
# FB_test = MarketBot("mobhuiyan1998@yahoo.com", "Orpon1998!", "Chrome")

# MLS Test
# MLS_test = MLSBot(MLS_username, MLS_pw, browser_choice, MLS_choice, data_path, price_range, zip_code, num_properties)
# MLS_test.initDriver()
# MLS_test.loginMLS()
# MLS_test.pullListings()
# time.sleep(5000)

# MarketBot Test
# FB_test = MarketBot(FB_email, FB_pw, browser_choice)
# FB_test.initDriver()
# FB_test.loginFB()
# time.sleep(500)
# FB_test.createListingFromMLS("VAFX1160980", "Unit/Flat/Apartment", 2, 2, 339900, "12957 Centre Park Cir #206, Herndon, VA")
# time.sleep(5000)

# MLS_test = MLSBot("mobhuiyan98", "Iloverealestate4!", "Chrome", "Bright", "", "700-800", 22152, 10)
# MLS_test.initDriver()
# MLS_test.loginMLS()
# MLS_test.updateListings()
# MLS_test.pullListings()
# MLS_test.addNewListings()
