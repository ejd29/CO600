import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AnalyseButton(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def check_title(self):
        driver = self.driver
        driver.get("C:/Users/USER/Desktop/CO600/PCopy/Website/index.html")
        self.assertIn("Terms and Conditions Analyser", driver.title)

    def test_buttons(self):
        driver = self.driver
        driver.get("C:/Users/USER/Desktop/CO600/PCopy/Website/index.html")

        topButton = driver.find_element_by_id("ab0")
        topButton.click()

        aboutButton = driver.find_element_by_id("ab1")
        aboutButton.click()

        txtArea = driver.find_element_by_id("termsandconditions")
        txtArea.send_keys("When you upload, submit, store, send or receive content to or through our Services, you give Google (and those we work with) a worldwide license to use, host, store, reproduce, modify, create derivative works (such as those resulting from translations, adaptations or other changes we make so that your content works better with our Services), communicate, publish, publicly perform, publicly display and distribute such content. The rights you grant in this license are for the limited purpose of operating, promoting, and improving our Services, and to develop new ones. This license continues even if you stop using our Services (for example, for a business listing you have added to Google Maps). Some Services may offer you ways to access and remove content that has been provided to that Service. Also, in some of our Services, there are terms or settings that narrow the scope of our use of the content submitted in those Services. Make sure you have the necessary rights to grant us this license for any content that you submit to our Services.Our automated systems analyze your content (including emails) to provide you personally relevant product features, such as customized search results, tailored advertising, and spam and malware detection. This analysis occurs as the content is sent, received, and when it is stored.")

        clearButton = driver.find_element_by_id("clearBtn")
        clearButton.click()

        analyseBtn = driver.find_element_by_id("analyseB")
        analyseBtn.click()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
