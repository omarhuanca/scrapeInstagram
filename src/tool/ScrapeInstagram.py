import configparser
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import re

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from time import sleep
from src.business.account.BasicAccount import BasicAccount
from src.business.account.UserLike import UserLike


class ScrapeInstagram:

    def __init__(self, location, filename, driverSelenium):
        basePath = Path(__file__).parent
        self._filePath = (basePath / os.path.join(location, filename)).resolve()
        self._driverSelenium = driverSelenium

    def readConfigPath(self):
        configObj = configparser.ConfigParser()
        configObj.read(self._filePath)
        return BasicAccount(configObj.get('credentials', 'email'), configObj.get('credentials', 'password'))

    def instagramLogin(self, basicAccount):
        print("Opening browser...")
        email = basicAccount.getEmail()
        password = basicAccount.getPassword()
        self._driverSelenium.fbInstagramNavigation(email, password)

    def findElement(self, item, selectorName):
        flag = False
        try:
            item.find_element(By.CSS_SELECTOR, selectorName)
            return not flag
        except Exception:
            sys.stdout.write("")
            pass

        return flag

    def filterString(self, regex, potentialString):
        splitResponse = ''
        if len(potentialString) > 0 and len(regex) > 0:
            regexString = re.search(regex, potentialString)
            if regexString is not None:
                splitString = potentialString[:regexString.start()] + potentialString[regexString.end():]
                splitResponse = splitString[regexString.end() + 1 - (regexString.end() - regexString.start()):]

        return splitResponse

    def changeValueString(self, potentialString):
        if "=" in potentialString:
            potentialString = ''
        return potentialString

    def getLikeFromPage(self, prefix, page):
        selectorOpenDiv = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xr1yuqi xkrivgy x4ii5y1 x1gryazu x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf x1a02dak xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"] > span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
        selectorCloseDiv = 'div[class="x6s0dn4 x78zum5 x19l4sor x1c4vz4f x2lah0s xl56j7k"] > div[class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"]'
        selectorLink = 'div[class="x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1pi30zi x1swvt13 xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x9f619 x1n2onr6 x1ja2u2z x1qjc9v5 x78zum5 xdt5ytf x1iyjqo2 xl56j7k xeuugli"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli x1iyjqo2"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x1rg5ohu"] > div > a'
        selectorContainerDiv = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x6ikm8r x10wlt62 x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div > div'
        selectorAmount = 'span[class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"] > span[class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"]'

        os.chdir("./data/out")
        if len(page) > 0 and len(prefix) > 0:
            arrayUserLike = []
            self._driverSelenium.executeGetPage(url=f"{page}")
            if self.findElement(self._driverSelenium.getBrowser(), selectorOpenDiv):
                sleep(5)
                self._driverSelenium.openDiv(self._driverSelenium.getBrowser(), selectorOpenDiv)
                sleep(10)

            amount = self._driverSelenium.getBrowser().find_element(By.CSS_SELECTOR, selectorAmount)
            print("---------------------------------")
            print(amount.text)
            print("---------------------------------")

            counter = 0
            # divisor = int(amount.text) // 11
            divisor = 16
            try:
                while counter < divisor:
                    counter = counter + 1

                    listLink = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorLink)
                    sleep(0.5)

                    for link in listLink:
                        sleep(0.5)
                        userPublication = UserLike(link.text, link.get_attribute("href"))
                        arrayUserLike.append(userPublication)
                        sleep(0.5)
                        link.send_keys(Keys.PAGE_DOWN)
                        sleep(1)

            except Exception as e:
                print(e)

            if self.findElement(self._driverSelenium.getBrowser(), selectorCloseDiv):
                self._driverSelenium.closeDiv(selectorCloseDiv)
                sleep(5)

            if len(arrayUserLike) > 0:
                csvOut = prefix + "user_publication_like_%s.csv" % datetime.now().strftime(
                    "%Y_%m_%d_%H%M")
                writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
                writer.writerow(['url_publication', 'B_name', 'B_profile'])

                for userLike in arrayUserLike:
                    writer.writerow([page, userLike.getName(), userLike.getProfile()])
                    print(userLike.getName())
                    print(userLike.getProfile())

    def generateNavigationProfile(self, prefix, page, numberIteration):
        selectorPublication = 'div[class="_ac7v xras4av xgc1b0m xat24cr xzboxd6"] > div[class="x1lliihq x1n2onr6 xh8yej3 x4gyw5p xfllauq xo2y696 x11i5rnm x2pgyrj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
        os.chdir("./data/out")
        if len(page) > 0 and len(prefix) > 0:
            self._driverSelenium.executeGetPage(url=f"{page}")
            sleep(10)

            counter = 0
            while counter <= int(numberIteration):
                counter = counter + 1
                self._driverSelenium.scrollToBottomCssSelector(selectorPublication, 1)
                sleep(10)

                if self.findElement(self._driverSelenium.getBrowser(), selectorPublication):
                    sleep(10)
                    listPublication = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorPublication)
                    sleep(10)

                for publication in listPublication:
                    print(publication.get_attribute("href"))
