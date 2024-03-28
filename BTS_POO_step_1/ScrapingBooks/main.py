from scraper import DataExtractor
# Assure-toi que books.py est correctement implémenté et accessible
from books import Book

def main():
    base_url = "https://books.toscrape.com/"
    data_extractor = DataExtractor(base_url)

    # Extraction des URLs des catégories
    category_urls = data_extractor.extract_category_urls()
    print(f"Found {len(category_urls)} categories.")

    # Pour chaque catégorie, extraire les URLs des livres et les détails de chaque livre
    for category_url in category_urls:
        data_extractor.set_url(category_url)
        book_urls = data_extractor.extract_book_urls_from_category()
        print(f"Found {len(book_urls)} books in category {category_url}.")

        # Pour chaque livre, extraire et afficher les informations
        for book_url in book_urls:
            data_extractor.set_url(book_url)
            book_data = {
            'title': data_extractor.extract_title(),
            'upc': data_extractor.extract_upc(),
            'price_incl_tax': data_extractor.extract_price_including_tax(),
            'price_excl_tax': data_extractor.extract_price_excluding_tax(),
            'availability': data_extractor.extract_availability(),
            'review_rating': data_extractor.extract_review_rating(),
            'image_url': data_extractor.extract_image_url(),
            'category': data_extractor.extract_category(),
            'product_description': data_extractor.extrac_product_description(),
            # Assure-toi que tous les noms de clés ici correspondent à ceux dans __init__ de Book
}

            # Création d'une instance de Book avec les données extraites
            book = Book(**book_data)
            # Ici, tu pourrais sauvegarder les données du livre comme nécessaire
            print(book.to_dict())

if __name__ == "__main__":
    main()
