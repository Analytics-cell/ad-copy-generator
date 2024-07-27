import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Specify the path where the model and tokenizer are saved
model_path = 'path_to_save_model'

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

# Add the padding token to the model's config
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.resize_token_embeddings(len(tokenizer))

print("Model and tokenizer loaded successfully.")

# Function to generate ad copy
def generate_ad(prompt, max_length=100):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)  # Set attention mask
    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,          # Enable sampling
        temperature=0.7,         # Adjust temperature
        top_k=50,                # Use top-k sampling
        top_p=0.9,               # Use top-p (nucleus) sampling
        repetition_penalty=1.2   # Apply repetition penalty
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
prompt = "my product tastes so good"
ad_copy = generate_ad(prompt)
print(ad_copy)
