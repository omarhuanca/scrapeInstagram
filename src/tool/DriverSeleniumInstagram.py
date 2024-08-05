import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class DriverSeleniumInstagram:

    def __init__(self):
        option = Options()
        option.add_argument("--disable-notifications")
        option.add_argument("--disable-infobars")
        option.add_argument("--mute-audio")
        self._browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    def fbInstagramNavigation(self, email, password):
        self._browser.get("https://www.instagram.com/")
        time.sleep(5)
        self._browser.find_element(By.NAME, 'username').send_keys(email)
        time.sleep(2)
        self._browser.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(2)
        self._browser.find_element(By.XPATH, '//button[1]/div[1]').click()

    def closeExecution(self):
        self._browser.quit()

    def executeGetPage(self, url):
        try:
            self._browser.get(url)
        except NoSuchElementException:
            print("Can not be render page")

    def getBrowser(self):
        return self._browser

    def openDiv(self, post, selectorOpenDiv):
        elementLike = post.find_element(By.CSS_SELECTOR, selectorOpenDiv)
        ActionChains(self._browser).move_to_element(elementLike).perform()
        elementLike.click()

    def closeDiv(self, selectorCloseDiv):
        elementCloseDiv = self._browser.find_element(By.CSS_SELECTOR, selectorCloseDiv)
        ActionChains(self._browser).move_to_element(elementCloseDiv).perform()
        elementCloseDiv.click()

    def evaluateExpressionCssSelectorMany(self, expressionCssSelector):
        try:
            array_item = self._browser.find_elements(By.CSS_SELECTOR, expressionCssSelector)
            return array_item
        except NoSuchElementException:
            print("No Items")

    def scrollToBottomCssSelector(self, expressionCssSelector, scrollPauseItem):
        numerator = self.generateNumeratorCssSelector(expressionCssSelector)
        counter = 0
        # Get scroll height
        while numerator >= counter:
            # Scroll down to bottom
            self.scrollDownJavaScript(scrollPauseItem)
            counter = self.generateNumeratorCssSelector(expressionCssSelector)

    def generateNumeratorCssSelector(self, expressionCssSelector):
        numerator = 0
        try:
            if len(expressionCssSelector) > 0:
                numerator = len(self._browser.find_elements(By.CSS_SELECTOR, expressionCssSelector))
        except NoSuchElementException:
            print("No Details")

        return numerator

    def scrollDownJavaScript(self, scrollPauseItem):
        # Wait to load page
        time.sleep(scrollPauseItem)
        self._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
