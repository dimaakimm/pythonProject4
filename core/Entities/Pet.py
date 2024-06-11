import Pet
class Volunteer:
    def __init__(self, forename, surname, passport, phoneNumber, email, tgId):
        self.forename = forename
        self.surname = surname
        self.passport = passport
        self.phoneNumber = phoneNumber
        self.email = email
        self.tgId = tgId

    def addOwnPet(self, photoId, name, isStrerilized, district, info):
        newPet = Pet(photoId, photoId, name, isStrerilized, district, info)