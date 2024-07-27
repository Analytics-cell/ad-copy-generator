import requests
from bs4 import BeautifulSoup
import time


# Function to get HTML content of a webpage with a delay and retries
def get_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    for _ in range(5):  # Retry up to 5 times
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            time.sleep(2)  # Add a delay of 2 seconds between requests
            return response.text
        else:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            time.sleep(5)  # Wait for 5 seconds before retrying
    return None


# Function to parse and extract data from the "About Us" page
def scrape_about_us(url):
    html_content = get_html_content(url)
    if not html_content:
        return "Failed to fetch the About Us page"
    soup = BeautifulSoup(html_content, 'html.parser')
    about_us_section = soup.find('div', class_='columns small-12 medium-10 large-5 text-center medium-order-2')
    if about_us_section:
        return about_us_section.get_text(separator=' ', strip=True)
    return "No content found"


# Function to parse and extract data from the "Products" page
def scrape_products(url):
    html_content = get_html_content(url)
    if not html_content:
        return "Failed to fetch the Products page"
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []

    # Locate the specific product sections
    product_sections = soup.find_all('div', class_='listing-product')
    if not product_sections:
        print("No product sections found")
    for section in product_sections:
        product_items = section.find_all('div', class_='post-item_content')
        if not product_items:
            print("No product items found in section")
        for product in product_items:
            product_name_tag = product.find('a', class_='post-product__link')
            product_description_tag = product.find('div', class_='post-product__text')
            if product_name_tag and product_description_tag:
                product_name = product_name_tag.get_text(strip=True)
                product_description = product_description_tag.get_text(strip=True)
                products.append({
                    'name': product_name,
                    'description': product_description
                })
                print(f"Found product: {product_name}")  # Logging for debugging
            else:
                print("Failed to find product name or description")
            time.sleep(2)  # Add a delay of 2 seconds between processing each product
    return products


# URLs of the pages to scrape (replace with actual URLs)
about_us_url = 'https://www.bluebell.com/about-us/'
products_url = 'https://www.bluebell.com/our-products/'

# Scrape the content
about_us_content = scrape_about_us(about_us_url)
products_content = scrape_products(products_url)

# Print the scraped content
print("About Us Content:")
print(about_us_content)
print("\nProducts Content:")
if isinstance(products_content, str):  # If an error message is returned
    print(products_content)
else:
    for product in products_content:
        print(f"Name: {product['name']}, Description: {product['description']}")
