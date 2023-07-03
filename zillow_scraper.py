import requests
from bs4 import BeautifulSoup
import time


class ZillowAgentPage:
    def __init__(self, url):
        self.url = url
        self.base_url = 'https://www.zillow.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.html_content = None

    def get_html_content(self):
        # Add a delay of 1 second before sending the request
        time.sleep(1)

        # Send a GET request to the agent's page URL using HTTPS
        try:
            response = requests.get(self.url, headers=self.headers)

            # Check the return code of the response
            if response.status_code == 200:
                # Retrieve the HTML content from the response
                self.html_content = response.content
            elif response.status_code == 403:
                print(f"Error 403: Forbidden - Access to {self.url} is denied.")
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {self.url}: {e}")

    def get_agent_info(self):
        if self.html_content is None:
            print('HTML content not available. Please call get_html_content() first.')
            return None, None

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(self.html_content, 'html.parser')

        name_div = soup.find('div', class_='StyledCard-c11n-8-91-4__sc-1w6p0lv-0 liOflQ')
        if name_div:
            name = name_div.find('h2', class_='Text-c11n-8-91-4__sc-aiai24-0 StyledHeading-c11n-8-91-4__sc-s7fcif-0 jnoIGe')
            if name:
                name = name.text.strip()
            else:
                name = 'N/A'
        else:
            name = 'N/A'

        address_div = soup.find('div', class_='Flex-c11n-8-91-4__sc-n94bjd-0 sc-fzolEj dmgWTu')
        if address_div:
            address = address_div.find('span', class_='Text-c11n-8-91-4__sc-aiai24-0 dOtWDO')
            if address:
                address = address.text.strip()
            else:
                address = 'N/A'
        else:
            address = 'N/A'

        return name, address

    def get_professional_info(self):
        if self.html_content is None:
            print('HTML content not available. Please call get_html_content() first.')
            return None

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(self.html_content, 'html.parser')

        professional_info = {}

        info_div = soup.find('dl', class_='CardSection-c11n-8-91-4__sc-10rcp1p-0 sc-fznWOq cjiVKu')
        if info_div:
            info_items = info_div.find_all('div', class_='Flex-c11n-8-91-4__sc-n94bjd-0 sc-fzolEj dmgWTu')
            for item in info_items:
                label = item.find('span', class_='Text-c11n-8-91-4__sc-aiai24-0 huQSxs')
                value = item.find('span', class_='Text-c11n-8-91-4__sc-aiai24-0 dOtWDO')
                if label and value:
                    label_text = label.text.strip().strip(':')
                    value_text = value.text.strip()
                    professional_info[label_text] = value_text

        return professional_info


class RealtorScraper:
    def __init__(self, url):
        self.url = url
        self.base_url = 'https://www.zillow.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def scrape_associated_realtors(self):
        try:
            # Add a delay of 1 second before sending the request
            time.sleep(1)

            response = requests.get(self.base_url + self.url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            associated_realtors_divs = soup.find_all('div', class_='Flex-c11n-8-91-4__sc-n94bjd-0 TOPuK')

            if associated_realtors_divs:
                print("Our associated members are:")
                count = 0
                for div in associated_realtors_divs:
                    realtor_name_elem = div.find('a')
                    if realtor_name_elem and realtor_name_elem.text:
                        count += 1
                        realtor_name = realtor_name_elem.text.strip()
                        if count % 2 != 0:
                            if count > 8:
                                break
                            print(realtor_name)

            else:
                print("Associated realtors div not found.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {self.base_url + self.url}: {e}")


# Read the URLs from the text file
with open('profiles.txt', 'r') as file:
    partial_urls = file.read().splitlines()

# Iterate over each partial URL and construct the full URL
for partial_url in partial_urls:
    # Construct the full URL
    full_url = 'https://www.zillow.com' + partial_url

    # Create an instance of the ZillowAgentPage class
    agent_page = ZillowAgentPage(full_url)

    # Get the HTML content
    agent_page.get_html_content()

    # Get the agent's information
    agent_name, agent_address = agent_page.get_agent_info()

    # Get the professional information
    professional_info = agent_page.get_professional_info()

    # Print the agent's information
    print('URL:', full_url)
    print('Name:', agent_name)
    print('Address:', agent_address)
    print('---')

    # Print the professional information
    print('Professional Information:')
    for label, value in professional_info.items():
        print(label + ':', value)

    # Create an instance of the RealtorScraper class
    scraper = RealtorScraper(partial_url)

    # Scrape the associated realtors
    scraper.scrape_associated_realtors()
    print('---')

