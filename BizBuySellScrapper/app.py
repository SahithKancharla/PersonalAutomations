# The existing scrapers only allow for choosing one state with no additional information to choose from
# So I want to provide an API that is able to atleast reach that level of information that anyone can use for free.
# This scrapper allows you to get all the elements, from multiple pages of a category.
# 
# This is a good baseline if you want tb build your own scraper.


import sys
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from bs4 import BeautifulSoup
import random
import logging
from pythonjsonlogger import jsonlogger

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Rate limiter (10 requests per minute)
rate_limiter = AsyncLimiter(10, 60)

# User-Agent list to prevent detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36',
    'Safari/17612.3.14.1.6 CFNetwork/1327.0.4 Darwin/21.2.0',
]

BASE_URL = "https://www.bizbuysell.com"

async def scrape_bizbuysell(url=None, cityname=None, number_of_pages = 1):
    cityname_part = f"{cityname.lower()}-" if cityname else ""
    
    if not url:   
        url = f'{BASE_URL}/{cityname_part}businesses-for-sale/'

    useragent = random.choice(USER_AGENTS)
    print(useragent + "\n")
    headers = {
        'User-Agent': useragent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
    }

    results = []
    async with aiohttp.ClientSession() as session:
        for page in range(1, number_of_pages + 1):
            paginated_url = f"{url}/{page}/"
            async with rate_limiter:
                try:
                    async with session.get(paginated_url, headers=headers, timeout=5) as response:
                        if response.status != 200:
                            logger.error(f"Failed to retrieve page {page}. Status code: {response.status}")
                            continue
                        
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        listings = soup.find_all('a', class_='diamond')

                        for listing in listings:
                            title_tag = listing.find('h3', class_='title')
                            if title_tag:
                                title = title_tag.get_text(strip=True)
                                link = listing.get('href')
                                results.append({"title": title, "link": link})
                    
                except asyncio.TimeoutError:
                    logger.error(f"Page {page} request timed out.")
                except Exception as e:
                    logger.error(f"Request failed on page {page}: {e}")

    return results if results else {"message": "No listings found."}

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    results = asyncio.run(scrape_bizbuysell(None, None, 2))
    print(results)

