import os
import requests
import datetime
import pandas as pd
from dotenv import load_dotenv

# --- Configuration & Setup ---

# Load .env file
env_loaded = load_dotenv()
if not env_loaded:
    print("[ERROR] .env file not found or not loaded!")

# Check API key
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("[ERROR] API_KEY not found in environment.")

# Sectors to track with relevant search terms
# This is a much more powerful way to get raw market data.
sectors = {
    "Technology": ["artificial intelligence", "AI", "semiconductors", "cloud computing", "fintech"],
    "Automotive": ["electric vehicles", "EV", "self-driving", "robotaxi"],
    "Finance": ["banking", "investment", "capital markets", "stock market"],
    "Healthcare": ["biotech", "pharmaceuticals", "drug discovery", "medical devices"],
    "Energy": ["oil and gas", "renewable energy", "solar", "wind power", "drilling"]
}

# Folder structure
base_folder = os.path.join("project", "newscollector")
news_folder = os.path.join(base_folder, "newsdata")
os.makedirs(news_folder, exist_ok=True)
print(f"[DEBUG] News folder: {news_folder}")

# File to store the timestamp of the last successful run
last_run_file = os.path.join(base_folder, "last_run.txt")

# --- Main Functions ---

def get_news_for_sector(sector_name, search_terms):
    """
    Fetches news articles for a given sector from the last successful run time
    up to the present, and saves them to a CSV file.
    """
    
    # 1. Determine the time window for news search
    from_date = None
    if os.path.exists(last_run_file):
        with open(last_run_file, 'r') as f:
            try:
                from_date = f.read().strip()
            except Exception:
                pass  # If file is empty or corrupted, we'll start fresh.

    if not from_date:
        from_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')

    to_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # The search query now uses a combination of terms for the sector
    q = " OR ".join(search_terms)

    params = {
        "q": q,
        "from": from_date,
        "to": to_date,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": API_KEY,
        "domains": "cnbc.com,marketwatch.com,yahoo.com,reuters.com,seekingalpha.com,wsj.com"
    }

    try:
        response = requests.get("https://newsapi.org/v2/everything", params=params)
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch news for {sector_name} — Status Code: {response.status_code}")
            print(f"[ERROR] Message: {response.text}")
            return

        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            print(f"[INFO] No new articles found for {sector_name} between {from_date} and {to_date}")
            return

        news_data = []
        for article in articles:
            news_data.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "source": article.get("source", {}).get("name"),
                "sector": sector_name
            })

        df = pd.DataFrame(news_data)

        # Create a single folder for all news
        sector_folder = os.path.join(news_folder, "sectors")
        os.makedirs(sector_folder, exist_ok=True)

        # Append to the existing CSV file or create a new one
        filename = f"{sector_name}.csv".replace(" ", "_")
        file_path = os.path.join(sector_folder, filename)
        
        # Check if file exists to decide whether to write headers
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)
            
        print(f"[SUCCESS] {len(df)} new articles appended for {sector_name} -> {file_path}")

    except Exception as e:
        print(f"[ERROR] Exception occurred for {sector_name}: {e}")

# --- New Orchestrator Function ---

def run_news_collector():
    """
    Orchestrates the news collection for all companies and updates the last run time.
    """
    print(f"\n[INFO] Starting sector-based news collection at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    
    # Main loop to collect news for all sectors
    for sector_name, search_terms in sectors.items():
        print(f"\n[INFO] Collecting news for {sector_name}...")
        get_news_for_sector(sector_name, search_terms)

    # After all sectors are processed, save the current time as the last run time
    with open(last_run_file, 'w') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    print("\n[INFO] Sector news collection complete. Timestamp updated for next run.")

# --- Main Execution ---

if __name__ == "__main__":
    run_news_collector()