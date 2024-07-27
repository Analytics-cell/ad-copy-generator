# ad-copy-generator
Fine Tuned GPT-2 for Advertising Campaigns

##Advertising Campaign Generator

This project provides a web application for generating advertising copy using a fine-tuned GPT-2 language model. The application is built using Flask, a lightweight WSGI web application framework in Python.
 Project Structure
 ## Download Required Files

Due to storage limitations, some large files are hosted externally. Please download the following files and place them in the appropriate directories:

- **Model Checkpoints**: [Download Link](https://drive.google.com/file/d/10qkPbKMrTbIBWfDiV89FDz41f0OIOkCm/view?usp=drive_link)
- **Optimizer pt**: [Download Link](https://drive.google.com/file/d/1RSWdbykHb7l1StKurYmSuFkXWv_SiWLr/view?usp=drive_link)

- app.py: The main Flask application script.
- generate_text.py: Script for loading the fine-tuned GPT-2 model and generating text.
- fine_tune_model.py: Script for fine-tuning the GPT-2 model on your dataset.
- prepare_dataset.py: Script for preparing the dataset for fine-tuning.
- combine_data.py: Script for combining extracted text and customer reviews into a single dataset.
- scrape_ads.py: Script for scraping ad images and text from specified websites.
- scrape_customers_reviews.py: Script for scraping customer reviews.
- templates/index.html: HTML template for the web interface.
- tokenized_datasets/: Directory where tokenized datasets are saved.
- results/**: Directory where fine-tuning results and checkpoints are saved.
- requirements.txt: List of required Python packages.
- gitignore: Specifies files and directories to be ignored by Git.
- ad_text_dataset.txt**: Text dataset for fine-tuning.
- customer_reviews.csv: CSV file containing customer reviews.
- combined_dataset.csv: Combined dataset of ad text and customer reviews.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Preparing the Dataset

1. **Combine Data:
    ```sh
    python combine_data.py
    ```

2. Prepare the Dataset:
    ```sh
    python prepare_dataset.py
    ```

### Fine-Tuning the Model

1. **Fine-tune the GPT-2 model:
    ```sh
    python fine_tune_model.py
    ```

### Running the Web Application

1. **Start the Flask application:**
    ```sh
    python app.py
    ```

2. **Access the application in your browser:**
    ```
    http://127.0.0.1:5000
    ```

### Generating Ad Copy

1. Navigate to the home page.
2. Enter a prompt and specify the maximum length for the generated ad copy.
3. Click "Generate" to receive the generated ad copy.

Files Description

- app.py: Initializes and runs the Flask web server.
- generate_text.py**: Contains the logic to load the fine-tuned model and generate text based on the input prompt.
- fine_tune_model.py: Handles the fine-tuning process for the GPT-2 model.
- prepare_dataset.py: Prepares the text data for model training.
- combine_data.py: Combines different datasets into a single dataset for training.
- scrape_ads.py: Script to scrape ad content from the web.
- scrape_customers_reviews.py: Script to scrape customer reviews.
- templates/index.html: HTML template for the user interface.
- requirements.txt: Lists the dependencies required for the project.
- tokenized_datasets/: Directory to store tokenized datasets.
- results/**: Directory to save model checkpoints and results.
- ad_text_dataset.txt: The dataset of advertising text used for training.
- customer_reviews.csv: CSV file containing customer reviews used in training.
- combined_dataset.csv: Combined dataset of ad text and customer reviews.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Hugging Face for the [Transformers library](https://github.com/huggingface/transformers).
- Flask for providing an easy-to-use web framework.
- The creators of the datasets used in training and fine-tuning the model.
- Collected data from bluebell ice-cream website: https://www.bluebell.com/ , WayBackMachine Internet Archived data: https://web.archive.org/ , Customer reviews site: https://www.shespeaks.com/memberreviewsdetails/2/140720/159885764/2/111




