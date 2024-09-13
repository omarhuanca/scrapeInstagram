from src.tool.DriverSeleniumInstagram import DriverSeleniumInstagram
from src.tool.ScrapeInstagram import ScrapeInstagram


def main():
    driverSeleniumInstagram = DriverSeleniumInstagram()
    scrapeInstagram = ScrapeInstagram("../../data/in/", "configInstagram.txt", driverSeleniumInstagram)
    basicAccount = scrapeInstagram.readConfigPath()
    scrapeInstagram.instagramLogin(basicAccount)

    itemOption = input("Enter number value: ")

    if itemOption == "1":
        # get info from username, profile
        scrapeInstagram.getLikeFromPublication("1_", "https://www.instagram.com/p/C8xtve2Rcfl/", "guevaradiputadouy")
    elif itemOption == "2":
        # get link publication
        scrapeInstagram.generateNavigationProfile("2_", "https://www.instagram.com/andresojedaxpartidocolorado/", 1)
    elif itemOption == "3":
        # get link publication, username, profile
        scrapeInstagram.generateLikeFromListPublication("3_", "https://www.instagram.com/andresojedaxpartidocolorado/",
                                                        1)
    elif itemOption == "4":
        scrapeInstagram.getCommentFromPublication("4_", "https://www.instagram.com/p/C8xtve2Rcfl/",
                                                  "Andrés Ojeda Presidente")
    elif itemOption == "5":
        # get profile, comment
        scrapeInstagram.getCommentFromListPublication("5_", "https://www.instagram.com/andresojedaxpartidocolorado/",
                                                      "Andrés Ojeda Presidente")
    elif itemOption == "6":
        scrapeInstagram.getCommentFromFile("6_")
    elif itemOption == "7":
        # balde 3.1 found user
        scrapeInstagram.findUserMatchPadron("7_", "https://www.instagram.com/")
    elif itemOption == "8":
        scrapeInstagram.getCommentUserLikePublication("8_", "https://www.instagram.com/andresojedaxpartidocolorado/",
                                                      "Andrés Ojeda Presidente")

    driverSeleniumInstagram.closeExecution()


if __name__ == "__main__":
    main()
