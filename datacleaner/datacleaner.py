import pandas as pd
import os

"""
datacleaner.py

This script is a crucial part of my news data project. Its main purpose is to load
all the raw CSV files collected by my news collector script, clean and preprocess
the data, and then save the final, clean dataset to a single file for analysis.
"""

# --- Project Configuration & Setup ---

project_root = os.getcwd()

# I'll define the path to the raw news data, which is inside my 'newscollector' folder.
news_data_folder = os.path.join(project_root, "project", "newscollector", "newsdata")


cleaned_data_folder = os.path.join(project_root, "datacleaner", "cleaned_data")
os.makedirs(cleaned_data_folder, exist_ok=True)


# --- My Core Functions ---

def load_all_news_data(base_path):
    
    my_dfs = []
    # I'll use os.walk() to handle the directory traversal automatically.
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path)
                    my_dfs.append(df)
                    print(f"Loaded: {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
    
    if my_dfs:
        # I'll use ignore_index=True to get a clean index for the combined DataFrame.
        return pd.concat(my_dfs, ignore_index=True)
    
    print(f"No CSV files found in {base_path}. I need to check my news collector script!")
    return pd.DataFrame()


def clean_and_process_data(df):
    
    if df.empty:
        print("The DataFrame is empty, so there's nothing for me to clean.")
        return pd.DataFrame()

    print("\n--- Starting Data Cleaning and Preprocessing ---")
    initial_count = len(df)
    print(f"Initial row count: {initial_count}")

    # Step 1: I'm dropping rows that are missing critical information.
   
    df.dropna(subset=['title', 'publishedAt'], inplace=True)
    print(f"I dropped {initial_count - len(df)} rows with missing data.")
    initial_count = len(df)

    # Step 2: I'm removing duplicates.
   
    df.drop_duplicates(subset=['title', 'description'], inplace=True)
    print(f"I dropped {initial_count - len(df)} duplicate articles.")

    # Step 3: I'm converting the `publishedAt` column.
   
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    # If the conversion fails for a row, I'll drop it.
    df.dropna(subset=['publishedAt'], inplace=True)
    print("I've converted the 'publishedAt' column to datetime format and removed any invalid rows.")

    # Finally, I'm sorting the data by date so it's chronologically ordered.
    df.sort_values(by='publishedAt', inplace=True)

    print(f"\nFinal row count after cleaning: {len(df)}")
    print("--- Cleaning Complete ---")
    return df


# --- Main Execution ---

if __name__ == "__main__":
    # 1. My first step is to load all the news data I've collected.
    raw_df = load_all_news_data(news_data_folder)

    if not raw_df.empty:
        # 2. If I found data, I'll go ahead and clean it.
        cleaned_df = clean_and_process_data(raw_df)

        # 3. Finally, I'll save the cleaned data to a single CSV file
        # in the 'cleaned_data' folder for future use.
        output_file_path = os.path.join(cleaned_data_folder, "all_cleaned_news.csv")
        cleaned_df.to_csv(output_file_path, index=False)
        print(f"\nI've saved my cleaned data to: {output_file_path}")
    else:
        print("I found no raw data to process. I'm exiting now.")

