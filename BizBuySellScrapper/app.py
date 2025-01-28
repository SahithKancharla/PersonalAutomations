import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Generate a Google user agent
ua = UserAgent()
headers = {'User-Agent': ua.google}

# URL of the BizBuySell listings (you can modify this as needed)
url = 'https://www.bizbuysell.com'

# Send a GET request to the site
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the page!")
    print(response.text)
    
    # Parse the content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')


    # Extract specific data from the page (example: find all listing titles)
    listings = soup.find_all('a', class_='listing-title')  # Adjust class name as per site structure
    for listing in listings:
        title = listing.get_text(strip=True)
        print(title)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
