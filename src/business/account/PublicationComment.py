from src.business.account.UserComment import UserComment


class PublicationComment:

    def __init__(self, username, urlPublication, userComment : UserComment):
        self._username = username
        self._urlPublication = urlPublication
        self._userComment = userComment

    def getUsername(self):
        return self._username

    def getUrlPublication(self):
        return self._urlPublication

    def getUserComment(self):
        return self._userComment
