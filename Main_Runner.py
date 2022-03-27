from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time 
import requests 
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.keys import Keys
from urllib.request import Request, urlopen
import shutil
import csv 
import os









parent_dir = "C:/Users/jeral/Desktop/Current Listings"







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







profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", "C:/Users/jeral/Desktop/Current Listings")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

driver = webdriver.Firefox(profile,executable_path='C:/Users/jeral/Downloads/geckodriver-v0.30.0-win64/geckodriver.exe')

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


driver.get("https://login.brightmls.com/login")
time.sleep(5)

elem = driver.find_element_by_name("username")
elem.send_keys("mobhuiyan98")

elem = driver.find_element_by_id("password")
elem.send_keys("Iloverealestate4!")

time.sleep(5)

elem = driver.find_element_by_class_name("MuiButton-label")
elem.click()

time.sleep(5)

driver.get("https://matrix.brightmls.com/Matrix/Search/ResidentialSale/Residential")

time.sleep(5)
elem = driver.find_element_by_css_selector("option[title='VA']")
elem.click()

time.sleep(5)

elem = driver.find_element_by_css_selector("#m_ucSearchButtons_m_clblCount")
elem.click()

time.sleep(5)

elem = driver.find_element_by_css_selector(".linkIcon.icon_search")
elem.click() 

time.sleep(5)



##get csv
elem = driver.find_element_by_xpath("//a[@id='m_lnkCheckAllLink']")
elem.click()

elem = driver.find_element_by_css_selector(".linkIcon.icon_export")
elem.click()

elem = driver.find_element_by_css_selector("#m_btnExport")
elem.click()




#check with the current csv for any changes
newList = open('C:/Users/jeral/Downloads/Agent One-Line.csv')
curList = open('C:/Users/jeral/Desktop/Current Listings/Current Listing.csv') 

#if there is new listing 
#create a new listing 

#if listing no longer exists 
#remove the listing and remove it from the list





#modify the csv 


#if the csv has changed 
    #pull the MLS NUMBER    
    #execute changes in facebook











#This temporrary for only one listings 
#need to pull the mls number from the export
# and punch it in the xpath 

#MLS_NUM = "VAFX2048786"

#elem = driver.find_element_by_xpath("//input[@id='ctl01_m_ucSpeedBar_m_tbSpeedBar']")
#elem.clear()
#elem.send_keys("VAFX2048786")
#elem.send_keys(Keys.RETURN)

#time.sleep(2)

#content = driver.find_element_by_xpath("//a[normalize-space()='VAFX2048786']")

#content.click()

#time.sleep(1)

#elem = driver.find_element_by_xpath("//img[@src='/Matrix/Images/cammulti.gif']")

#elem.click()


#elem = driver.find_element_by_xpath("//*[contains(@src,'Type=1&Size=4&')]")


#img_url = str(elem.get_attribute('src'))


#elem = driver.find_element_by_css_selector("td[class='d115m5'] span[class='formula field NoPrint']")

#img_count = str(elem.text).replace('(','')
#img_count = img_count.replace(')','') 
#print(img_count)



#img_url = replacer(img_url,'',len(str(img_url)) - 1)


#create new directory for new listing 
#path = os.path.join(parent_dir,MLS_NUM)

#check if path exists
#if os.path.isdir(path) != True: 
#    os.mkdir(path)

#for x in range (int(img_count)): 
 #   os.makedirs(os.path.dirname(path), exist_ok=True)
  #  img_downloader(img_url + str(x),MLS_NUM, str(x),path)




#### print(img_url)



#driver.close()
#print("Driver has successfully closed")


#print("\n")
#print(replace_string)

#for x in range(len(elem)):
#    print(elem[x].get_attribute('src'))




######            print("Oops!  That was no valid number.  Try again...")



    

##HTML PARSER





#driver.get("http://www.facebook.com")
#print(driver.title)
#assert "Facebook" in driver.title
#elem = driver.find_element_by_name("email")
#elem.clear()
#elem.send_keys("mobhuiyan1998@yahoo.com")

#elem = driver.find_element_by_name("pass")
#elem.send_keys("Orpon1998!")

#elem = driver.find_element_by_name("login")
#elem.click()


#driver.get("https://www.facebook.com/marketplace/create/rental")


#assert "No results found." not in driver.page_source





#def brightLaunch():

#def facebookLaunch(): 


#def checkListings(): 


#def updateListings(): 

#def getElement():


#def doesListingExist():

#def pullListing():
    









