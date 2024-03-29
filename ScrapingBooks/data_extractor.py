import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from urllib.parse import urljoin



class Scraper:
    """Crée et configure le Scraper"""
    def __init__(self, url=None, headers=None):
        self.url = url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.soup = None  # Initialiser la propriété soup à None

    def set_url(self, url):
        """
    Met à jour l'URL cible pour le scraping et réinitialise l'état de BeautifulSoup.

    Cette méthode permet de changer dynamiquement l'URL cible du scraper sans nécessiter
    une nouvelle instance de l'objet. Elle est particulièrement utile pour naviguer à travers
    les pages web lors du scraping, permettant au scraper de se concentrer sur différentes pages
    en utilisant une seule instance de l'objet.

    Paramètres:
    - url (str): L'URL cible à définir pour les prochaines opérations de scraping.

    Retour:
    - None
    """
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
            try: 
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
        """Extrait et retourne les URLs des livres d'une catégorie. Gère également la pagination
        si nécessaire (cas des catégories ayant plusieurs pages de livres)
        """
        all_books_urls = [] # Stocke les URLs de tous les livres trouvés dans la categorie
        while True:
            soup = self.fetch_soup()  # Assurez-vous d'avoir le BeautifulSoup de la page de catégorie
            if soup:
                book_urls = [
                    urljoin("https://books.toscrape.com/catalogue/", book.find('a')['href'][9:]) 
                    for book in soup.find_all('h3')
                ]
                all_books_urls.extend(book_urls) # Ajoute les URLs extraites à la liste globale
                # Vérification de l'existence d'une page suivante
                next_button = soup.find('li', class_ ='next')
                if next_button:
                    next_page_partial_url = next_button.find('a')['href']
                    # Construction de l'RUL de la page suivante
                    next_page_url = urljoin(self.url, next_page_partial_url)
                    self.set_url(next_page_url) # Mise à jour de l'URL pour charger la page suivante
                else:
                    break # Sortie de la boucle si aucune page n'est trouvée
            else:
                break # Sortie de la boucle en cas d'erreur lors du fetching
        self.soup = None # Réinitialisation de soup après avoir terminé la pagination
        return all_books_urls
             
