import os
import time
import requests
from bs4 import BeautifulSoup
from waybackpy import WaybackMachineCDXServerAPI
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed for this use case
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Set up logging
logging.basicConfig(filename='scrape_ads.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a directory to save ads
ads_dir = 'ads'
if not os.path.exists(ads_dir):
    os.makedirs(ads_dir)

# Define the target URL
url = "http://bluebell.com/"

# Custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to retry Wayback Machine snapshots request with exponential backoff
def fetch_snapshots_with_retry(url, retries=5, delay=5):
    for i in range(retries):
        try:
            wayback = WaybackMachineCDXServerAPI(url)
            snapshots = list(wayback.snapshots())  # Convert generator to list
            return snapshots
        except requests.exceptions.SSLError as ssl_error:
            logging.error(f"SSL error for fetching snapshots: {ssl_error}")
            if i < retries - 1:
                time.sleep(delay * (2 ** i))  # Exponential backoff
            else:
                raise
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {i + 1} failed for fetching snapshots: {e}")
            print(f"Attempt {i + 1} failed for fetching snapshots: {e}")
            if i < retries - 1:
                time.sleep(delay * (2 ** i))  # Exponential backoff
            else:
                raise

# Fetch Wayback Machine snapshots with retry
print("Fetching snapshots...")
snapshots = fetch_snapshots_with_retry(url)
print(f"Total snapshots fetched: {len(snapshots)}")

# Function to retry requests with exponential backoff and SSL verification
def fetch_url_with_retry(url, retries=5, delay=5, skip_on_file_not_found=True):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, verify=False)  # SSL verification disabled
            response.raise_for_status()
            return response
        except requests.exceptions.SSLError as ssl_error:
            logging.error(f"SSL error for {url}: {ssl_error}")
            if i < retries - 1:
                time.sleep(delay * (2 ** i))  # Exponential backoff
            else:
                raise
        except requests.exceptions.RequestException as e:
            if isinstance(e, FileNotFoundError) and skip_on_file_not_found:
                logging.error(f"File not found for {url}: {e}")
                print(f"File not found for {url}: {e}")
                return None  # Skip this URL
            logging.warning(f"Attempt {i + 1} failed for {url}: {e}")
            print(f"Attempt {i + 1} failed for {url}: {e}")
            if i < retries - 1:
                time.sleep(delay * (2 ** i))  # Exponential backoff
            else:
                raise

# Load already processed URLs from log file
processed_urls = set()
if os.path.exists('scrape_ads.log'):
    with open('scrape_ads.log') as log_file:
        for line in log_file:
            if 'INFO' in line and 'Processed' in line:
                processed_url = line.split('Processed: ')[1].strip()
                processed_urls.add(processed_url)

# Function to handle relative URLs
def ensure_absolute_url(base_url, link):
    if link.startswith('http'):
        return link
    if link.startswith('//'):
        return f"https:{link}"
    return f"https://web.archive.org{link}"

# Download ad images from all snapshots
for idx, snapshot in enumerate(snapshots, start=1):
    snapshot_url = snapshot.archive_url
    if snapshot_url in processed_urls:
        continue  # Skip already processed URLs
    try:
        print(f"Processing snapshot {idx}/{len(snapshots)}: {snapshot_url}")
        response = fetch_url_with_retry(snapshot_url)
        if response is None:
            logging.warning(f"Skipping snapshot due to fetch failure: {snapshot_url}")
            continue  # Skip to the next snapshot if the current one fails

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all images (you may need to adjust the selector based on the website's structure)
        images = soup.find_all('img')

        if not images:
            logging.info(f"No images found in snapshot: {snapshot_url}")

        for img in images:
            img_url = img.get('src')
            if img_url and 'ad' in img_url.lower():  # Ensure it's an ad image
                full_img_url = ensure_absolute_url(snapshot_url, img_url)
                try:
                    img_response = fetch_url_with_retry(full_img_url, skip_on_file_not_found=False)
                    if img_response is None:
                        logging.warning(f"Skipping image due to fetch failure: {full_img_url}")
                        continue
                    img_data = img_response.content
                    image_path = f'{ads_dir}/{img_url.split("/")[-1]}'
                    with open(image_path, 'wb') as handler:
                        handler.write(img_data)
                    print(f"Saved image {img_url.split('/')[-1]}")  # Print statement for debugging
                    logging.info(f"Saved image: {image_path}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Failed to fetch image {img_url}: {e}")
        logging.info(f"Processed: {snapshot_url}")
    except Exception as e:
        logging.error(f"Failed to fetch {snapshot_url}: {e}")
        print(f"Failed to fetch {snapshot_url}: {e}")

# List saved files
saved_files = os.listdir(ads_dir)
print(f"Total images saved: {len(saved_files)}")
for file in saved_files:
    print(file)

print("Script execution completed.")
