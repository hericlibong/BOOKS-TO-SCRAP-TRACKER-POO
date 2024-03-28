# scraper_manager.py
from scraper import DataExtractor
from books import Book

class ScraperManager:
    def __init__(self, base_url):
        self.base_url = base_url
        self.data_extractor = DataExtractor(self.base_url)
    
    def extract_all_books(self):
        # Étape 1: Extraire les URLs de toutes les catégories
        category_urls = self.data_extractor.extract_category_urls()
        
        # Étape 2: Pour chaque catégorie, extraire les URLs des livres
        for category_url in category_urls:
            self.data_extractor.set_url(category_url)
            book_urls = self.data_extractor.extract_book_urls_from_category()
            
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
                self.save_book(book)
                print(book.to_dict())
    
    def save_book(self, book):
        # Méthode pour sauvegarder les données du livre
        # À implémenter selon les besoins (fichier CSV, base de données, etc.)
        pass
