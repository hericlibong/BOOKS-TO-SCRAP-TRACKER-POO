
from scraper import Scraper






def main():


    scraper = Scraper("https://books.toscrape.com/")
    book_info = scraper.get_book_info("catalogue/a-light-in-the-attic_1000/index.html")
    print('title:',book_info.title)
    print('price:',book_info.price)
    print('avaibility:',book_info.availability )



if __name__=="__main__":
    main()