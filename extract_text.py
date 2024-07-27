import pytesseract
from PIL import Image
import os

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory containing ad images
image_dir = 'ads'

# Extract text from each image
ad_texts = []
for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    text = pytesseract.image_to_string(Image.open(image_path))
    ad_texts.append(text)

# Combine all ad texts into a single dataset
ad_text_dataset = "\n".join(ad_texts)

# Save the dataset to a file
with open('ad_text_dataset.txt', 'w') as file:
    file.write(ad_text_dataset)
