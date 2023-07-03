# Zillow-Realtor-Data-Scraper

This repository contains Python scripts for web scraping real estate agent information from Zillow's website.

## Files

- `zillow_scraper.py`: This script includes classes and methods for scraping realtor profile links, retrieving agent information, and extracting professional details.
- `profiles.txt`: This text file contains partial URLs of realtor profiles on Zillow. The script reads these URLs and scrapes the corresponding information.

## Usage

1. Ensure that Python 3.x is installed on your system.
2. Install the required dependencies by running the command: `pip install requests beautifulsoup4`.
3. Modify the `profiles.txt` file by adding the desired partial URLs of realtor profiles from Zillow.
4. Run the `zillow_scraper.py` script to scrape agent information, retrieve professional details, and display the results in the console.

Please note that web scraping should be conducted responsibly and in accordance with the terms of service of the website you are scraping. Make sure to respect Zillow's terms of use and be mindful of any rate limits or restrictions they may have in place.

