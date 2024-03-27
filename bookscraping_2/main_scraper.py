import requests
from bs4 import BeautifulSoup

class Book:
    def __init__(self, title, price, availability):
        self.title = title
        self.price = price
        self.availability = availability

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_soup(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')

    def clean_title(self, title):
        return title.lower()

    def clean_price(self, price):
        price = price.replace('£', '')
        try:
            return float(price)
        except ValueError:
            print("Numeric Conversion Error")
            return None

    def clean_availability(self, availability):
        num_available = availability.replace('In stock', '').replace('(', '').replace(')', '').replace('available', '').strip()
        return int(num_available)

    def get_book_data(self, book_url):
        try:
            soup = self.get_soup(self.base_url + book_url)
            title = self.clean_title(soup.find('h1').text)
            price = self.clean_price(soup.find('p', class_='price_color').text)
            availability = self.clean_availability(soup.find('p', class_='instock availability').text)
            return Book(title, price, availability)
        except Exception as e:
            print(f"Error extracting book data: {e}")
            return None

# Usage
scraper = Scraper("https://books.toscrape.com/")
book = scraper.get_book_data("catalogue/a-light-in-the-attic_1000/index.html")
print(book.title, book.price, book.availability)