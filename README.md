# news_scraper
This is a web scraper specifically designed to scrape URLs from the BBC News website. It utilizes the Selenium, BS4 and Requests libraries to automate web browser interactions.

## How to run:

1. Create your virtual environment
2. Change the directory to /src
3. Run "python main.py".

### Additional Notes

- The script uses a regular expression pattern (self.pattern) to filter the URLs to be scraped. You can modify this pattern to match your specific requirements.

- The script includes some JavaScript code (div_script) that is executed in the browser to remove certain elements from the page. You can modify this code if you want to customize the elements to remove.

- The maximum number of pages that the scraper will visit can be adjusted by modifying the self.num_pag variable in the process_page method.

### Tree
.
├── data
├── requirements.txt
├── src
└── utils
