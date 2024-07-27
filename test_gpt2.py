from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the pre-trained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Add pad token to tokenizer and resize model embeddings
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Tokenize input
input_text = "Blue Bell Ice Cream is known for its"
inputs = tokenizer.encode_plus(input_text, return_tensors='pt', padding=True)
input_ids = inputs['input_ids']
attention_mask = inputs['attention_mask']

# Print the tokenized input and attention mask for debugging
print("Input IDs:", input_ids)
print("Attention Mask:", attention_mask)

# Generate text with adjusted parameters
output = model.generate(
    input_ids,
    attention_mask=attention_mask,
    max_length=50,
    num_return_sequences=1,
    pad_token_id=tokenizer.pad_token_id,
    do_sample=True,  # Enable sampling for better variety
    top_k=50,  # Use top_k sampling
    top_p=0.9,  # Use nucleus sampling with lower threshold
    temperature=0.7  #control randomness of predictions
)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
