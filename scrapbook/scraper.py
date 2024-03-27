import requests
from bs4 import BeautifulSoup
from book import Book

class Scraper:
    """Crée un scraper."""
    def __init__(self, base_url):
        """Initialise l'URL de base."""
        self.base_url = base_url

    def get_soup(self, endpoint=''):
        """ 
        Fait une requête HTTP GET à l'URL combinée de base_url et endpoint, 
        et retourne un objet BeautifulSoup du contenu HTML.

        Args:
            endpoint (str): Chemin à ajouter à l'URL de base pour former l'URL complète.
        """
        full_url = self.base_url + endpoint
        try:
            response = requests.get(full_url)
            response.raise_for_status()  # Vérifie le succès de la requête
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Request Error : {e}")
            return None
        
    def get_book_info(self, endpoint=''):
        """Extrait les informations d'un livre spécifié par l'endpoint."""
        soup = self.get_soup(endpoint)
        try:
            title = soup.find('h1').text.strip()
            price = soup.find('p', class_='price_color').text.strip()
            availability = soup.find_all('tr')[5].td.text

            # Ajoute ici l'extraction d'autres informations si nécessaire
            return Book(title, price, availability)
           
            #return {'title': title, 'price': price}
        except Exception as e:
            print(f"Error extracting book info: {e}")
            return None







    

