import pandas as pd

# Load extracted text with appropriate encoding and delimiter handling
try:
    extracted_text_df = pd.read_csv('ad_text_dataset.txt', encoding='ISO-8859-1', on_bad_lines='skip')
    print("Extracted text data loaded successfully.")
except Exception as e:
    print(f"Error loading extracted text data: {e}")

# Load customer reviews with appropriate encoding and delimiter handling
try:
    customer_reviews_df = pd.read_csv('customer_reviews.csv', encoding='ISO-8859-1', on_bad_lines='skip')
    print("Customer reviews data loaded successfully.")
except Exception as e:
    print(f"Error loading customer reviews data: {e}")

# Combine both datasets
try:
    combined_df = pd.concat([extracted_text_df, customer_reviews_df.rename(columns={'review': 'text'})], ignore_index=True)
    print("Datasets combined successfully.")
except Exception as e:
    print(f"Error combining datasets: {e}")

# Save combined dataset
combined_csv_file = 'combined_dataset.csv'
try:
    combined_df.to_csv(combined_csv_file, index=False)
    print(f"Combined dataset has been saved to {combined_csv_file}.")
except Exception as e:
    print(f"Error saving combined dataset: {e}")
