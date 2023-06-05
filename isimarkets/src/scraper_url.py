import os
import re
import time
import sqlite3
from sqlite3 import Error
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

class BBCScraper:
    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chromedriver_path = os.path.join(os.path.dirname(__file__), '../utils/chromedriver')
        
        self.driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
        self.pattern = r"https://www\.bbc\.com/news/(?!.*-.*-.*\/)(?=.*-[\w]+$)(?![^#]*#)(?!.*\?).*"
        self.urls_saved = set()
        self.new_urls = []
        self.paginator = True
        self.num_pag = 1

        self.data_dir = os.path.join(os.path.abspath(
            os.path.join(os.getcwd(), os.pardir)), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.db_path = os.path.join(self.data_dir, 'urls.db')

    def start_scraper(self, url):
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(20)

        div_script = '''
        var navElements = document.querySelectorAll('nav');
        for (var i = 0; i < navElements.length; i++) {
            navElements[i].remove();
        }

        var headerElements = document.querySelectorAll('header');
        for (var i = 0; i < headerElements.length; i++) {
            headerElements[i].remove();
        }

        var footerElements = document.querySelectorAll('footer');
        if (footerElements) {
            footerElements.forEach(function(element) {
                element.remove();
            });
        }

        var div1_1 = document.querySelector('div[role="region"][aria-labelledby="nw-c-Features&Analysis__title"]');
        if (div1_1)
            div1_1.remove();

        var div1_2 = document.querySelector('div[role="region"][aria-labelledby="nw-c-Specialreports__title"]');
        if (div1_2)
            div1_2.remove();

        var div1_3 = document.querySelector('div[role="region"][aria-labelledby="nw-c-Watch/Listen__title"]');
        if (div1_3)
            div1_3.remove();
        '''
        self.driver.execute_script(div_script)

    def process_page(self):
        urls = self.driver.find_elements(By.TAG_NAME, 'a')
        for url in urls:
            href = url.get_attribute('href')
            if re.match(self.pattern, href) and href not in self.urls_saved:
                self.new_urls.append(href)
                self.urls_saved.add(href)
                # print(self.new_urls)

        while True:
            try:
                next_link = self.driver.find_element(By.XPATH, "//a[@rel='next']")
                if next_link.is_enabled() and self.num_pag <= 50:
                    next_link.click()
                    time.sleep(2)
                    print("The 'next' link is enabled, num_page: {}".format(self.num_pag))
                    self.num_pag += 1
                    break
                else:
                    print("The 'next' link is not enabled.")
                    self.paginator = False
                    break
            except:
                print("The 'next' link was not found or is not clickable.")
                self.paginator = False
                break


    def save_urls_to_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            print("Connected!")
            new_urls_filtered = [url for url in self.new_urls if url not in self.get_saved_urls_from_db(conn)]
            query = "INSERT INTO urls (url) VALUES (?)"
            cursor.executemany(query, [(url,) for url in new_urls_filtered])
            conn.commit()
            print("URLs stored in the database")
        except Error as e:
            print(f"Error saving the URLs in the database: {e}")
        finally:
            if conn:
                conn.close()

    def get_saved_urls_from_db(self, conn):
        cursor = conn.cursor()
        query = "SELECT url FROM urls"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def run_scraper(self, url):
        self.start_scraper(url)

        while self.paginator:
            try:
                time.sleep(3)
                self.process_page()
            except:
                break

        self.save_urls_to_db()
        print('Ready!')

    def close_scraper(self):
        self.driver.quit()


if __name__ == '__main__':
    scraper = BBCScraper()
    scraper.run_scraper('https://www.bbc.com/news/technology')
    scraper.close_scraper()
