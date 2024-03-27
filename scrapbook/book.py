class Book:
    """Create book"""
    def __init__(self, title, price,  availability):
        self.title = self.clean_title(title)
        self.price = self.clean_price(price)
        self.availability = self.clean_avaibility(availability)


    @staticmethod
    def clean_title(title):
        title = title.lower()
        return title
        
    @staticmethod
    def clean_price(price):
        price_numeric = price.replace('£', '')
        try:
            return float(price_numeric)
        except ValueError:
            print("Erreur lors de la conversion du prix en nombre")
            return None
    
    @staticmethod
    def clean_avaibility(availability):
        num_available = availability.replace('In stock', '').replace('(', '').replace(')', '').replace('available', '').strip()
        return int(num_available)

     