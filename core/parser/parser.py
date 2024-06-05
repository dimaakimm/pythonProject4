import bs4
import requests
from pets.pet import Pet
class Client:
    pets = list()
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept-Language': 'ru'
        }
    def parse(self):
        text = self.load_page()
        self.parse_page(text=text)

    def load_page(self, page:int = None):
        url = 'https://urbananimal.ru/shelter'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text
    def parse_page(self, text:str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('a.p-k-b-p-shelter-cat__item')
        print(len(container))
        for i in range(30):
            self.parse_block(block = container[i])
        # for block in container:
        #     self.parse_block(block=block)

    def parse_block(self, block):
        pet_url = block.get('href')
        pet_name = block.select_one('img').get('alt')
        pet_photo = block.select_one('img').get('src')
        pet_sex_age_block = block.select_one('ul')
        pet_sex_age = pet_sex_age_block.select('li')
        pet_sex = pet_sex_age[0].text
        pet_age = pet_sex_age[1].text
        pet = Pet(pet_name, pet_sex, pet_age, pet_photo, pet_url)
        pet.createInformation()
        self.pets.append(pet)

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)

    @property
    def getPets(self):
        return self.pets

if __name__ == '__main__':
    parser = Client()
    parser.run()