import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

BASE_URL="https://ustr.gov/"
PRESS_RELEASE_URL="https://ustr.gov/about-us/policy-offices/press-office/press-releases"

def fetch_press_releases():
    print("Fetching USTR press releases")
    response= requests.get(PRESS_RELEASE_URL)
    soup= BeautifulSoup(response.content,"lxml")

    article_links=[]
    for link in soup.select("div.view-content .views-row a"):
        href=link.get("href")
        title=link.get_text(strip=True)
        if any(term in title.lower() for term in ["tariff", "duty", "trade", "import", "export"]):
            full_url=BASE_URL + href
            article_links.append((title, full_url))

    return article_links        

        