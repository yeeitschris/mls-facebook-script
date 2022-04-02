from MarketBot import FB

print("This is a test file for Facebook Marketplace login.")
email = input("Enter your Facebook email: ")
pw = input("Enter your Facebook password: ")
driver = input("Enter the path of your browser's web driver: ")
test = FB(email, pw, driver)
test.login()
test.marketplace()
