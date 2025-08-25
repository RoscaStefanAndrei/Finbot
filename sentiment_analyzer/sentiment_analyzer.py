# sentiment_analyzer.py
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# --- My VADER Lexicon Customization ---
# I'm creating a new dictionary with financial-specific words and their sentiment scores.
# The scores range from -3.0 (extremely negative) to +3.0 (extremely positive).

# Updated financial_lexicon for sentiment_analyzer.py

financial_lexicon = {
    # --- Strongly Positive ---
    'bullish': 3.0,
    'soaring': 3.0,
    'surging': 3.0,
    'skyrocketed': 3.0,
    'explodes': 3.0,
    'booms': 3.0,
    'record-high': 3.0,
    'breakout': 2.5,
    'rally': 2.5,
    'outperforming': 2.5,
    'outperforms': 2.5,
    'rebound': 2.5,
    'growing': 2.5,
    'boosts': 2.5,
    'upside': 2.5,
    'momentum': 2.0, # New term
    'reaffirms': 1.5, # New term
    
    # --- Positive ---
    'gains': 2.0,
    'rises': 2.0,
    'climbs': 2.0,
    'jumps': 2.0,
    'growth': 2.0,
    'profitable': 2.0,
    'strong': 2.0,
    'upgraded': 1.5,
    'positive': 1.5,
    'stable': 1.0,
    'solid': 1.0,
    'investment': 1.5,
    'invests': 1.5,
    'deal': 1.5,
    'equity': 1.0,
    'acquisition': 2.0,
    'merger': 2.0,
    'expands': 1.5,
    'launches': 1.0,
    'outlook': 1.5,
    'target': 1.0,
    'stake': 1.0,
    'ups': 1.5,
    'outmaneuvered': 1.5,
    'buys': 1.5,
    'raises': 1.0,
    'optimistic': 1.5,
    'up': 1.0, # New term
    
    # --- Neutral/Mixed ---
    'volatile': 0.0,
    'uncertainty': -0.5,
    'mixed': -0.5,
    'speculation': 0.0,
    'analyst': 0.0,
    'forecast': 0.0,
    'expected': 0.0,
    'hovers': 0.0,
    
    # --- Negative ---
    'declines': -2.0,
    'falls': -2.0,
    'drops': -2.0,
    'losses': -2.0,
    'downgraded': -1.5,
    'weak': -1.5,
    'negative': -1.5,
    'struggles': -1.5,
    'warning': -1.0,
    'concern': -1.0,
    'debt': -1.0,
    'downside': -1.5,
    'cut': -1.5,
    'sued': -2.0,
    'down': -1.5, # New term
    
    # --- Strongly Negative ---
    'bearish': -3.0,
    'plunges': -3.0,
    'crashes': -3.0,
    'collapses': -3.0,
    'plummets': -3.0,
    'sinks': -3.0,
    'slump': -2.5,
    'tumbles': -2.5,
    'crisis': -2.5,
    'bankrupt': -2.5,
    'missed': -2.5,
    'overcapacity': -2.0,
    'crackdown': -2.5,
    'indebted': -2.0,
    'bloated': -2.0,
    'warning': -2.5,
    'steps down': -2.0
}
# --- Setup ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')

# I'm creating a new VADER analyzer and updating its lexicon with my custom words.
analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(financial_lexicon)

# --- My Existing Functions ---
# (The rest of your functions remain the same)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text and returns the compound score.
    """
    if not isinstance(text, str):
        return 0
    
    scores = analyzer.polarity_scores(text)
    return scores['compound']

def run_sentiment_analysis(input_df, output_path):
    """
    Performs sentiment analysis on a DataFrame and saves the results to a new CSV file.
    """
    if input_df.empty:
        print("DataFrame is empty, cannot perform sentiment analysis.")
        return

    input_df['sentiment_score'] = input_df['description'].apply(analyze_sentiment)
    
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