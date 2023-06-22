import time
import threading
from createdb import create_db
from scraper_art import ScraperArt
from scraper_url import BBCScraper

def run_scraper(url):
    scraper = BBCScraper()
    scraper.run_scraper(url)
    scraper.close_scraper()

def main():
    create_db()

    thread_business = threading.Thread(target=run_scraper, args=('https://www.bbc.com/news/business',))
    thread_business.start()

    time.sleep(5)

    thread_technology = threading.Thread(target=run_scraper, args=('https://www.bbc.com/news/technology',))
    thread_technology.start()

    thread_business.join()
    thread_technology.join()

    ArtScraper = ScraperArt()
    ArtScraper.scrape_urls()

if __name__ == '__main__':
    main()
