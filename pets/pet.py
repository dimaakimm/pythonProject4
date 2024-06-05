from bs4 import BeautifulSoup as bs
import requests

class Pet(object):
    def __init__(self, name, sex, age, photoUrl, url):
        self.name = name
        self.url = url
        self.sex = sex
        self.age = age
        self.photoUrl = photoUrl

    @property
    def getSexPet(self):
        return self.sex

    @property
    def getInformationPet(self):
        return self.information

    @property
    def getUrlPet(self):
        return self.url

    @property
    def getPhotoUrlPet(self):
        return self.photoUrl

    @property
    def getAgePet(self):
        return self.age

    @property
    def getNamePet(self):
        return self.name

    def createInformation(self):
        req = requests.get(self.url)
        soup = bs(req.text, "lxml")
        information_block = soup.select_one('div.s-c-p-i-gallery__info')
        text_block = information_block.select('p')
        self.information = ""
        for block in text_block:
            self.information += block.text


