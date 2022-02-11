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



def img_downloader(image_url):
    
## Set up the image URL and filename
    filename = "Listing "

# Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

# Check if the image was retrieved successfully
    if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
    
    # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ',filename)
        return 1
    else:
        print('Image Couldn\'t be retreived')
        return 0 









driver = webdriver.Firefox(executable_path='C:/Users/jeral/Downloads/geckodriver-v0.30.0-win64/geckodriver.exe')


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
elem.send_keys("Iloverealestate3!")

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




#This temporrary for only one listings 
#need to pull the mls number from the export
# and punch it in the xpath 

elem = driver.find_element_by_xpath("//input[@id='ctl01_m_ucSpeedBar_m_tbSpeedBar']")
elem.clear()
elem.send_keys("VAFX2048786")
elem.send_keys(Keys.RETURN)

time.sleep(2)

content = driver.find_element_by_xpath("//a[normalize-space()='VAFX2048786']")

content.click()

time.sleep(1)

elem = driver.find_element_by_xpath("//img[@src='/Matrix/Images/cammulti.gif']")

elem.click()


elem = driver.find_element_by_xpath("//*[contains(@src,'Type=1&Size=4&')]")
#elem = driver.find_element_by_xpath("//*[contains(@src,'https://matrixmedia.brightmls.com/mediaserver/GetMedia.ashx?')]")


img_url = str(elem.get_attribute('src'))


elem = driver.find_element_by_xpath("//div[@class='count']")
print(elem   )


print(img_url)



img_url = replacer(img_url,'0',len(str(img_url)) - 1)

img_count = 0

while(img_downloader(img_url) == 1):
    img_count += 1 
    img_url = replacer(img_url,str(img_count),len(str(img_url)) - 1)
    print(img_url)







print("\n")
print(replace_string)

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



#def pullHTML(): 

#def doesListingExist():

#def pullListing() 









