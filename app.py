from indeed_scraper import scrape_indeed
from linkedin_scraper import scrape_linkedin

def main():
    # Scrape Indeed
    indeed_results = scrape_indeed()

    # Scrape the second website
    linkedin_results = scrape_linkedin()

if __name__ == '__main__':
    main()