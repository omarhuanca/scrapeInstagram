class PublicationContact:

    def __init__(self, nameAccount, publication, nameContact, profileContact):
        self._nameAccount = nameAccount
        self._publication = publication
        self._nameContact = nameContact
        self._profileContact = profileContact

    def getNameAccount(self):
        return self._nameAccount

    def getPublication(self):
        return self._publication

    def getNameContact(self):
        return self._nameContact

    def getProfileContact(self):
        return self._profileContact

    def __str__(self):
        return self._nameAccount + ',' + self._publication + ',' + self._nameAccount + ',' + self._profileContact
