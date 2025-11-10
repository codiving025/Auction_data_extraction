import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from urllib.parse import urljoin
BASE_URL = "https://www.cricbuzz.com"
ARCHIVE_URL = f"{BASE_URL}/cricket-scorecard-archives"
current_year = datetime.now().year
years = range(2008, current_year + 1)
hrefs = {}
session = requests.Session()  # O(1) setup

for year in years:  # O(n)
    url = f"{ARCHIVE_URL}/{year}"

    soup = BeautifulSoup(session.get(url).text, "html.parser")

    # Find IPL link in current year, break after first found → O(1)
    a_tag = soup.find("a", href=lambda x: x and "indian-premier-league" in x)
    if a_tag:
        href = urljoin(BASE_URL, a_tag["href"])
        season_year = a_tag["href"].split("/")[3].split("-")[-1]
        hrefs[season_year] = href

session.close()  # O(1)

# Convert to DataFrame and save to CSV
pd.DataFrame(sorted(hrefs.items()), columns=["Year", "Link"]).to_csv("href2.csv", index=False)

print("✅ IPL links extracted successfully (O(n) complexity).")
