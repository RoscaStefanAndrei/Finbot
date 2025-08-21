import pandas as pd
import os
import numpy as np

# --- My Project Configuration & Setup ---

# I'm setting the paths here to ensure the script can find my news data and
# save the cleaned output in the correct locations, no matter where I run it from.
project_root = os.getcwd()
news_data_folder = os.path.join(project_root, "project", "newscollector", "newsdata")
cleaned_data_folder = os.path.join(project_root, "datacleaner", "cleaned_data")
os.makedirs(cleaned_data_folder, exist_ok=True)


# --- Core Functions ---

def load_all_news_data(base_path):
    """
    My function for loading all the raw news data.
    """
    all_dfs = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path)
                    all_dfs.append(df)
                    print(f"Loaded: {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    
    print(f"No CSV files found in {base_path}.")
    return pd.DataFrame()


def clean_and_process_data(df):
    """
    My function for cleaning the raw data.
    """
    if df.empty:
        print("The DataFrame is empty, so there's nothing for me to clean.")
        return pd.DataFrame()

    print("\n--- Starting Data Cleaning and Preprocessing ---")
    initial_count = len(df)
    print(f"Initial row count: {initial_count}")

    # I'm adding a step to replace empty descriptions with NaN so they can be dropped.
    df['description'] = df['description'].replace('', np.nan)
    df['title'] = df['title'].replace('', np.nan)
    
    # Step 1: I'm dropping rows that are missing critical information.
    df.dropna(subset=['title', 'description', 'publishedAt'], inplace=True)
    print(f"I dropped {initial_count - len(df)} rows with missing data.")
    initial_count = len(df)

    # I'm adding a new step to filter out low-quality articles with very short descriptions.
    df = df[df['description'].str.len() > 50]
    print(f"I dropped {initial_count - len(df)} articles with descriptions that were too short.")
    initial_count = len(df)

    # Step 2: I'm removing duplicates.
    df.drop_duplicates(subset=['title', 'description'], inplace=True)
    print(f"I dropped {initial_count - len(df)} duplicate articles.")

    # Step 3: I'm converting the `publishedAt` column.
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df.dropna(subset=['publishedAt'], inplace=True)
    print("I've converted the 'publishedAt' column to datetime format and removed any invalid rows.")

    df.sort_values(by='publishedAt', inplace=True)

    print(f"\nFinal row count after cleaning: {len(df)}")
    print("--- Cleaning Complete ---")
    return df
# --- My Orchestrator Function ---

def run_data_cleaning():
    """
    My function to orchestrate the entire data cleaning process.
    It loads raw data, cleans it, and returns a final DataFrame.
    """
    # 1. I'll load all news data from the collected CSVs.
    raw_df = load_all_news_data(news_data_folder)

    if not raw_df.empty:
        # 2. If I found data, I'll go ahead and clean it.
        cleaned_df = clean_and_process_data(raw_df)

        # 3. I'll save the cleaned data to a new CSV file.
        output_file_path = os.path.join(cleaned_data_folder, "all_cleaned_news.csv")
        cleaned_df.to_csv(output_file_path, index=False)
        print(f"\nI've saved my cleaned data to: {output_file_path}")

        # This is a critical step: I'm returning the DataFrame so the next script can use it.
        return cleaned_df
    else:
        print("I found no raw data to process. I'm exiting.")
        return pd.DataFrame()


# --- Main Execution ---

if __name__ == "__main__":
    # This block now just calls the main function, allowing it to be imported elsewhere.
    run_data_cleaning()