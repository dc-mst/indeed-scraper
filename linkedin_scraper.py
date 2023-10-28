import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from csv_writer import save_to_csv
from selenium_config import setup_linkedin

def scrape_linkedin():
    # URL of the job postings page
    url = 'https://www.linkedin.com/jobs/search?keywords=Programmatore&location=Bologna%2C%20Emilia%20Romagna%2C%20Italia&locationId=&geoId=105768355&f_TPR=&distance=10'

    # Initialize the browser using the setup_browser function from the selenium_config module
    browser = setup_linkedin(url)

    # Get the page source using Selenium
    page_source = browser.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Initialize the results list
    results = []

    job_postings = browser.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li div.base-card')
    main_window_handle = browser.current_window_handle  # Store the main window handle

    # Use an index-based loop
    for index in range(min(5, len(job_postings))):
    # for index in range(len(job_postings)):
        # Re-fetch job postings after navigating back to the main listings page
        job_postings = browser.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li div.base-card')
        job = job_postings[index]
        
        title = job.find_element(By.CSS_SELECTOR, 'h3').text.strip()
        href_value = job.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
        
        # Open a new tab
        browser.execute_script("window.open('', '_blank');")
        
        # Give the browser a moment to open the new tab
        time.sleep(5)
        
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