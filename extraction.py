import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# ==============================
# Read all IPL seasons
# ==============================
df = pd.read_csv("href2.csv")
df['SquadLink'] = df['Link'].apply(lambda x: x.replace('matches', 'squads'))
# ==============================
# Chrome Setup
# ==============================
options = Options()
# comment out headless if you want to watch the browser run
# options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 25)

# ==============================
# Function: scrape_ipl_squads
# ==============================
def scrape_ipl_squads(url, year):
    print(f"\n🏏 Opening {url} ({year})")
    driver.get(url)
    time.sleep(5)

    all_players = []

    # Wait for team sidebar to appear (new Cricbuzz React layout)
    try:
        wait.until(lambda d: "Super Kings" in d.page_source or "Royals" in d.page_source)
    except:
        print(f"⚠️ Sidebar not found for {year}, skipping.")
        return []

    # Find team names
    team_elements = driver.find_elements(By.XPATH, "//div[contains(@class,'cursor-pointer')]/span[1]")
    if not team_elements:
        print(f"⚠️ No teams found for {year} — possibly old layout or page not available.")
        return []

    print(f"✅ Found {len(team_elements)} teams for {year}")

    # Loop through teams
    for i in range(len(team_elements)):
        try:
            team_elements = driver.find_elements(By.XPATH, "//div[contains(@class,'cursor-pointer')]/span[1]")
            team_name = team_elements[i].text.strip()
            if not team_name:
                continue

            print(f"➡️ Clicking team: {team_name}")
            driver.execute_script("arguments[0].scrollIntoView(true);", team_elements[i])
            driver.execute_script("arguments[0].click();", team_elements[i])
            time.sleep(4)

            # Wait for players to appear
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.fullscreen-container a[href*='/profiles/']")))
            except:
                print(f"⚠️ No player cards loaded for {team_name}")
                continue

            cards = driver.find_elements(By.CSS_SELECTOR, "div.fullscreen-container a[href*='/profiles/']")
            print(f"   ↳ {len(cards)} players found")

            for c in cards:
                try:
                    name = c.find_element(By.CSS_SELECTOR, "span.hover\\:underline").text.strip()
                except:
                    name = ""
                try:
                    role = c.find_element(By.CSS_SELECTOR, "p.text-cbTxtSec.tb\\:text-sm").text.strip()
                except:
                    role = ""
                try:
                    img = c.find_element(By.TAG_NAME, "img").get_attribute("src")
                except:
                    img = ""
                profile = c.get_attribute("href")

                all_players.append({
                    "Year": year,
                    "Team": team_name,
                    "Player": name,
                    "Role": role,
                    "Image": img,
                    "Profile_URL": profile,
                    "Source_URL": url
                })

        except Exception as e:
            print(f"⚠️ Error fetching team {team_name}: {e}")
        time.sleep(2)

    print(f"🎯 Extracted total {len(all_players)} players for {year}")
    return all_players


# ==============================
# Loop Through All Years
# ==============================
all_players = []
for _, row in df.iterrows():
    year = row['Year']
    url = row['SquadLink']
    try:
        players = scrape_ipl_squads(url, year)
        all_players.extend(players)
    except Exception as e:
        print(f"⚠️ Failed for {year}: {e}")
    time.sleep(3)

# ==============================
# Save to CSV
# ==============================
output_file = "ipl_all_years_squads.csv"
pd.DataFrame(all_players).to_csv(output_file, index=False, encoding="utf-8-sig")

driver.quit()
print(f"\n🏆 Done! Extracted total {len(all_players)} players across all years.")
print(f"📁 Data saved to → {output_file}")
