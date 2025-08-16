# main.py

import os
# Corrected import path for newscollector.py
from newscollector import run_news_collector
# Corrected import path for datacleaner.py
from datacleaner.datacleaner import run_data_cleaning
# Corrected import path for sentiment_analyzer.py
from sentiment_analyzer.sentiment_analyzer import run_sentiment_analysis

# --- Configuration & Setup ---

# You may need to adjust these paths based on your final folder structure.
NEWS_DATA_PATH = os.path.join(os.getcwd(), "project", "newscollector", "newsdata")
CLEANED_DATA_PATH = os.path.join(os.getcwd(), "datacleaner", "cleaned_data")
OUTPUT_FILE_PATH = os.path.join(CLEANED_DATA_PATH, "all_cleaned_news.csv")
SENTIMENT_OUTPUT_PATH = os.path.join(CLEANED_DATA_PATH, "news_with_sentiment.csv")


# main.py

# ... (imports and configuration) ...

def main():
    """
    Orchestrates the entire data pipeline from news collection to sentiment analysis.
    """
    print("--- Starting the Automated News Pipeline ---")

    # Step 1: Run the news collector
    print("\n[INFO] Starting news collection...")
    # This function doesn't return anything; it just saves the data.
    run_news_collector()

    # Step 2: Run the data cleaner
    print("\n[INFO] Starting data cleaning...")
    # This function returns the cleaned DataFrame.
    cleaned_df = run_data_cleaning()
    
    if cleaned_df.empty:
        print("[WARNING] No data to analyze. Exiting pipeline.")
        return
        
    # Step 3: Run the sentiment analyzer
    print("\n[INFO] Starting sentiment analysis...")
    # Pass the cleaned DataFrame AND the output path to the sentiment function.
    run_sentiment_analysis(cleaned_df, SENTIMENT_OUTPUT_PATH)

    print("\n--- Pipeline Complete. Ready for the next run. ---")

if __name__ == "__main__":
    main()