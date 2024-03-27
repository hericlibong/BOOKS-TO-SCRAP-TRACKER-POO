import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from urllib.parse import urljoin

class Book:
    """Create a book"""
    def __init__(self, title, availability, universal_product_code, 
                 price_including_tax, price_excluding_tax, review_rating,
                 category, product_book_url, image_url, description):
        """Initialise all data book : title, avaialability, universal_product_code """
        self.title = title
        self.availability = availability
        self.universal_product_code = universal_product_code
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.review_rating = review_rating
        self.category = category
        self.product_book_url = product_book_url
        self.image_url = image_url
        self.description = description
        

    def to_dict(self):
        """Turn book data to dict"""
        return {
            
            "title": self.title, 
            'availability': self.availability,
            'universal_product_code': self.universal_product_code,
            'price_including_tax': self.price_including_tax, 
            'price_excluding_tax': self.price_excluding_tax, 
            'review_rating': self.review_rating,
            'category': self.category,
            'product_book_url': self.product_book_url,
            'image_url': self.image_url,
            'description': self.description
            
        }



class Scraper:
    def __init__(self, base_url = "https://books.toscrape.com/"):
        self.base_url = base_url
        self.catalogue_url = urljoin(self.base_url, 'catalogue/')

    def get_soup(self, url):
        """Passe la requête Http"""
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    

    def get_category_links(self):
        start_url = self.base_url  # Si base_url est la racine du site
        soup = self.get_soup(start_url)
        category_links = []
        list_link = soup.find('ul', class_='nav').find_all('li')
        for a in list_link:
            # Utilise urljoin pour construire l'URL complet sans dupliquer 'catalogue/'
            link = urljoin(self.base_url, a.find('a')['href'])
            category_links.append(link)
        return category_links[1:]  # Exclut la première catégorie "Books"

    

    def extract_and_clean_title(self, soup):
        title = soup.find('h1').text
        return title.lower()


    def extract_and_clean_availability(self, soup):
        try :
            raw_availability = soup.find('p', class_='instock availability').text
            num_available = raw_availability.replace('In stock', '').replace('(', '').replace(')', '').replace('available', '').strip()
            return int(num_available)
        except Exception:
            return None
    
    def extract_and_clean_upc(self, soup):
        """ Extrait le code produit universel (UPC) de la page du produit."""
        try: 
            return soup.find_all('tr')[0].td.text
        except Exception:
            return None
        
    def extract_and_clean_price_including_tax(self, soup):
        """
        Extrait le prix du livre incluant les taxes
        
        Returns:
            float: Prix incluant les taxes ou None en cas d'erreur.
        """
        try:
            price_including_tax = soup.find_all('tr')[3].td.text.strip()[1:] #Enlève le sigle Livre sur le prix
            return float(price_including_tax)
        except Exception:
            return None
        
    def extract_and_clean_price_excluding_tax(self, soup):
        """
            Extrait le prix du livre hors taxes.
        
        Returns:
                float: Prix hors taxes ou None en cas d'erreur.
        """
        try : 
            price_excluding_tax = soup.find_all('tr')[2].td.text.strip()[1:] 
            return float(price_excluding_tax)
        except Exception:
            return None
        
    def extract_and_clean_review_rating(self, soup):
        words_to_nums = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5} # Dictionnaire pour convertir les mots en chiffre
        try : 
            rating_word = soup.find('p', class_='star-rating')['class'][1]
            # Convertir le mot en nombre en utilisant le dictionnaire
            return words_to_nums.get(rating_word, 0)  #Retourne la valeur de la clé si celle-ci est dans le dictionnaire. Si la clé n'est pas présente, la valeur est 0
        except Exception:
            return None
        
    def extract_and_clean_category(self, soup):
        try : 
            return soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
        except Exception:
            return None
        
    def extract_and_clean_image_url(self, soup):
        try:
            image_url_relative = soup.find('img')['src']
            image_url_absolute = urljoin(self.base_url, image_url_relative.replace('../', ''))
            return image_url_absolute
        except Exception:
            return None

        
    def get_product_description(self, soup):
        try :
            description_tag = soup.find('div', id='product_description')
            if description_tag : 
                description = description_tag.find_next_sibling('p').text
                description = description.replace('/', '')
                description = description.replace('&amp;', '&')
                description = re.sub(' +', ' ', description)
                description = description.strip()
                return unidecode(description)
            else:
                return None
        except Exception:
            return None  


    def get_book_data(self, book_url):
        print("Tentative d'accès à l'URL du livre :", book_url)
        soup = self.get_soup(book_url)
        title = self.extract_and_clean_title(soup)
        availability = self.extract_and_clean_availability(soup)
        universal_product_code = self.extract_and_clean_upc(soup)
        price_including_tax = self.extract_and_clean_price_including_tax(soup)
        price_excluding_tax = self.extract_and_clean_price_excluding_tax(soup)
        review_rating = self.extract_and_clean_review_rating(soup)
        category = self.extract_and_clean_category(soup)
        product_book_url =  book_url 
        image_url = self.extract_and_clean_image_url(soup)
        description = self.get_product_description(soup)

        return Book(title, availability, universal_product_code, 
                    price_including_tax, price_excluding_tax, review_rating, 
                    category, product_book_url, image_url, description)
    
    def get_books_urls_from_category(self, category_url):
        """Renvoie les urls de tous les livres d'une catégorie"""
        book_urls = []
        while True : 
            category_soup = self.get_soup(category_url)
            book_links = category_soup.find_all("h3")
            book_urls.extend([urljoin(self.base_url, link.find('a')['href'].replace('../', '')) for link in book_links])
            # Gestion de la pagination
            next_button = category_soup.find(class_='next')
            if next_button:
                next_page_partial = next_button.find('a')['href'] 
                category_url = urljoin(category_url, next_page_partial) # Prépare de la page suivante
            else:
                break # Sort de la boucle si aucune page suivante n'est trouvée
        return book_urls
    
    def get_books_data_from_category(self, category_url):
        book_urls = self.get_books_urls_from_category(category_url)
        books_data = []
        for book_url in book_urls:
            book_data = self.get_book_data(book_url)  # Ici, book_url est déjà une URL complète.
            if book_data:
                books_data.append(book_data.to_dict())  # Correction ici: utilise book_data au lieu de books_data
        return books_data
    

    def get_all_books(self):
        all_books_data = []
        for category_url in self.get_category_links():
            books_data = self.get_books_data_from_category(category_url)
            all_books_data.extend(books_data)
        return all_books_data



    

    

# Usage

scraper = Scraper("https://books.toscrape.com/catalogue/")
# category_url = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
# books_data = scraper.get_books_data_from_category(category_url)
# for book_data in books_data:
#     print(book_data)

all_books_data = scraper.get_all_books()
