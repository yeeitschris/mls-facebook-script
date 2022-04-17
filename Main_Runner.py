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

class MLSBot:
    def __init__(self, username, password, browser, site_id, data_path):
        self.username = username
        self.password = password
        self.browser = browser
        self.site_id = site_id
        self.data_path = data_path
        if not self.data_path:
            self.data_path = ""

    def try_find_element(self, type, target):
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((type, target))
        )
        if elem is None:
            self.driver.quit()
            sys.exit("ERROR. Element couldn't be found. Check credentials, website, and connection.")
        return elem

    def initDriver(self):
        if self.data_path == "":
            self.data_path = os.getcwd() + "\\Data\\"
        else:
            self.data_path = self.data_path + "\\Data\\"
        prefs = {"download.default_directory" : self.data_path}
        if self.browser == 'Chrome':
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(options = chromeOptions, executable_path = "WebDrivers/chromedriver.exe")
        elif self.browser == 'Edge':
            # self.driver = webdriver.Edge("WebDrivers/msedgedriver.exe")
            edgeOptions = webdriver.EdgeOptions()
            edgeOptions.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Edge(options = edgeOptions, executable_path = "WebDrivers/msedgedriver.exe")
        elif self.browser == 'Firefox':
            # self.driver = webdriver.Firefox("WebDrivers/geckodriver.exe")
            firefoxOptions = Options()
            firefoxOptions.set_preference("browser.download.folderList", 2)
            firefoxOptions.set_preference("browser.download.dir", self.data_path)
            self.driver = webdriver.Firefox(options = firefoxOptions, executable_path = "WebDrivers/geckodriver.exe")
        else:
            sys.exit("Invalid browser!")

    def loginMLS(self):
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

    def GetListings(self):
        if self.site_id == 'Bright':
            old_file = os.path.join(self.data_path, 'Agent One-Line.csv')
            if os.path.exists(old_file):
                os.remove(old_file)

            search = self.driver.get("https://matrix.brightmls.com/Matrix/Search/ResidentialSale/Residential")

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

    def replacer(s, newstring, index, nofail=False):
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

    def img_downloader(image_url, MLS_NUM, imgcount,path):

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







#profile = webdriver.FirefoxProfile()
#profile.set_preference("browser.download.folderList", 2)
#profile.set_preference("browser.download.manager.showWhenStarting", False)
#profile.set_preference("browser.download.dir", "C:/Users/Chris/Desktop")
#profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

    def addListing(MLS_NUM):
        pullListingImg(MLS_NUM)


    def pullListingImg(MLS_NUM):
        image_dir = self.data_path + '\\Current Listings\\'

        elem = driver.find_element_by_xpath("//input[@id='ctl01_m_ucSpeedBar_m_tbSpeedBar']")
        elem.clear()
        elem.send_keys(MLS_NUM)
        elem.send_keys(Keys.RETURN)

        time.sleep(2)

        content = driver.find_element_by_xpath("//a[normalize-space()='VAFX2048786']")

        content.click()

        time.sleep(1)

        elem = driver.find_element_by_xpath("//img[@src='/Matrix/Images/cammulti.gif']")

        elem.click()


        elem = driver.find_element_by_xpath("//*[contains(@src,'Type=1&Size=4&')]")


        img_url = str(elem.get_attribute('src'))


        elem = driver.find_element_by_css_selector("td[class='d115m5'] span[class='formula field NoPrint']")

        img_count = str(elem.text).replace('(','')
        img_count = img_count.replace(')','')
        print(img_count)



        img_url = replacer(img_url,'',len(str(img_url)) - 1)


        #create new directory for new listing
        path = os.path.join(image_dir,MLS_NUM)

        #check if path exists
        if os.path.isdir(path) != True:
            os.mkdir(path)
        #Download the image
        for x in range (int(img_count)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            img_downloader(img_url + str(x),MLS_NUM, str(x),path)

#go in to zillow
#check existing listings

#or go into bright
#pull image data
#figure out how to get all the image links
#download them, store them, upload them, then delete
#add error checking
#build a case for only one picture or no pictures




#find all the listings in the given zip code of new listings
#find store the information
#check if listing is already on facebook



#add new listing function
#remove listing function


#bed = ""
#bath = ""
#price = ""
#address = ""
#sqft ==




# <<<<<<< HEAD
#check with the current csv for any changes
    def checkListings(self):
        new_file = os.path.join(self.data_path, 'Current Listings.csv')
        if not os.path.exists(new_file):
            file = open(self.data_path + 'Current Listings.csv', 'w+')
            file.close()
        newList = csv.DictReader(open('Data/Agent One-Line.csv', 'r'))
        # Add code to create/overwrite current listings
        curList = csv.DictReader(open('Data/Current Listings.csv','r'))

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
    def __init__(self, email, password, browser):
        self.email = email
        self.password = password
        self.browser = browser
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
MLS_test.GetListings()

# MarketBot Test
FB_test = MarketBot(FB_email, FB_pw, browser_choice)
FB_test.initDriver()
FB_test.loginFB()
time.sleep(5)
FB_test.createListingFromMLS("Unit/Flat/Apartment", 2, 2, 339900, "12957 Centre Park Cir #206, Herndon, VA")
time.sleep(5000)
