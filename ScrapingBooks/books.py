from utils import clean_filename
import os, requests



class Book:
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
        """Renvoie les données du livre sous forme de dictionnaire."""
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
    
    def save_cover_image(self, base_directory='book_images'):
        category_cleaned = clean_filename(self.category)
        image_save_path = os.path.join(base_directory, category_cleaned, f"{self.upc}.jpg")

        response = requests.get(self.image_url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
            with open(image_save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Erreur de du téléchargement de l'image pour {self.upc}")

