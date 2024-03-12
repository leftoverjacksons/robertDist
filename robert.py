from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time

# Specify the path to EdgeDriver and initialize the WebDriver
edge_driver_path = "C:/Users/jtking/Downloads/edgedriver_win64/msedgedriver.exe"
s = Service(edge_driver_path)
driver = webdriver.Edge(service=s)

# Example list of ZIP codes - replace with your actual list
zip_codes = ['30097', '10001', '90210']  # Add as many as you need

# Prepare a CSV file to store the data
with open('distributors.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the headers to the CSV file
    writer.writerow(['ZIP Code', 'Distributor Name', 'Address', 'Phone', 'Email', 'Website'])

    for zip_code in zip_codes:
        url = f"https://www.robertshaw.com/Find-Distributor/?category=1&zip={zip_code}&country=USA%20and%20Canada"
        driver.get(url)
        
        # Check for the presence of the search result container. 
        # This needs to be adjusted to the actual ID or class that encloses the search results.
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results-container'))  # Adjust to actual selector
            )
            
            # Find all blocks of distributor information
            distributor_blocks = driver.find_elements_by_css_selector('div.location-summary')  # Adjust to actual selector

            for block in distributor_blocks:
                details = block.text.split('\n')  # This will create a list of text items
                name = details[0]
                address = ' '.join(details[1:3])  # Assuming the address is two lines
                phone = details[3] if 'tel:' in details[3] else 'No phone'
                email = details[4] if '@' in details[4] else 'No email'
                website = details[5] if 'http' in details[5] else 'No website'

                # Write the distributor information to the CSV file
                writer.writerow([zip_code, name, address, phone, email, website])

        except TimeoutException as e:
            print(f"Timed out waiting for distributor information to load for ZIP code {zip_code}")
            print(str(e))
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

        # Be respectful and avoid hitting the server too rapidly
        time.sleep(2)

# Clean up by closing the Edge browser
driver.quit()
