from Main_Runner import MLSBot
from Main_Runner import MarketBot
import unittest

class TestRunner(unittest.TestCase):

    def test_brightNav(self):
        """

        Tests initializing driver with predefined values and logging in to Bright.
        Reliant on stable internet and valid predefined credentials.
        """
        MLS_test = MLSBot("csosasan", "Sos@S@nchez31543", "Chrome", "Bright", "", 100, 22003, 1)
        MLS_test.initDriver()
        MLS_test.loginMLS()
        title = MLS_test.driver.title
        self.assertEqual(title, 'Dashboard | Bright MLS')

    def test_facebookNav(self):
        """

        Test initializing driver with predefined values and logging in to Facebook.
        Reliant on stable internet and valid predefined credentials.
        """
        FB_test = MarketBot("mobhuiyan1998@yahoo.com", "Orpon1998!", "Chrome")
        FB_test.initDriver()
        FB_test.loginFB()
        title = FB_test.driver.title
        self.assertEqual(title, 'Facebook')

if __name__ == '__main__':
    unittest.main()
