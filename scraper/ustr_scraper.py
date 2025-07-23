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


def extract_article_text(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.content,"lxml")
    paragraphs=soup.select("div.field--name-body p")
    return "n".join(p.get_text(strip=True)for p in paragraphs)


def run_scraper():
    articles=[]
    for title, url in fetch_press_releases():
        print(f"Scrapping:{title}")
        content=extract_article_text(url)
        articles.append({
            "title": title,
            "url": url,
            "content": content,
            "scraped-at": datetime.utcnow().isoformat()
        })

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/ustr_press_releases.json", "w", encoding="utf-8") as f:
        json.dump(articles,f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to outputs/ustr_press_releases.json")  

if __name__ == "__main__":
    run_scraper()


     

        