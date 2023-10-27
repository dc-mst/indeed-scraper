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

    # Extract job postings' div elements
    job_divs = browser.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li div.base-card')

    results = []

    for div in job_divs:
        # Use JavaScript to click on the div to access its details
        browser.execute_script("arguments[0].click();", div)
        
        # Wait for the description to be loaded and become visible
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section.two-pane-serp-page__detail-view div.show-more-less-html__markup'))
        )

        # Parse the new page source with BeautifulSoup
        soup_detail = BeautifulSoup(browser.page_source, 'html.parser')

        title = soup_detail.select_one('h3.base-search-card__title').text.strip()
        description = soup_detail.select_one('section.two-pane-serp-page__detail-view div.show-more-less-html__markup').text.strip()
        
        # Extract the href attribute from the child anchor element of the div
        link = div.find_element(By.TAG_NAME, 'a')
        href_value = link.get_attribute('href')

        # Debug print statement
        if href_value is None:
            print("DEBUG: Found a div with no href. Div's outerHTML:", div.get_attribute('outerHTML'))

        results.append({
            'source': 'linkedin', 
            'title': title,
            'description': description,
            'href': href_value
        })

        # If needed, you can go back to the original listings page using: browser.back()

        

    # Save results to CSV
    save_to_csv(results)

    # Close the Selenium browser
    browser.quit()

    return results