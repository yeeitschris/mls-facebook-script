
import unittest
# from unittest import suite
import Main_Runner as runner


class BotTester(unittest.TestCase):

    def setUp(self):
        self.mls_bot = runner.MLSBot("csosasan","Sos@S@nchez31543","Chrome","Bright","","400-600","20154",5)
       # self.fb_bot = runner.MarketBot("mobhuiyan1998@yahoo.com", "Orpon1998!","Chrome")

        self.mls_bot.initDriver()
        self.fb_bot.initDriver() 

    def tearDown(self): 
        self.fb_bot.driver.close()
        self.mls_bot.driver.close()


    def brightLoginTest(self): 
        message = "Bright Login Failed, Dashboard not Detected"
        #self.mls_bot.loginMLS() 
        self.assertEqual(self.mls_bot.driver.current_url,"https://www.brightmls.com/dashboard", message) 

    def facebookLoginTest(self):
        message = "Facebook Logif Failed, Dashboard not Detected"
        #self.fb_bot.loginFB()
        self.assertEqual(self.mls_bot.driver.current_url,"https://www.facebook.com", message)  
   


if __name__ == '__main__':
    unittest.main()




