import requests
from bs4 import BeautifulSoup

class Book:
    def __init__(self, title, price, availability):
        self.title = self.clean_title(title)
        self.price = self.clean_price(price)
        self.availability = self.clean_avaibility(availability)
    
    
    @staticmethod
    def clean_title(upper_title):
        """put title in lower case """
        title = upper_title.lower()
        return title
    
    @staticmethod
    def clean_price(raw_price):
        price = raw_price.replace('£', '')
        try:
            return float(price)
        except ValueError:
            print("Numeric Conversion Error")
            return None
        
    @staticmethod
    def clean_avaibility(raw_avaibility):
        num_available = raw_avaibility.replace('In stock', '').replace('(', '').replace(')', '').replace('available', '').strip()
        return int(num_available)


class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_soup(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')

    def get_book_data(self, book_url):
        try : 
            soup = self.get_soup(self.base_url + book_url)
            title = soup.find('h1').text
            price = soup.find('p', class_='price_color').text
            availability = soup.find('p', class_='instock availability').text
            return Book(title, price, availability)
        except Exception:
            return None
       

# Usage
scraper = Scraper("https://books.toscrape.com/")
book = scraper.get_book_data("catalogue/a-light-in-the-attic_1000/index.html")
print(book.title, book.price, book.availability)
