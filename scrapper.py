'''
We only use this to populate out steam_workshop_mods_file with data
'''

import requests
from bs4 import BeautifulSoup
import json
import time

#URL for  Cities: Skylines mods
base_url = 'https://steamcommunity.com/workshop/browse/?appid=255710&requiredtags[]=Mod&p={}'

def get_mods_from_page(page_number):
    # Construct the URL for the current page
    url = base_url.format(page_number)
    
    # Make a request to the page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}")
        return {}
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all mod elements
    mod_elements = soup.find_all('div', class_='workshopItem')
    
    mods = {}
    for mod_element in mod_elements:
        # Extract mod name
        name_element = mod_element.find('div', class_='workshopItemTitle ellipsis')
        mod_name = name_element.text.strip() if name_element else 'Unknown'
        
        # Extract mod ID
        id_element = mod_element.find('a', class_='ugc')
        mod_id = id_element['data-publishedfileid'] if id_element else 'Unknown'
        
        # Add to mods dictionary
        mods[mod_id] = {'name': mod_name}
    
    return mods

def scrape_all_pages():
    all_mods = {}
    page_number = 1
    
    while True:
        mods = get_mods_from_page(page_number)
        
        if not mods:
            print(f"No more mods found on page {page_number}. Stopping.")
            break
        
        all_mods.update(mods)
        print(f"Scraped page {page_number}, found {len(mods)} mods")
        
        page_number += 1
        time.sleep(1)  # Adding a delay to avoid being blocked by Steam
    
    return all_mods

if __name__ == "__main__":
    # Scrape all pages
    mods = scrape_all_pages()
    
    # Create the final data structure
    data = {'mods': mods}
    
    # Save to a JSON file
    with open('steam_workshop_mods.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    print("Data saved to steam_workshop_mods.json")
