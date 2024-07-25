from requests.exceptions import ConnectionError, Timeout
import requests
import time
import os
from utils import clean_filename


class Book:
    """
    Représente un livre extrait du site web.

    Attributs :
        product_book_url (str): URL de la page du livre.
        title (str): Titre du livre.
        upc (str): Code produit universel du livre.
        price_incl_tax (float): Prix du livre incluant les taxes.
        price_excl_tax (float): Prix du livre excluant les taxes.
        availability (int): Nombre d'exemplaires disponibles.
        review_rating (int): Évaluation du livre (1 à 5).
        category (str): Catégorie du livre.
        image_url (str): URL de l'image de couverture du livre.
        product_description (str): Description du livre.
    """

    def __init__(self, product_book_url=None, title=None, upc=None, price_incl_tax=None,
                 price_excl_tax=None, availability=None, review_rating=None, category=None,
                 image_url=None, product_description=None):
        self.product_book_url = product_book_url
        self.title = title
        self.upc = upc
        self.price_incl_tax = price_incl_tax
        self.price_excl_tax = price_excl_tax
        self.availability = availability
        self.review_rating = review_rating
        self.category = category
        self.image_url = image_url
        self.product_description = product_description

    def to_dict(self):
        """
        Convertit les attributs du livre en un dictionnaire.

        Returns:
            dict: Dictionnaire contenant les données du livre
        """
        return {
            'product_book_url': self.product_book_url,
            'title': self.title,
            'upc': self.upc,
            'price_including_tax': self.price_incl_tax,
            'price_excluding_tax': self.price_excl_tax,
            'availability': self.availability,
            'review_rating': self.review_rating,
            'category': self.category,
            'image_url': self.image_url,
            'product_description': self.product_description,
        }

    def fetch_image_with_retries(self, url, max_retries=3, timeout=10):
        """
        Télécharge une image en effectuant jusqu'à `max_retries` tentatives.

        Args:
            url (str): URL de l'image à télécharger.
            max_retries (int): Nombre maximal de tentatives de téléchargement.
            timeout (int): Temps d'attente maximal pour chaque tentative, en secondes.

        Returns:
            response: L'objet Response contenant les données de l'image en cas de succès.

        Raises:
            ConnectionError: En cas d'échec après `max_retries` tentatives.
        """
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                return response  # Succès, retourne la réponse
            except (ConnectionError, Timeout) as e:
                print(f"Tentative {retries + 1}/{max_retries} échouée pour {url}: {e}")
                retries += 1
                time.sleep(2)
        raise ConnectionError(f"Echec après {max_retries} tentatives pour {url}")

    def save_cover_image(self, base_directory='book_images'):
        """
        Sauvegarde l'image de couverture du livre dans le répertoire spécifié.

        L'image est sauvegardée dans un sous-répertoire correspondant à la catégorie du livre,
        et le nom du fichier est basé sur l'UPC du livre.

        Args:
            base_directory (str): Chemin du répertoire de base pour les images sauvegardées.

        Note:
            Si le téléchargement de l'image échoue après plusieurs tentatives, un message d'erreur est affiché.
        """
        category_cleaned = clean_filename(self.category)
        image_save_path = os.path.join(base_directory, category_cleaned, f"{self.upc}.jpg")

        try:
            response = self.fetch_image_with_retries(self.image_url)  # Utilise la méthode avec tentatives de connexions
            os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
            with open(image_save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image sauvegardée : {image_save_path}")
        except ConnectionError as e:
            print(f"Erreur de du téléchargement de l'image pour {self.upc} après plusieurs tentatives : {e}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image pour {self.upc} : {e}")
