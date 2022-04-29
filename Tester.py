
from email import message
from sqlite3 import Time
import unittest
# from unittest import suite
import Main_Runner as runner
import time
import selenium
from selenium.webdriver.common.by import By



class BotTester(unittest.TestCase):

    def setUp(self):
        self.mls_bot = runner.MLSBot("csosasan","Sos@S@nchez31543","Chrome","Bright","","400-600","20154",5)
        self.fb_bot = runner.MarketBot("mobhuiyan1998@yahoo.com", "Orpon1998!","Chrome")

        self.mls_bot.initDriver()
        self.fb_bot.initDriver() 

    def tearDown(self): 
        self.fb_bot.driver.close()
        self.mls_bot.driver.close()

    def testBrightLogin(self): 
        message = "Bright Login Failed, Dashboard not Detected"
        self.mls_bot.loginMLS() 
        time.sleep(2)

        self.assertEqual(self.mls_bot.driver.current_url,"https://www.brightmls.com/dashboard", message) 

    def testFacebookLogin(self):
        message = "Facebook Login Failed, Dashboard not Detected"
        self.fb_bot.loginFB()
        time.sleep(3)

        try: 
            self.fb_bot.driver.find_element(By.XPATH,"//*[name()='path' and contains(@class,'p361ku9c')]")
        except Exception:
            self.fail("Facebook Login Failed")
    

if __name__ == '__main__':
    unittest.main()



