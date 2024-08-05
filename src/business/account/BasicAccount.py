class BasicAccount:

    def __init__(self, email, password):
        self._email = email
        self._password = password

    def __str__(self):
        return ''

    def getEmail(self):
        return self._email

    def getPassword(self):
        return self._password
