from transformers import GPT2Tokenizer
from datasets import Dataset
import pandas as pd

# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Load the combined dataset
try:
    combined_df = pd.read_csv('combined_dataset.csv', encoding='ISO-8859-1', on_bad_lines='skip')
    print("Combined dataset loaded successfully.")
except Exception as e:
    print(f"Error loading combined dataset: {e}")

# Ensure the text column is of type str
try:
    combined_df['text'] = combined_df['text'].astype(str)
    print("Converted text column to string successfully.")
except Exception as e:
    print(f"Error converting text column to string: {e}")

# Prepare the dataset for tokenization
try:
    dataset = Dataset.from_pandas(combined_df[['text']])
    print("Dataset prepared successfully.")
except Exception as e:
    print(f"Error preparing the dataset: {e}")

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

try:
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    print("Dataset tokenized successfully.")
except Exception as e:
    print(f"Error tokenizing the dataset: {e}")

# Save the tokenized dataset
try:
    tokenized_datasets.save_to_disk("tokenized_datasets")
    print("Tokenized dataset saved successfully.")
except Exception as e:
    print(f"Error saving the tokenized dataset: {e}")
