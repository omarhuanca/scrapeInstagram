from src.tool.DriverSeleniumInstagram import DriverSeleniumInstagram
from src.tool.ScrapeInstagram import ScrapeInstagram


def main():
    driverSeleniumInstagram = DriverSeleniumInstagram()
    scrapeInstagram = ScrapeInstagram("../../data/in/", "configInstagram.txt", driverSeleniumInstagram)
    basicAccount = scrapeInstagram.readConfigPath()
    scrapeInstagram.instagramLogin(basicAccount)

    itemOption = input("Enter number value: ")

    if itemOption == "1":
        scrapeInstagram.getLikeFromPublication("1_", "https://www.instagram.com/p/C8xtve2Rcfl/")
    elif itemOption == "2":
        scrapeInstagram.generateNavigationProfile("2_", 'https://www.instagram.com/andresojedaxpartidocolorado/', 1)
    elif itemOption == "3":
        scrapeInstagram.generateLikeFromListPublication("3_", 'https://www.instagram.com/andresojedaxpartidocolorado/',
                                                        1)
    elif itemOption == "4":
        scrapeInstagram.getCommentFromPublication("4_", "https://www.instagram.com/p/C8xtve2Rcfl/")
    driverSeleniumInstagram.closeExecution()


if __name__ == "__main__":
    main()
