import os
import requests
import datetime
import pandas as pd
from dotenv import load_dotenv

# Load .env file
env_loaded = load_dotenv()
if not env_loaded:
    print("[ERROR] .env file not found or not loaded!")

# Check API key
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("[ERROR] API_KEY not found in environment.")
else:
    print(f"[DEBUG] API_KEY loaded: {API_KEY[:4]}***")

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

def get_news_for_company(company_name, ticker, days_ago=2):
    from_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')

    params = {
        "q": f"{company_name} OR {ticker} stock",
        "from": from_date,
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
            print(f"[INFO] No news found for {company_name} ({ticker})")
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

        # Save file in that folder
        filename = f"{ticker}_{company_name}.csv".replace(" ", "_")
        file_path = os.path.join(company_folder, filename)
        df.to_csv(file_path, index=False)
        print(f"[SUCCESS] {len(df)} articles saved for {company_name} -> {file_path}")

    except Exception as e:
        print(f"[ERROR] Exception occurred for {company_name}: {e}")

# Main loop
for company, ticker in companies.items():
    print(f"\n[INFO] Collecting news for {company} ({ticker})...")
    get_news_for_company(company, ticker)
