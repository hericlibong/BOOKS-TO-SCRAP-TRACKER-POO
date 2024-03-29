# scraper_manager.py
from data_extractor import DataExtractor
from books import Book
import os, csv
from utils import clean_filename


class ScraperManager:
    """ 
    Coordonne l'extraction des données de livres depuis un site web et la sauvegarde des résultats.

    Attributes:
        base_url (str): URL de base du site web à scraper.
        data_extractor (DataExtractor): Instance de DataExtractor utilisée pour extraire les données.
    
    """
    def __init__(self, base_url):
        """ 
        Initialise ScraperManager avec une URL de base pour le scraping.

        Parameters:
            base_url (str): L'URL de base du site web à scraper.
        """
        self.base_url = base_url
        self.data_extractor = DataExtractor(self.base_url)
    
    def extract_all_books(self):
        """ 
        Orchestre le processus complet d'extraction des données des livres depuis le site web ciblé.

        Pour chaque catégorie trouvée sur le site, cette méthode extrait les URLs des livres et 
        collecte les données essentielles de chaque livre, y compris l'URL de l'image de couverture.
        Chaque livre est ensuite instancié en tant qu'objet Book, ses données étant collectées dans une 
        liste. Pour chaque catégorie, les images de couverture des livres sont sauvegardées localement,
        et les données des livres sont exportées dans un fichier CSV spécifique à la catégorie.

        Cette méthode s'appuie sur DataExtractor pour l'extraction des URLs des catégories, des URLs des livres
        par catégorie, et des données détaillées pour chaque livre. Elle utilise également la fonctionnalité de
        Book pour sauvegarder les images de couverture et utilise une méthode interne pour exporter les données
        des livres en CSV.

        Les fichiers CSV sont sauvegardés dans un répertoire 'datas_csv', et les images sont sauvegardées dans
        un répertoire 'book_images', tous deux créés à la racine du projet s'ils n'existent pas déjà. Les sous-répertoires
        pour les images suivent la structure de catégorisation des livres, permettant une organisation claire des fichiers.
        """
        # Étape 1: Extraire les URLs de toutes les catégories
        category_urls = self.data_extractor.extract_category_urls()
        
        # Étape 2: Pour chaque catégorie, extraire les URLs des livres
        for category_url in category_urls:
            self.data_extractor.set_url(category_url)
            book_urls = self.data_extractor.extract_book_urls_from_category()
            books = [] # Liste pour stocker les données des livres
            
            # Étape 3: Pour chaque URL de livre, extraire les données du livre et créer une instance de Book
            for book_url in book_urls:
                self.data_extractor.set_url(book_url)
                book_data = {
                    'product_book_url': book_url,
                    'title': self.data_extractor.extract_title(),
                    'upc': self.data_extractor.extract_upc(),
                    'price_incl_tax': self.data_extractor.extract_price_including_tax(),
                    'price_excl_tax': self.data_extractor.extract_price_excluding_tax(),
                    'availability': self.data_extractor.extract_availability(),
                    'review_rating': self.data_extractor.extract_review_rating(),
                    'category': self.data_extractor.extract_category(),
                    'image_url': self.data_extractor.extract_image_url(),
                    'product_description': self.data_extractor.extrac_product_description(),
                }
                book = Book(**book_data)
                books.append(book)
                book.save_cover_image() # Sauvegarde l'image de couverture pour chaque livre
                print(book_data)
            
            # À ce point, tous les livres d'une catégorie ont été traités
            # Sauvegarde les données des livres dans un fichier CSV   
            if books:
                self.save_books_to_csv(books, book_data['category'])



    def save_books_to_csv(self, books, category):
        """
        Sauvegarde les données d'une liste de livres dans un fichier CSV, organisé par catégorie.

        Parameters:
            books (list): Liste des instances de Book contenant les données à sauvegarder.
            category (str): La catégorie des livres, utilisée pour nommer le fichier CSV.
        
        """
        directory = 'datas_csv'
        category_cleaned = clean_filename(category)
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, f"{category_cleaned}.csv")

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = books[0].to_dict().keys()  # Utilise to_dict() pour obtenir les noms de champs
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow(book.to_dict())

    
    
    
  
