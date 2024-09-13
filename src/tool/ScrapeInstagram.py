import configparser
import csv
import os
import sys
import re
from datetime import datetime
from pathlib import Path

from selenium.webdriver.common.by import By
from time import sleep
from src.business.account.BasicAccount import BasicAccount
from src.business.account.PotentialContact import PotentialContact
from src.business.account.ProfileName import ProfileName
from src.business.account.PublicationComment import PublicationComment
from src.business.account.PublicationUser import PublicationUser
from src.business.account.UserComment import UserComment
from src.business.account.UserLike import UserLike
from selenium.webdriver import ActionChains, Keys

from src.business.person.Person import Person
from src.business.publication.PublicationContact import PublicationContact


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

    def loadGeneralCsv(self, filename):
        arrayFriend = []
        with open(filename, 'rt', encoding="utf-8") as inputCsv:
            reader = csv.DictReader(inputCsv)
            for idx, row in enumerate(reader):
                arrayFriend.append({
                    "name": row['B_name'],
                    "profile": row['B_profile'],
                    "username": self.getProfileFromUrl(row['B_profile'])
                })
        print("%d friends in imported list" % (idx + 1))
        return arrayFriend

    def getLikeFromPublication(self, prefix, urlPublication, username):
        selectorOpenDiv = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xr1yuqi xkrivgy x4ii5y1 x1gryazu x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf x1a02dak xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"] > span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
        selectorCloseDiv = 'div[class="x6s0dn4 x78zum5 x19l4sor x1c4vz4f x2lah0s xl56j7k"] > div[class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"]'
        selectorDiv = 'div[class="x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1pi30zi x1swvt13 xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x9f619 x1n2onr6 x1ja2u2z x1qjc9v5 x78zum5 xdt5ytf x1iyjqo2 xl56j7k xeuugli"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli x1iyjqo2"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"]'
        selectorDivLink = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x1rg5ohu"] > div > a'
        selectorDivSpan = 'span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj"] > span'

        os.chdir("./data/out")
        if len(urlPublication) > 0 and len(prefix) > 0:
            arrayPublicationUser = []
            self._driverSelenium.executeGetPage(url=f"{urlPublication}")

            self.getUserDivLikePublication(urlPublication, arrayPublicationUser, selectorCloseDiv, selectorDiv,
                                           selectorOpenDiv, username, selectorDivLink, selectorDivSpan)

            if len(arrayPublicationUser) > 0:
                csvOut = prefix + "user_publication_like_%s.csv" % datetime.now().strftime(
                    "%Y_%m_%d_%H%M")
                writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
                writer.writerow(['username', 'url_publish', 'B_name', 'B_profile'])

                for publicationUser in arrayPublicationUser:
                    writer.writerow([publicationUser.getUsername(), publicationUser.getUrlPublication(),
                                     publicationUser.getUserLike().getName(),
                                     publicationUser.getUserLike().getProfile()])

    def getUserDivLikePublication(self, urlPublication, arrayPublicationUser, selectorCloseDiv, selectorDiv,
                                  selectorOpenDiv, username, selectorDivLink, selectorDivSpan):
        counter = 0
        divisor = 16
        try:
            if self.findElement(self._driverSelenium.getBrowser(), selectorOpenDiv):
                sleep(5)
                self._driverSelenium.openDiv(self._driverSelenium.getBrowser(), selectorOpenDiv)
                sleep(10)

            while counter < divisor:
                counter = counter + 1

                listDiv = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorDiv)
                sleep(0.5)

                for itemDiv in listDiv:
                    item = itemDiv.find_element(By.CSS_SELECTOR, selectorDivLink)
                    itemName = itemDiv.find_element(By.CSS_SELECTOR, selectorDivSpan)
                    sleep(0.5)
                    userLike = UserLike(itemName.text, item.get_attribute("href"))
                    publicationUser = PublicationUser(username, urlPublication, userLike)
                    arrayPublicationUser.append(publicationUser)
                    sleep(0.5)
                    item.send_keys(Keys.PAGE_DOWN)
                    # sleep(1)
                    sleep(5)

            if self.findElement(self._driverSelenium.getBrowser(), selectorCloseDiv):
                self._driverSelenium.closeDiv(selectorCloseDiv)
                sleep(5)
        except Exception as e:
            print(e)

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

    def generateLikeFromListPublication(self, prefix, pageProfile, numberIteration):
        selectorPublication = 'div[class="_ac7v xras4av xgc1b0m xat24cr xzboxd6"] > div[class="x1lliihq x1n2onr6 xh8yej3 x4gyw5p xfllauq xo2y696 x11i5rnm x2pgyrj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
        selectorClosePublication = 'div[class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"] > div[class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"]'
        selectorOpenDiv = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xr1yuqi xkrivgy x4ii5y1 x1gryazu x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf x1a02dak xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"] > span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
        selectorCloseDiv = 'div[class="x6s0dn4 x78zum5 x19l4sor x1c4vz4f x2lah0s xl56j7k"] > div[class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"]'
        selectorDiv = 'div[class="x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1pi30zi x1swvt13 xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x9f619 x1n2onr6 x1ja2u2z x1qjc9v5 x78zum5 xdt5ytf x1iyjqo2 xl56j7k xeuugli"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli x1iyjqo2"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"]'
        selectorDivLink = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x1rg5ohu"] > div > a'
        selectorDivSpan = 'span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj"] > span'

        os.chdir("./data/out")
        if len(pageProfile) > 0 and len(prefix) > 0:
            self._driverSelenium.executeGetPage(url=f"{pageProfile}")
            sleep(5)
            arrayPublicationUser = []

            try:
                username = self.getProfileFromUrl(pageProfile)
                counter = 0
                while counter <= numberIteration:
                    counter = counter + 1
                    self._driverSelenium.scrollToBottomCssSelector(selectorPublication, 1)
                    sleep(10)

                if self.findElement(self._driverSelenium.getBrowser(), selectorPublication):
                    sleep(5)
                    listPublication = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorPublication)
                    sleep(5)

                    for publication in listPublication:
                        self._driverSelenium.executeElementClick(publication)
                        sleep(10)

                        self.getUserDivLikePublication(publication.get_attribute("href"), arrayPublicationUser,
                                                       selectorCloseDiv, selectorDiv, selectorOpenDiv, username,
                                                       selectorDivLink,
                                                       selectorDivSpan)
                        sleep(10)

                        self._driverSelenium.closeDiv(selectorClosePublication)
                        sleep(10)

            except Exception as e:
                print(e)

            csvOut = prefix + "publication_like_%s.csv" % datetime.now().strftime(
                "%Y_%m_%d_%H%M")
            writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
            writer.writerow(['username', 'publication', 'B_name', 'B_profile'])

            for publicationUser in arrayPublicationUser:
                writer.writerow([publicationUser.getUsername(), publicationUser.getUrlPublication(),
                                 publicationUser.getUserLike().getName(),
                                 publicationUser.getUserLike().getProfile()])

    def getCommentFromPublication(self, prefix, urlPublication, username):
        selectorBlockComment = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]'
        selectorLinkUser = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"] > span[class="xt0psk2"] > div > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd"]'
        selectorComment = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"] > span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]'

        os.chdir("./data/out")
        if len(urlPublication) > 0 and len(prefix) > 0:
            self._driverSelenium.executeGetPage(url=f"{urlPublication}")
            arrayPublicationComment = []

            self.getCommentPublication(arrayPublicationComment, selectorBlockComment, selectorComment, selectorLinkUser,
                                       urlPublication, username)

            csvOut = prefix + "user_comment_%s.csv" % datetime.now().strftime(
                "%Y_%m_%d_%H%M")
            writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
            writer.writerow(['publication', 'B_name', 'B_comment'])

            for publicationComment in arrayPublicationComment:
                writer.writerow(
                    [publicationComment.getUrlPublication(), publicationComment.getUserComment().getUrlUsername(),
                     publicationComment.getUserComment().getComment()])

    def getCommentPublication(self, arrayPublicationComment, selectorBlockComment, selectorComment, selectorLinkUser,
                              urlPublication, username):
        try:
            listBlockComment = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorBlockComment)
            print("urlPublication")
            print(urlPublication)
            for blockComment in listBlockComment:
                if self.findElement(blockComment, selectorLinkUser):
                    linkUser = blockComment.find_element(By.CSS_SELECTOR, selectorLinkUser)
                    commentUser = blockComment.find_element(By.CSS_SELECTOR, selectorComment)
                    userComment = UserComment(linkUser.get_attribute("href"), commentUser.text)
                    publicationComment = PublicationComment(username, urlPublication, userComment)
                    print("linkUser.get_attribute")
                    print(linkUser.get_attribute("href"))
                    print(commentUser.text)
                    arrayPublicationComment.append(publicationComment)
                    sleep(5)
        except Exception as e:
            print(e)

    def getProfileFromUrl(self, urlProfile):
        uniqueIdentifier = ""
        profile = self.filterString(r"com{1}", urlProfile)
        if "=" in profile:
            username = self.filterString(r"[?]", profile)
        else:
            username = profile

        if len(username) > 0:

            stringDot = self.filterString(r"[0-9]+", username)
            number = self.filterString(r"[a-z\\.]+", username)

            username = self.changeValueString(username)
            stringDot = self.changeValueString(stringDot)

            if len(username) > len(stringDot):
                if len(username) > len(number):
                    uniqueIdentifier = username
            elif len(stringDot) > len(number):
                uniqueIdentifier = stringDot
            elif len(number) > len(username):
                uniqueIdentifier = number

        return uniqueIdentifier

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

    def getCommentFromListPublication(self, prefix, page, username):
        selectorPublication = 'div[class="_ac7v xras4av xgc1b0m xat24cr xzboxd6"] > div[class="x1lliihq x1n2onr6 xh8yej3 x4gyw5p xfllauq xo2y696 x11i5rnm x2pgyrj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
        selectorClosePublication = 'div[class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"] > div[class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"]'

        selectorBlockComment = 'div[class="x1qjc9v5 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xk390pu xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xggy1nq x11njtxf"] > li[class="_a9zj _a9zl"] > div[class="_a9zm"] > div[class=" _a9zo"] > div[class="_a9zr"]'
        selectorLinkUser = 'h3[class="_a9zc"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xw3qccf x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > span[class="xt0psk2"] > div > a[class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83"]'
        selectorComment = 'div[class="_a9zs"] > span[class="_ap3a _aaco _aacu _aacx _aad7 _aade"]'

        os.chdir("./data/out")
        if len(page) > 0 and len(prefix) > 0:
            self._driverSelenium.executeGetPage(url=f"{page}")
            sleep(5)
            arrayPublicationComment = []
            self.getCommentPublicationFromProfile(arrayPublicationComment, username, selectorBlockComment,
                                                  selectorClosePublication, selectorComment, selectorLinkUser,
                                                  selectorPublication)

            if 0 < len(arrayPublicationComment):
                csvOut = prefix + "publication_comment_%s.csv" % datetime.now().strftime(
                    "%Y_%m_%d_%H%M")
                writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
                writer.writerow(['url_publication', 'B_name', 'B_comment'])

            for publicationComment in arrayPublicationComment:
                writer.writerow(
                    [publicationComment.getUrlPublication(), publicationComment.getUserComment().getUrlUsername(),
                     publicationComment.getUserComment().getComment()])

    def getCommentPublicationFromProfile(self, arrayPublicationComment, username, selectorBlockComment,
                                         selectorClosePublication, selectorComment, selectorLinkUser,
                                         selectorPublication):
        try:
            if self.findElement(self._driverSelenium.getBrowser(), selectorPublication):
                listPublication = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorPublication)
                sleep(5)

                for publication in listPublication:
                    self._driverSelenium.executeElementClick(publication)
                    sleep(10)

                    listBlockComment = self._driverSelenium.evaluateExpressionCssSelectorMany(
                        selectorBlockComment)
                    print("urlPublication")
                    print(publication.get_attribute("href"))
                    for blockComment in listBlockComment:
                        linkUserContent = ''
                        commentUserContent = ''

                        sleep(5)

                        if self.findElement(blockComment, selectorLinkUser):
                            linkUser = blockComment.find_element(By.CSS_SELECTOR, selectorLinkUser)
                            if linkUser.get_attribute("href") is not None:
                                print("linkUser.get_attribute")
                                print(linkUser.get_attribute("href"))
                                linkUserContent = linkUser.get_attribute("href")

                        if self.findElement(blockComment, selectorComment):
                            commentUser = blockComment.find_element(By.CSS_SELECTOR, selectorComment)
                            if commentUser is not None:
                                print("commentUser")
                                print(commentUser.text)
                                commentUserContent = commentUser.text

                        userComment = UserComment(linkUserContent, commentUserContent)
                        publicationComment = PublicationComment(username, publication.get_attribute("href"),
                                                                userComment)

                        arrayPublicationComment.append(publicationComment)

                    sleep(10)
                    if self.findElement(self._driverSelenium.getBrowser(), selectorClosePublication):
                        self._driverSelenium.closeDiv(selectorClosePublication)
                        sleep(20)

        except Exception as e:
            print(e)

    def getCommentFromFile(self, prefix):
        os.chdir("./data/in")
        filenameReader = input("Enter the filename .csv: ")
        if len(filenameReader) > 0 and len(prefix) > 0:
            print("Loading list from %s..." % filenameReader)
            listAccount = self.loadGeneralCsv(filenameReader)
            os.chdir("../out")

            selectorPublication = 'div[class="_ac7v xras4av xgc1b0m xat24cr xzboxd6"] > div[class="x1lliihq x1n2onr6 xh8yej3 x4gyw5p xfllauq xo2y696 x11i5rnm x2pgyrj"] > a[class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]'
            selectorClosePublication = 'div[class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"] > div[class="x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"]'

            selectorBlockComment = 'div[class="x1qjc9v5 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xk390pu xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xggy1nq x11njtxf"] > li[class="_a9zj _a9zl"] > div[class="_a9zm"] > div[class=" _a9zo"] > div[class="_a9zr"]'
            selectorLinkUser = 'h3[class="_a9zc"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xw3qccf x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > span[class="xt0psk2"] > div > a[class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83"]'
            selectorComment = 'div[class="_a9zs"] > span[class="_ap3a _aaco _aacu _aacx _aad7 _aade"]'
            arrayPublicationComment = []

            for account in listAccount:
                profile = account['profile']
                self._driverSelenium.executeGetPage(url=f"{profile}")
                sleep(5)
                self.getCommentPublicationFromProfile(arrayPublicationComment, account['username'],
                                                      selectorBlockComment,
                                                      selectorClosePublication, selectorComment, selectorLinkUser,
                                                      selectorPublication)

            if 0 < len(arrayPublicationComment):
                csvOut = prefix + "politic_publication_comment_%s.csv" % datetime.now().strftime(
                    "%Y_%m_%d_%H%M")
                writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
                writer.writerow(['username', 'url_publication', 'B_name', 'B_profile'])

            for publicationComment in arrayPublicationComment:
                writer.writerow(
                    [publicationComment.getUsername(), publicationComment.getUrlPublication(),
                     publicationComment.getUserComment().getUrlUsername(),
                     publicationComment.getUserComment().getComment()])

    def findUserMatchPadron(self, prefix, mainPage):
        xpathLinkSearch = '//div[@class="x1xgvd2v x1o5hw5a xaeubzz x1cy8zhl xvbhtw8 x9f619 x78zum5 xdt5ytf x1gvbg2u x1y1aw1k xn6708d xx6bls6 x1ye3gou"]/div[2]/div[2]/span/div/a'
        selectorInputSearch = '//div[@class="xjoudau x6s0dn4 x78zum5 xdt5ytf x1c4vz4f xs83m0k xrf2nzk x1n2onr6 xh8yej3 x1hq5gj4"]/input'

        selectorDivResult = 'div[class="x78zum5 xdt5ytf x5yr21d"] > div[class="x6s0dn4 x78zum5 xdt5ytf x5yr21d x1odjw0f x1n2onr6 xh8yej3"] > div[class="x9f619 x78zum5 xdt5ytf x1iyjqo2 x6ikm8r x1odjw0f xh8yej3 xocp1fn"] > a[class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"]'
        selectorSpanSearch = 'div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xxbr6pl xbbxn1n xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"] > div[class="x9f619 x1n2onr6 x1ja2u2z x1qjc9v5 x78zum5 xdt5ytf x1iyjqo2 xl56j7k xeuugli"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9"] > div[class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli x1iyjqo2"] > div[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"] > span[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj"]'

        xpathLinkSearchClose = '//div[@class="x1xgvd2v x1cy8zhl xvbhtw8 x9f619 x78zum5 xdt5ytf x1gvbg2u x1y1aw1k xn6708d xx6bls6 x1ye3gou"]/div[2]/div[2]/span/div/a'

        os.chdir("./data/in")
        filenameReader = "mil_dato_balde_tres.csv"
        if len(filenameReader) > 0 and len(mainPage) > 0:
            listFileRow = self.loadCustomCsv(filenameReader, "B_lastname", "B_second_lastname", "B_firstname",
                                             "B_middlename")
            os.chdir("../out")
            arrayProfileName = []

            try:
                self._driverSelenium.executeGetPage(url=f"{mainPage}")

                elementSearchLinkXpath = self._driverSelenium.evaluateExpressionXPath(xpathLinkSearch)
                sleep(10)
                ActionChains(self._driverSelenium.getBrowser()).move_to_element(elementSearchLinkXpath).perform()
                elementSearchLinkXpath.click()
                sleep(30)
                elementInputSearch = self._driverSelenium.evaluateExpressionXPath(selectorInputSearch)
                ActionChains(self._driverSelenium.getBrowser()).move_to_element(elementInputSearch).perform()

                for fileRow in listFileRow:

                    nameSearch = fileRow.toString()
                    print(nameSearch)

                    ActionChains(self._driverSelenium.getBrowser()).key_down(Keys.SHIFT).send_keys(nameSearch).perform()
                    sleep(30)

                    listPotentialContact = self._driverSelenium.evaluateExpressionCssSelectorMany(selectorDivResult)
                    for contact in listPotentialContact:
                        urlProfile = contact.get_attribute("href")
                        if self.findElement(contact, selectorSpanSearch):
                            elementSpan = contact.find_element(By.CSS_SELECTOR, selectorSpanSearch)
                            nameProfile = self.filterFullname(r"[\\•]", elementSpan.text)
                        profileName = ProfileName(urlProfile, nameProfile)
                        arrayProfileName.append(profileName)

                    elementSearchLinkXpath2 = self._driverSelenium.evaluateExpressionXPath(xpathLinkSearchClose)
                    sleep(10)
                    ActionChains(self._driverSelenium.getBrowser()).move_to_element(elementSearchLinkXpath2).perform()
                    elementSearchLinkXpath2.click()

                    sleep(10)
                    ActionChains(self._driverSelenium.getBrowser()).move_to_element(elementSearchLinkXpath).perform()
                    elementSearchLinkXpath.click()

            except Exception:
                pass

            if 0 < len(arrayProfileName):
                csvOut = prefix + "padron_match_%s.csv" % datetime.now().strftime(
                    "%Y_%m_%d_%H%M")
                writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
                writer.writerow(['B_name', 'B_profile'])

            for profileName in arrayProfileName:
                writer.writerow([profileName.getName(), profileName.getProfile()])

    def loadCustomCsv(self, filename, lastname, secondLastname, firstname, middlename):
        arrayPotential = []
        with open(filename, 'rt', encoding="utf-8") as inputCsv:
            reader = csv.DictReader(inputCsv)
            for idx, row in enumerate(reader):
                row[lastname] = self.replaceNotNull(row[lastname])
                row[secondLastname] = self.replaceNotNull(row[secondLastname])
                row[firstname] = self.replaceNotNull(row[firstname])
                row[middlename] = self.replaceNotNull(row[middlename])
                potentialContact = PotentialContact(row[lastname], row[secondLastname], row[firstname], row[middlename])
                arrayPotential.append(potentialContact)

        return arrayPotential

    def replaceNotNull(self, potentialName):
        potentialName = potentialName.strip()
        if potentialName == "NULL":
            potentialName = ""

        return potentialName

    def filterFullname(self, regex, potentialFullname):
        splitString = potentialFullname
        if 0 < len(regex) and 0 < len(potentialFullname):
            try:
                regexString = re.search(regex, potentialFullname)
                if regex in regexString:
                    potentialFullname = potentialFullname[:regexString.start()]
                    splitString = potentialFullname.strip()
            except Exception as e:
                print(e)
        return splitString

    def getCommentUserLikePublication(self, prefix, page, username):
        os.chdir("./data/in")
        arrayCensus = self.readCensus("padron.csv")
        filenameReader = input("Enter the filename .csv: ")
        if len(filenameReader) > 0:
            print("Loading list from %s..." % filenameReader)
            listFileRow = self.loadCustomCsvPublicationContact(filenameReader, "username", "publication", "B_name",
                                                               "B_profile")
            os.chdir("../out")
            if len(listFileRow) > 0:
                csvOut = prefix + "user_publication_code_%s.csv" % datetime.now().strftime(
                    "%Y_%m_%d_%H%M")
                writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
                writer.writerow(['name', 'publish', 'B_zone', 'B_code', 'B_name', 'B_profile'])
            try:
                for fileRow in listFileRow:
                    for itemCensus in arrayCensus:
                        if itemCensus.compareOtherFullname(itemCensus.reverseLastname(fileRow.getNameContact())):
                            writer.writerow([fileRow.getNameAccount(), fileRow.getPublication(), itemCensus.getZone(),
                                             itemCensus.getCode(), fileRow.getNameContact(),
                                             fileRow.getProfileContact()])

            except Exception:
                sys.stdout.write("")

    def loadCustomCsvCode(self, filename, zone, code, lastname, secondLastname, firstname, middlename):
        arrayPerson = []
        with open(filename, 'rt', encoding="utf-8") as inputCsv:
            reader = csv.DictReader(inputCsv)
            for idx, row in enumerate(reader):
                row[zone] = self.replaceNotNull(row[zone])
                row[code] = self.replaceNotNull(row[code])
                row[lastname] = self.replaceNotNull(row[lastname])
                row[secondLastname] = self.replaceNotNull(row[secondLastname])
                row[firstname] = self.replaceNotNull(row[firstname])
                row[middlename] = self.replaceNotNull(row[middlename])
                potentialContact = Person(row[zone], row[code], row[lastname], row[secondLastname], row[firstname],
                                          row[middlename])
                arrayPerson.append(potentialContact)

        print("%d quantity of item" % (idx + 1))
        return arrayPerson

    def readCensus(self, filename):
        arrayCensus = []
        if len(filename) > 0:
            arrayCensus = self.loadCustomCsvCode(filename, "B_zone", "B_code", "B_lastname", "B_second_lastname",
                                                 "B_firstname", "B_middlename")
        return arrayCensus

    def loadCustomCsvPublicationContact(self, filename, nameAccount, publication, nameContact, profileContact):
        arrayPerson = []
        with open(filename, 'rt', encoding="utf-8") as inputCsv:
            reader = csv.DictReader(inputCsv)
            for idx, row in enumerate(reader):
                row[nameAccount] = self.replaceNotNull(row[nameAccount])
                row[publication] = self.replaceNotNull(row[publication])
                row[nameContact] = self.replaceNotNull(row[nameContact])
                row[profileContact] = self.replaceNotNull(row[profileContact])

                publicationContact = PublicationContact(row[nameAccount], row[publication], row[nameContact],
                                                        row[profileContact])

                arrayPerson.append(publicationContact)

        print("%d quantity of item" % (idx + 1))
        return arrayPerson

    def replaceNotNull(self, potentialName):
        potentialName = potentialName.strip()
        if potentialName == "NULL":
            potentialName = ""

        return potentialName
