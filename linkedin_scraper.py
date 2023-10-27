import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from csv_writer import save_to_csv

def scrape_linkedin():
    # Determine the path to chromedriver
    current_directory = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(current_directory, 'chromedriver')

    chrome_options = Options()
    chrome_options.add_argument(f'--binary-location={chromedriver_path}')

    browser = webdriver.Chrome(options=chrome_options)

    # URL of the job postings page
    url = 'https://www.linkedin.com/jobs/search?keywords=Programmatore&location=Bologna&position=1&pageNum=0'

    # Use Selenium to access the URL
    browser.get(url)

    # Get the page source using Selenium
    page_source = browser.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract job postings' links
    job_links = browser.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li div.base-card')

    results = []

    for link in job_links:
        # Click on the job link to access its details
        link.click()
        
        # Wait for the description to be loaded and become visible
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section.two-pane-serp-page__detail-view div.show-more-less-html__markup'))
        )

        # Parse the new page source with BeautifulSoup
        soup_detail = BeautifulSoup(browser.page_source, 'html.parser')

        title = soup_detail.select_one('h3.base-search-card__title').text.strip()
        description = soup_detail.select_one('section.two-pane-serp-page__detail-view div.show-more-less-html__markup').text.strip()
        href_value = link.get_attribute('href')
        
        results.append({
            'source': 'linkedin', 
            'title': title,
            'description': description,
            'href': href_value
        })

    # Save results to CSV
    save_to_csv(results)

    # Close the Selenium browser
    browser.quit()

    return results