# The existing scrapers only allow for choosing one state with no additional information to choose from
# 
# 
# 
# 
# 

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Generate a random Google user agent
ua = UserAgent()
headers = {'User-Agent': ua.google}

# Target listings page for a specific state (modify as needed)
url = 'https://www.bizbuysell.com/{something}businesses-for-sale/'

# Send a GET request to fetch the listings page
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Successfully fetched the page!")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all business listings (adjust the class if needed)
    listings = soup.find_all('a', class_='diamond')

    if listings:
        print("\nFound Listings:")
        for listing in listings:
            title_tag = listing.find('h3', class_='title')  # Extract title
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = listing.get('href')  # Extract the link
                print(f"- {title} ({link})")

    else:
        print("No listings found. Check the class name or site structure.")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

