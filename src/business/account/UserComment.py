class UserComment:

    def __init__(self, urlUsername, comment):
        self._urlUsername = urlUsername
        self._comment = comment

    def getUrlUsername(self):
        return self._urlUsername

    def getComment(self):
        return self._comment
