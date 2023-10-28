import os
import time
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
    url = 'https://www.linkedin.com/jobs/search?keywords=programmatore&location=Bologna'

    # Use Selenium to access the URL
    browser.get(url)

    # Get the page source using Selenium
    page_source = browser.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Initialize the results list
    results = []

    job_postings = browser.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li div.base-card')

    main_window_handle = browser.current_window_handle  # Store the main window handle

    # Use an index-based loop
    # for index in range(len(job_postings)):
    for index in range(4):  # This will only process a specific number of job postings
        # Re-fetch job postings after navigating back to the main listings page
        job_postings = browser.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li div.base-card')
        job = job_postings[index]
        
        title = job.find_element(By.CSS_SELECTOR, 'h3').text.strip()
        href_value = job.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
        
        # Open a new tab
        browser.execute_script("window.open('', '_blank');")
        
        # Give the browser a moment to open the new tab
        time.sleep(3)
        
        if len(browser.window_handles) > 1:  # Check if the new tab is open
            # Switch to the new tab
            browser.switch_to.window(browser.window_handles[1])
            
            # Navigate to the detailed job description page in the new tab
            browser.get(href_value)
            
            try:
                # Wait for and click the "show more" button
                show_more_button = WebDriverWait(browser, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.show-more-less-html__button'))
                )
                if show_more_button:
                    show_more_button.click()
                
                # Extract the detailed description
                description_section = WebDriverWait(browser, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'section.show-more-less-html'))
                )
                description = description_section.text.strip().replace('\n', ' ').replace('Show less', '')

                results.append({
                    'source': 'linkedin', 
                    'title': title,
                    'description': description,
                    'href': href_value
                })

            except Exception as e:
                print(f"Could not expand the description for job {title}. Error: {e}")
                results.append({
                    'source': 'linkedin', 
                    'title': title,
                    'description': 'Description not available.',
                    'href': href_value
                })

            # Close the new tab
            browser.close()
            
            # Switch back to the main tab
            browser.switch_to.window(main_window_handle)
        else:
            print(f"Could not open the new tab for job {title}.")
            results.append({
                'source': 'linkedin', 
                'title': title,
                'description': 'Description not available due to navigation issues.',
                'href': href_value
            })

    # Save results to CSV
    save_to_csv(results)

    # Close the Selenium browser
    browser.quit()

    return results