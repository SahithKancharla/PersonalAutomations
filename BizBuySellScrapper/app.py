# The existing scrapers only allow for choosing one state with no additional information to choose from
# So I want to provide an API that is able to atleast reach that level of information that anyone can use for free.
# 
# 
# 
# 


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

async def scrape_bizbuysell(cityname=None, numberofpages = 1):
    cityname_part = f"{cityname.lower()}-" if cityname else ""
    
    url = f'https://www.bizbuysell.com/{cityname_part}businesses-for-sale/'
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


    async with rate_limiter:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=2) as response:
                    if response.status != 200:
                        return {"error": f"Failed to retrieve the page. Status code: {response.status}"}
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    listings = soup.find_all('a', class_='diamond')
                    
                    results = []
                    for listing in listings:
                        title_tag = listing.find('h3', class_='title')
                        if title_tag:
                            title = title_tag.get_text(strip=True)
                            link = listing.get('href')
                            results.append({"title": title, "link": link})
                    
                    return results if results else {"message": "No listings found."}
        except asyncio.TimeoutError:
            return {"error": "Request timed out. The website might be down or slow."}
        except Exception as e:
            return {"error": f"Request failed: {e}"}

if __name__ == '__main__':
    # cityname = input("Enter city name (or press enter to skip): ").strip()
    # cityname = cityname.replace(" ", "-").lower() if cityname else None
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    results = asyncio.run(scrape_bizbuysell())
    print(results)

