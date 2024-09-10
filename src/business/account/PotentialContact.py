class PotentialContact:

    def __init__(self, lastname, secondLastname, firstname, middlename):
        self._lastname = lastname
        self._secondLastname = secondLastname
        self._firstname = firstname
        self._middlename = middlename

    def getLastname(self):
        return self._lastname

    def getSecondLastname(self):
        return self._secondLastname

    def getFirstname(self):
        return self._firstname

    def getMiddlename(self):
        return self._middlename

    def __str__(self):
        return self.toString()

    def toString(self):
        result = ''
        if len(self._middlename) > 0:
            result = self._firstname + ' ' + self._middlename + ' ' + self._lastname + ' ' + self._secondLastname
        else:
            result = self._firstname + ' ' + self._lastname + ' ' + self._secondLastname

        return result
