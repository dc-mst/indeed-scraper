import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from csv_writer import save_to_csv

def scrape_indeed():
    # Determine the path to chromedriver
    current_directory = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(current_directory, 'chromedriver')

    chrome_options = Options()
    chrome_options.add_argument(f'--binary-location={chromedriver_path}')

    browser = webdriver.Chrome(options=chrome_options)

    # URL of the job postings page
    url = 'https://it.indeed.com/jobs?q=programmatore&l=Bologna%2C+Emilia-Romagna'

    # Use Selenium to access the URL
    browser.get(url)

    # Get the page source using Selenium
    page_source = browser.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract job postings
    job_postings = soup.select('div.job_seen_beacon')

    results = []

    for job in job_postings:
        title = job.select_one('h2').text.strip()
        description = job.select_one('table[role="presentation"]').text.strip()
        a_element = job.select_one('h2 a[href]')
        href_value = a_element['href']
        
        results.append({
            'source': 'indeed', 
            'title': title,
            'description': description,
            'href': href_value
        })

    # Save results to CSV
    save_to_csv(results)

    # Close the Selenium browser
    browser.quit()

    return results