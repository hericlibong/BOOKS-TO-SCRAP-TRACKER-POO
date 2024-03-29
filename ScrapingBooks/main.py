

from scraper_manager import ScraperManager

def main():
    """ 
    Point d'entrée principal du script de scraping.

    Initialise le gestionnaire de scraping avec l'URL de base du site à scraper,
    puis lance l'extraction de toutes les données des livres disponibles sur le site.
    """
    base_url = "https://books.toscrape.com/"
    scraper_manager = ScraperManager(base_url)
    scraper_manager.extract_all_books()
    

if __name__ == "__main__":
    main()

