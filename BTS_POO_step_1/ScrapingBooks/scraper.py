import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from urllib.parse import urljoin
from books import Book


class Scraper:
    """Crée et configure le Scraper"""
    def __init__(self, url=None, headers=None):
        self.url = url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.soup = None  # Initialiser la propriété soup à None

    def set_url(self, url):
        self.url = url
        self.soup = None

    def fetch_soup(self):
            """Extrait le contenu HTML et le parse, stocke le résultat dans self.soup."""
            if not self.soup:  # Si soup n'est pas déjà défini
                try:
                    response = requests.get(self.url, headers=self.headers)
                    response.raise_for_status()
                    self.soup = BeautifulSoup(response.content, 'html.parser')
                except requests.RequestException as e:
                    print(f"Error retrieving content: {e}")
                    self.soup = None  # Assurez-vous que soup est None en cas d'échec
            return self.soup

class DataExtractor(Scraper):
    """Gère l'extraction des données; hérite de Scraper"""

    def extract_title(self):
        """Extrait et transforme la casse titre"""
        soup = self.fetch_soup()  # Assurez-vous d'avoir le dernier soup disponible
        if soup:  # Vérifier que soup n'est pas None
            try:
                title = soup.find('h1').text.strip()
                return title.lower()
            except Exception:
                return None
        return None

    
    def extract_upc(self):
        """ Extrait le code produit universel (UPC) de la page du produit."""
        soup = self.fetch_soup()
        if soup:
            try: 
                return soup.find_all('tr')[0].td.text
            except Exception:
                return None
        return None 

    
    def extract_price_including_tax(self):
        """Extrait le prix du livre incluant les taxes en float"""
        soup = self.fetch_soup()
        if soup:
            try:
                price_including_tax = soup.find_all('tr')[3].td.text.strip()[1:] #Enlève le sigle Livre sur le prix
                return float(price_including_tax)
            except Exception:
                return None
        return None
    
    
    def extract_price_excluding_tax(self):
        """
            Extrait le prix du livre hors taxes.
        
        Returns:
                float: Prix hors taxes ou None en cas d'erreur.
        """
        soup = self.fetch_soup()
        if soup:
            try : 
                price_excluding_tax = soup.find_all('tr')[2].td.text.strip()[1:] 
                return float(price_excluding_tax)
            except Exception:
                return None
        return None
            
    
    def extract_review_rating(self):
        words_to_nums = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5} # Dictionnaire pour convertir les mots en chiffre
        soup = self.fetch_soup()
        if soup:
            try : 
                rating_word = soup.find('p', class_='star-rating')['class'][1]
                # Convertir le mot en nombre en utilisant le dictionnaire
                return words_to_nums.get(rating_word, 0)  #Retourne la valeur de la clé si celle-ci est dans le dictionnaire. Si la clé n'est pas présente, la valeur est 0
            except Exception:
                return None
        return None    
            
    
    def extract_category(self):
        soup = self.fetch_soup()
        if soup:
            try : 
                return soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
            except Exception:
                return None
        return None
    

    def extract_availability(self):
        soup = self.fetch_soup()
        if soup:
            try :
                raw_availability = soup.find('p', class_='instock availability').text
                num_available = raw_availability.replace('In stock', '').replace('(', '').replace(')', '').replace('available', '').strip()
                return int(num_available)
            except Exception:
                return None
        return None
        
    
    def extract_image_url(self):
        base_url = 'https://books.toscrape.com/'
        soup = self.fetch_soup()
        if soup:
            try:
                image_url_relative = soup.find('img')['src']
                image_url_absolute = urljoin(base_url, image_url_relative.replace('../', ''))
                return image_url_absolute
            except Exception:
                return None
        return None
        
    
    def extrac_product_description(self):
        soup = self.fetch_soup()
        if soup:
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
        return None
    
    def extract_category_urls(self):
        """Extrait et retourne les URLs des catégories depuis l'URL principale du site."""
        self.soup = None  # Réinitialise soup pour forcer un nouveau fetch de la page principale
        soup = self.fetch_soup()
        if soup:
            category_urls = [urljoin(self.url, li.a['href']) for li in soup.find('ul', class_='nav-list').find_all('li')][1:]
            return category_urls
        else:
            return []
        
    def extract_book_urls_from_category(self):
        """Extrait et retourne les URLs des livres d'une catégorie."""
        while True:
            soup = self.fetch_soup()  # Assurez-vous d'avoir le BeautifulSoup de la page de catégorie
            if soup:
                book_urls = [
                    urljoin("https://books.toscrape.com/catalogue/", book.find('a')['href'][9:]) 
                    for book in soup.find_all('h3')
                ]
                next_button = soup.find(class_='next')
                if next_button:
                    next_page_partial = next_button.find('a')['href']
                    category_url = urljoin(category_url, next_page_partial)
                else :
                    break
                return book_urls
            else:
                return []

# Instanciation de DataExtractor avec l'URL d'une page produit spécifique
# data_extractor = DataExtractor("https://books.toscrape.com/catalogue/throwing-rocks-at-the-google-bus-how-growth-became-the-enemy-of-prosperity_948/index.html")

# # Appel des méthodes d'extraction
# title = data_extractor.extract_title()
# upc = data_extractor.extract_upc()
# price_incl_tax = data_extractor.extract_price_including_tax()
# price_excl_tax = data_extractor.extract_price_excluding_tax()
# review_rating = data_extractor.extract_review_rating()
# category = data_extractor.extract_category()
# avaibility = data_extractor.extract_availability()
# image_url = data_extractor.extract_image_url()
# product_description = data_extractor.extrac_product_description()

# Affichage des résultats
# print("Title:", title)
# print("UPC:", upc)
# print("Price Including Tax:", price_incl_tax)
# print("Price Excluding Tax:", price_excl_tax)
# print("Review Rating:", review_rating)
# print("Category:", category)
# print('Avaibility:', avaibility)
# print("Image URL:", image_url)
# print("Product Description:", product_description)

# book_info = Book(
#     title=title,
#     upc=upc,
#     price_incl_tax=price_incl_tax,
#     price_excl_tax=price_excl_tax,
#     review_rating=review_rating,
#     category=category,
#     image_url=image_url,
#     product_description=product_description
# )

# # Récupération des données du livre sous forme de dictionnaire
# book_data = book_info.to_dict()
# print(book_data)


url = "https://books.toscrape.com/"
data_extractor = DataExtractor(url)
    
# category_urls = data_extractor.extract_category_urls()
# print(category_urls)


data_extractor.set_url("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
book_urls = data_extractor.extract_book_urls_from_category()
print(book_urls)