from src.business.account.UserLike import UserLike


class PublicationUser:

    def __init__(self, urlPublication, userLike: UserLike):
        self._urlPublication = urlPublication
        self._userLike = userLike

    def getUrlPublication(self):
        return self._urlPublication

    def getUserLike(self):
        return self._userLike
