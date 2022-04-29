from Main_Runner import MLSBot
from Main_Runner import MarketBot
import unittest

class TestRunner(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
