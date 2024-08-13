from src.business.account.UserComment import UserComment


class PublicationComment:

    def __init__(self, urlPublication, userComment : UserComment):
        self._urlPublication = urlPublication
        self._userComment = userComment

    def getUrlPublication(self):
        return self._urlPublication

    def getUserComment(self):
        return self._userComment
