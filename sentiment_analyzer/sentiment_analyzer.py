# sentiment_analyzer.py
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# --- Setup ---
# Download the VADER lexicon if you haven't already
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# --- Main Functions ---

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text and returns the compound score.
    """
    if not isinstance(text, str):
        return 0  # Return a neutral score for non-string input
    
    scores = analyzer.polarity_scores(text)
    return scores['compound']

def run_sentiment_analysis(input_df, output_path):
    """
    Performs sentiment analysis on a DataFrame and saves the results to a new CSV file.
    """
    if input_df.empty:
        print("DataFrame is empty, cannot perform sentiment analysis.")
        return

    # Apply sentiment analysis to the 'description' column
    input_df['sentiment_score'] = input_df['description'].apply(analyze_sentiment)
    
    # Save the DataFrame with the new sentiment score
    input_df.to_csv(output_path, index=False)
    print(f"Sentiment analysis complete. File saved to {output_path}")

# --- Execution ---

if __name__ == "__main__":
    # Example usage if you want to run this file standalone
    base_path = os.path.join(os.getcwd(), "datacleaner", "cleaned_data")
    input_file = os.path.join(base_path, "all_cleaned_news.csv")
    output_file = os.path.join(base_path, "news_with_sentiment.csv")
    
    if os.path.exists(input_file):
        df = pd.read_csv(input_file)
        run_sentiment_analysis(df, output_file)
    else:
        print("Cleaned data file not found. Please run the datacleaner script first.")