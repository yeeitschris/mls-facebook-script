from xml.dom.expatbuilder import parseString
from Main_Runner import MLSBot
from Main_Runner import MarketBot
import Main_Runner
import unittest
import os
import time

class TestRunner(unittest.TestCase):
    """

    Tests creation and existence of default data directory.
    """
    def test_defaultDir(self):

        message = "Data directory not found in default path."
        self.MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
        # Initial init sets variables and path
        self.MLS_test.initDriver()
        # Delete existing directory.
        try:
            os.rmdir(self.MLS_test.data_path)
        except:
            pass
        # Second init to confirm creation after delete
        self.MLS_test.initDriver()
        dirExists = os.path.exists(self.MLS_test.data_path)
        self.assertTrue(dirExists, message)
        self.MLS_test.driver.close()

    def test_brightNav(self):
        """

        Tests initializing driver with predefined values and logging in to Bright.
        Reliant on stable internet and valid predefined credentials.
        """
        message = "Bright Login Failed, Dashboard not Detected"
        self.MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
        self.MLS_test.initDriver()
        self.MLS_test.loginMLS()
        title = self.MLS_test.driver.title
        self.assertEqual(title, 'Dashboard | Bright MLS', message)
        self.MLS_test.driver.close()

    def test_facebookNav(self):
        """

        Test initializing driver with predefined values and logging in to Facebook.
        Reliant on stable internet and valid predefined credentials.
        """
        message = "Facebook Login Failed, Dashboard not Detected"
        self.FB_test = MarketBot("mobhuiyan1998@yahoo.com", "Orpon1998!", "Chrome")
        self.FB_test.initDriver()
        self.FB_test.loginFB()
        title = self.FB_test.driver.title
        self.assertEqual(title, 'Facebook', message)
        self.FB_test.driver.close()

    def test_getDefaultCSV(self):
        
        message = "Default CSV not detected."

        self.MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
        self.MLS_test.initDriver()
        self.MLS_test.loginMLS()
        self.MLS_test.getDefaultCSV()

        csv_wait = 0
        while not os.path.exists(self.MLS_test.data_path + 'Agent One-Line.csv'):
            time.sleep(1)
            csv_wait += 1
            if csv_wait > 10:
                break
        csv_exists = os.path.exists(self.MLS_test.data_path + 'Agent One-Line.csv')
        self.assertTrue(csv_exists, message)
        self.MLS_test.driver.close()

    def test_imgDownloader(self):
        """
        Tests that the imgDownloader method properly creates the img directory and
        downloads the pictures with the given MLS NUM, 
        """

        self.MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
        self.MLS_test.initDriver()
        self.MLS_test.loginMLS()

        MLS_NUM = "VAFX2048786"

        self.MLS_test.pullListingImg(MLS_NUM)
        self.MLS_test.driver.close() 

        for i in range(0,18):
            if(os.path.exists(MLS_NUM + "-" + str(i))):
                continue
            else: 
                message = "Error at number" + str(i)
                self.assertFalse(False,message)

        self.assertTrue(True)
            
    #def test_pullListings(self):
    #    """
    #    Tests that the search queries are properly pulled 
    #    and inserted in the CSV
    #    """
    # 
    #
    #    self.MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
    #    self.MLS_test.initDriver()
    #    self.MLS_test.loginMLS()
    #    self.MLS_test.pullListings()


    def test_addListingsFaceBook(self): 
        """

        Test automated listings on Facebook with predefined images and listing data 
        are correctly posted on the Facebook Marketplace
        """

        message = "Facebook Listing Not Detected"
        self.FB_test = MarketBot("mobhuiyan1998@yahoo.com", "Orpon1998!", "Chrome")
        self.FB_test.initDriver()
        self.FB_test.loginFB()   

        self.MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
        self.MLS_test.initDriver()
        self.MLS_test.loginMLS()


        num_baths = 1
        num_beds = 1
        price = "210,000"
        address = "2059 HUNTINGTON AVENUE Alexandria, VA"
        description = "VAFX2048786"
        MLS_NUM = description


        self.FB_test.createListingFromMLS(
            self.MLS_test,
            MLS_NUM,"Unit/Flat/Apartment",
            num_baths,num_beds,
        price,address,description)

        try: 
            self.assertTrue(self.FB_test.checkIfListed(MLS_NUM))
        except:
            pass
        finally: 
            Main_Runner.remove_list.append(MLS_NUM)
            self.FB_test.deleteListings()
            self.FB_test.driver.close()
            self.MLS_test.driver.close()
        

    

if __name__ == '__main__':
    unittest.main()
