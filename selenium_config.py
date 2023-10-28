from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def setup_linkedin(url):
    # Determine the path to chromedriver
    current_directory = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(current_directory, 'chromedriver')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f'--binary-location={chromedriver_path}')

    browser = webdriver.Chrome(options=chrome_options)

    # Use Selenium to access the URL
    browser.get(url)
    
    return browser

def setup_indeed(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Set user-agent to mimic a regular browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Set window size
    chrome_options.add_argument("window-size=1920x1080")

    browser = webdriver.Chrome(options=chrome_options)


    # Use Selenium to access the URL
    browser.get(url)
    
    # Add a delay to allow JavaScript to load content
    time.sleep(5)  # You can adjust this value as needed

    # Optionally, wait for a specific element to appear (replace 'YOUR_ELEMENT' with an appropriate selector)
    # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "YOUR_ELEMENT")))

    return browser