class Person:

    def __init__(self, zone, code, lastname, secondLastname, firstname, middlename):
        self._zone = zone
        self._code = code
        self._lastname = lastname
        self._secondLastname = secondLastname
        self._firstname = firstname
        self._middlename = middlename

    def __str__(self):
        return self.toString().strip()

    def toString(self):
        return self.getToLastname() + ' ' + self.getToName()

    def getZone(self):
        return self._zone

    def getCode(self):
        return self._code

    def getToName(self):
        return self._firstname + ' ' + self._middlename

    def getToLastname(self):
        return self._lastname + ' ' + self._secondLastname

    def reverseLastname(self, potentialFullname):
        response = ''

        potentialFullname = potentialFullname.strip()
        arrayString = potentialFullname.split(" ", potentialFullname.count(" "))

        arrayCopy = arrayString.copy()

        size = len(arrayCopy)
        counter = (size // 2)

        if 0 == size % 2 and size > 2:
            counter = 2

        response = self.extractElementArray(arrayCopy, counter, size)

        size = len(arrayCopy)
        counter = 0

        response = self.acumulateElementArray(arrayCopy, counter, response, size)

        return response

    def extractElementArray(self, arrayCopy, counter, size):
        response = ""
        while counter < size:
            response = response + ' ' + arrayCopy[counter]
            size = size - 1
            arrayCopy.pop(counter)
        return response

    def acumulateElementArray(self, arrayCopy, counter, response, size):
        while counter < size:
            response = response + ' ' + arrayCopy[counter]
            counter = counter + 1
        response = response.strip()
        return response

    def compareOtherFullname(self, potentialFullname):
        return self.compareAnyName(self.extractPersonName(potentialFullname), self.getToName()) and self.compareAnyName(
            self.extractPersonLastName(potentialFullname), self.getToLastname())

    def compareAnyName(self, potentialName, personName):
        result = False
        potentialName = potentialName.strip()
        personName = personName.strip()
        if 0 < len(potentialName) and 0 < len(personName):
            result = potentialName.lower().__contains__(personName.lower())
            if len(potentialName) < len(personName):
                result = personName.lower().__contains__(potentialName.lower())

        return result

    def extractPersonName(self, potentialFullname):
        arrayName = potentialFullname.split(" ", potentialFullname.count(" "))
        counter = 2
        size = len(arrayName)
        if 2 >= size:
            counter = size // 2
        response = self.acumulateElementArray(arrayName, counter, '', size)

        return response

    def extractPersonLastName(self, potentialFullname):
        arrayName = potentialFullname.split(" ", potentialFullname.count(" "))
        arrayNameCopy = arrayName.copy()

        counter = 2
        size = len(arrayNameCopy)
        if counter == size:
            counter = 1
        self.extractElementArray(arrayNameCopy, counter, size)

        size = len(arrayNameCopy)
        response = self.acumulateElementArray(arrayNameCopy, 0, '', size)

        return response
