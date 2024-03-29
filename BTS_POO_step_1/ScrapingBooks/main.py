

from scraper_manager import ScraperManager

def main():
    base_url = "https://books.toscrape.com/"
    scraper_manager = ScraperManager(base_url)
    scraper_manager.extract_all_books()
    

if __name__ == "__main__":
    main()

