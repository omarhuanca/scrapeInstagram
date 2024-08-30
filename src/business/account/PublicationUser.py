from src.business.account.UserLike import UserLike


class PublicationUser:

    def __init__(self, username, urlPublication, userLike: UserLike):
        self._username = username
        self._urlPublication = urlPublication
        self._userLike = userLike

    def getUsername(self):
        return self._username

    def getUrlPublication(self):
        return self._urlPublication

    def getUserLike(self):
        return self._userLike
