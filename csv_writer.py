import os
import csv
from datetime import datetime

def get_existing_titles(filename):
    #Return a set of existing job titles from the CSV.
    if not os.path.isfile(filename):
        return set()

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return set(row["Job Title"] for row in reader)
    
def get_current_row_count(filename):
    #Return the current number of rows in the CSV, excluding the header.
    if not os.path.isfile(filename):
        return 0
    with open(filename, mode='r', encoding='utf-8') as file:
        return sum(1 for row in file) - 1  # Subtracting 1 for the header


def save_to_csv(data, filename="results.csv"):
    # Determine if file exists
    file_exists = os.path.isfile(filename)
    existing_titles = get_existing_titles(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write headers only if the file didn't exist
        if not file_exists:
            writer.writerow(["Row Number", "Timestamp", "Job Title", "Description", "Href"])
        
        row_number = get_current_row_count(filename)
        for item in data:
            # Skip writing if title already exists
            if item['title'] in existing_titles:
                continue
            
            # Get the current timestamp in the desired format
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            row_number += 1
            writer.writerow([row_number, timestamp, item['title'], item['description'], "https://it.indeed.com" + item['href']])

