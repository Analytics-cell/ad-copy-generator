import requests
from bs4 import BeautifulSoup
import csv
import time


# Function to fetch HTML content with retries and delay
def get_html_content(url, retries=3, delay=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    for _ in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}, status code: {response.status_code}. Retrying...")
            time.sleep(delay)
    return None


# Function to parse and extract reviews from a single page
def parse_reviews(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    reviews = []

    review_elements = soup.find_all('div', class_='ss_review_body')
    for review_element in review_elements:
        review_text = review_element.find('p').get_text(strip=True)
        reviews.append(review_text)

    return reviews


# Function to get the URL for the next page
def get_next_page_url(soup):
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        current_page = pagination.find('li', class_='active')
        if current_page:
            next_page_tag = current_page.find_next_sibling('li')
            if next_page_tag:
                next_page_link = next_page_tag.find('a', class_='page-link')
                if next_page_link and 'href' in next_page_link.attrs:
                    return next_page_link['href']
    print("Next page link not found.")
    return None


# Main function to scrape all reviews
def scrape_all_reviews(base_url, start_url):
    all_reviews = []
    url = start_url

    while url:
        print(f"Fetching URL: {url}")
        html_content = get_html_content(url)
        if not html_content:
            print(f"Failed to get content from URL: {url}")
            break

        reviews = parse_reviews(html_content)
        all_reviews.extend(reviews)

        soup = BeautifulSoup(html_content, 'html.parser')
        next_page_relative_url = get_next_page_url(soup)
        if next_page_relative_url:
            url = base_url + next_page_relative_url
        else:
            url = None

        print(f"Scraped {len(reviews)} reviews from {url}")
        time.sleep(2)  # Delay between page requests

    return all_reviews


# Base URL and initial URL
base_url = 'https://www.shespeaks.com'
start_url = 'https://www.shespeaks.com/memberreviewsdetails/1/140720/159885764/2/111'

# Scrape all reviews
reviews = scrape_all_reviews(base_url, start_url)

# Save reviews to a CSV file
csv_file = 'customer_reviews.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for review in reviews:
        writer.writerow({'review': review})

print(f"Scraped a total of {len(reviews)} reviews. Data has been stored in {csv_file}")
