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
print("This is a test for MLS integration.")
test = MLSBot()
test.initDriver()
test.loginMLS()
time.sleep(5000)

# MarketBot Test
# print("This is a test for Facebook Marketplace login.")
# test = FB()
# test.launchBrowser()
# test.login()
# time.sleep(5000)
