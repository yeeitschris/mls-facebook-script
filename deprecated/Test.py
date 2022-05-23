from MarketBot import FB
from Main_Runner import MLSBot
import time

# Test email: johnrealtormls@gmail.com
# Test PW: iloverealty!

# Bright username: mobhuiyan98
# Bright PW: Iloverealestate4!

# Chrome Webdriver path: chromedriver_win32/chromedriver.exe
# Downloads path: D:\Chris\Downloads

# MLS Test
# print("This is a test for MLS integration.")
# test = MLSBot()
# test.initDriver()
# test.loginMLS()
# test.GetListings()

# MarketBot Test
print("This is a test for Facebook Marketplace login.")
test = FB()
test.initDriver()
test.loginFB()
time.sleep(5)
test.createListingFromMLS("Unit/Flat/Apartment", 2, 2, 339900, "12957 Centre Park Cir #206, Herndon, VA")
time.sleep(5000)
