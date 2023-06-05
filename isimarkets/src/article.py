import requests
from bs4 import BeautifulSoup as bs

class Article:
    def __init__(self, url):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")        
        
        self.title = self.get_title()    
        self.body = self.get_body()

    def get_title(self) -> str:
        return self.soup.find(id="main-heading").text    

    def get_body(self) -> list:
        return [p.text for p in self.soup.find_all(attrs={"data-component":"text-block"})]    

if __name__=='__main__':
    parsed = Article('https://www.bbc.com/news/business-65790164')
    print(parsed.title)
    print(parsed.body)
