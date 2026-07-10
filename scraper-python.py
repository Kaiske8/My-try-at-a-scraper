# scraper-python.py
# A line-by-line learning version of the scraper.

import re
import requests
from bs4 import BeautifulSoup


# Step 1: download the page from the website
def download_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


# Step 2: read the HTML and pull out the data we want
def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")

    # Get the page title
    title = soup.title.get_text(strip=True) if soup.title else ""

    # Get all visible text from the page
    text = soup.get_text("\n", strip=True)

    # Find DAE values in the text
    dae_matches = re.findall(r"DAE\s*\(%\)\s*([0-9,]+)\s*%", text, re.IGNORECASE)

    # Find monthly payment values in the text
    monthly_matches = re.findall(r"Rata\s+lunar[aă]?\s*([0-9.,]+)", text, re.IGNORECASE)

    # Combine them into a list of offers
    offers = []
    for dae, monthly in zip(dae_matches, monthly_matches):
        offers.append({"dae": dae, "monthly": monthly})

    return {
        "title": title,
        "offers": offers,
    }


# Step 3: run the two steps together
def scrape(url="https://www.finzoom.ro/credite/ipotecare/"):
    html = download_page(url)
    return parse_page(html)


# Step 4: run the scraper when the file is executed
if __name__ == "__main__":
    result = scrape()
    print("TITLE:", result["title"])
    print("OFFERS FOUND:", len(result["offers"]))
    for offer in result["offers"][:10]:
        print(f"DAE: {offer['dae']}% | Monthly: {offer['monthly']}")

