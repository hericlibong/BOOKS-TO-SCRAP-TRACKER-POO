

class Book:
    def __init__(self, title=None, upc=None, price_incl_tax=None, 
                 price_excl_tax=None, review_rating=None, category=None, 
                 image_url=None, product_description=None):
        self.title = title
        self.upc = upc
        self.price_incl_tax = price_incl_tax
        self.price_excl_tax = price_excl_tax
        self.review_rating = review_rating
        self.category = category
        self.image_url = image_url
        self.product_description = product_description

    def to_dict(self):
        """Renvoie les données du livre sous forme de dictionnaire."""
        return {
            'title': self.title,
            'upc': self.upc,
            'price_including_tax': self.price_incl_tax,
            'price_excluding_tax': self.price_excl_tax,
            'review_rating': self.review_rating,
            'category': self.category,
            'image_url': self.image_url,
            'product_description': self.product_description,
        }
