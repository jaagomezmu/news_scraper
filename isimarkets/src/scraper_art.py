import os
import json
import sqlite3
from sqlite3 import Error

from article import Article

class ScraperArt:
    def __init__(self):
        self.data_dir = os.path.join(os.path.abspath(
            os.path.join(os.getcwd(), os.pardir)), 'data')
        self.db_path = os.path.join(self.data_dir, 'urls.db')

    def scrape_urls(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT id, url FROM urls WHERE processed == 0;"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                id = row[0]
                url = row[1]
                self.scrape_url(id, url)
                update_query = "UPDATE urls SET processed = 1 WHERE id = ?"
                cursor.execute(update_query, (id,))
                conn.commit()
        except Error as e:
            print(f"Error retrieving URLs from the database: {e}")
            pass
        finally:
            if conn:
                conn.close()

    def scrape_url(self, id, url):
        try:
            instance = Article(url)
            data = {
                'title' : instance.title,
                'body' : instance.body
            }
            file_name = str(id) + '.json'
            file_path = os.path.join(self.data_dir, file_name)
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
        except:
            pass
        
if __name__ == '__main__':
    ArtScraper = ScraperArt()
    ArtScraper.scrape_urls()
