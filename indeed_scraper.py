from bs4 import BeautifulSoup, NavigableString, Tag
from csv_writer import save_to_csv
from selenium_config import setup_indeed

def extract_with_spaces(element):
    texts = [child.get_text(separator=" ").strip() for child in element.children if isinstance(child, (NavigableString, Tag))]
    return ' '.join(texts).strip()

def scrape_indeed():
    # URL of the job postings page
    url = 'https://it.indeed.com/jobs?q=programmatore&l=Bologna%2C+Emilia-Romagna'

    # Initialize the browser using the setup_browser function from the selenium_config module
    browser = setup_indeed(url)

    # Get the page source using Selenium
    page_source = browser.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract job postings
    job_postings = soup.select('div.job_seen_beacon')

    results = []

    for job in job_postings:
        title = job.select_one('h2').text.strip()
        description = extract_with_spaces(job.select_one('table[role="presentation"]'))
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
