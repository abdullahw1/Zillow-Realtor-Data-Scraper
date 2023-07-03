import requests
from bs4 import BeautifulSoup

class RealtorLinkScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def scrape_realtor_links(self):
        print("Realtor Profile Links:")
        
        for page_num in range(2, 26):
            page_url = self.url + f"?page={page_num}"
            response = requests.get(page_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            realtor_links_divs = soup.find_all('div', class_='Flex-c11n-8-50-1__sc-n94bjd-0 Summary__StyledFlex-sc-130ry7i-0 hREGHr dRCSGX')

            if realtor_links_divs:
                for div in realtor_links_divs:
                    realtor_links = div.find_all('a')
                    for link in realtor_links:
                        realtor_url = link['href']
                        if not realtor_url.endswith("#reviews"):
                            print(realtor_url)
            else:
                print(f"No realtor profile divs found on page {page_num}.")

# URL of the page to scrape
url = "https://www.zillow.com/professionals/real-estate-agent-reviews/boulder-co/"

# Create an instance of the RealtorLinkScraper class
scraper = RealtorLinkScraper(url)

# Scrape the realtor profile links from multiple pages
scraper.scrape_realtor_links()

