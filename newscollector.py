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

# Companies to track
companies = {
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Tesla": "TSLA",
    "Meta": "META",
    "Alphabet": "GOOGL",
    "JPMorgan": "JPM",
    "ExxonMobil": "XOM",
    "Pfizer": "PFE"
}

# Folder structure
base_folder = os.path.join("project", "newscollector")
news_folder = os.path.join(base_folder, "newsdata")
os.makedirs(news_folder, exist_ok=True)
print(f"[DEBUG] News folder: {news_folder}")

# File to store the timestamp of the last successful run
last_run_file = os.path.join(base_folder, "last_run.txt")

# --- Main Functions ---

def get_news_for_company(company_name, ticker):
    """
    Fetches news articles for a given company from the last successful run time
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

    # If no last run time is found, default to fetching news from the last hour.
    if not from_date:
    # Default to a safe window within the 30-day limit
        from_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')

    to_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    params = {
        "q": f"{company_name} OR {ticker}", # Removed "stock" to broaden the search
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
            print(f"[ERROR] Failed to fetch news for {company_name} ({ticker}) — Status Code: {response.status_code}")
            print(f"[ERROR] Message: {response.text}")
            return

        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            print(f"[INFO] No new articles found for {company_name} ({ticker}) between {from_date} and {to_date}")
            return

        news_data = []
        for article in articles:
            news_data.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "source": article.get("source", {}).get("name")
            })

        df = pd.DataFrame(news_data)

        # Create folder for company
        company_folder = os.path.join(news_folder, company_name)
        os.makedirs(company_folder, exist_ok=True)

        # Append to the existing CSV file or create a new one
        filename = f"{ticker}_{company_name}.csv".replace(" ", "_")
        file_path = os.path.join(company_folder, filename)
        
        # Check if file exists to decide whether to write headers
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)
            
        print(f"[SUCCESS] {len(df)} new articles appended for {company_name} -> {file_path}")

    except Exception as e:
        print(f"[ERROR] Exception occurred for {company_name}: {e}")

# --- New Orchestrator Function ---

def run_news_collector():
    """
    Orchestrates the news collection for all companies and updates the last run time.
    """
    print(f"\n[INFO] Starting news collection at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    
    # Main loop to collect news for all companies
    for company, ticker in companies.items():
        print(f"\n[INFO] Collecting news for {company} ({ticker})...")
        get_news_for_company(company, ticker)

    # After all companies are processed, save the current time as the last run time
    with open(last_run_file, 'w') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    print("\n[INFO] News collection complete. Timestamp updated for next run.")

# --- Main Execution ---

if __name__ == "__main__":
    # This block now just calls the main function, allowing it to be imported elsewhere.
    run_news_collector()