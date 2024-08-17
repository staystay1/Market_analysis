import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time


def get_all_categories(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = []
    category_section = soup.find('ul', class_='nav-list')
    category_links = category_section.find_all('a')[1:]  
    for link in category_links:
        category_name = link.text.strip()
        category_url = urljoin(base_url, link['href'])
        categories.append((category_name, category_url))
    
    return categories


def get_book_links(category_url):
    book_links = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_containers = soup.find_all('article', class_='product_pod')
        for container in book_containers:
            relative_link = container.find('h3').find('a')['href']
            full_link = urljoin(category_url, relative_link)
            book_links.append(full_link)

        
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.find('a')['href']
            category_url = urljoin(category_url, next_page_url)
        else:
            category_url = None  
    return book_links

def extract_image_url(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        image_url = urljoin(book_url, soup.find('img')['src']) if soup.find('img') else 'N/A'
        
        print(f"Successfully extracted image URL from: {book_url}")
    
    except Exception as e:
        print(f"Error extracting image URL from {book_url}: {e}")
        return None
    
    return image_url

base_url = 'http://books.toscrape.com/'
categories = get_all_categories(base_url)

image_urls = []

for category_name, category_url in categories:
    print(f"Processing category: {category_name}")
    book_links = get_book_links(category_url)
    
    
    for book_link in book_links:
        print(f"Processing book: {book_link}")
        image_url = extract_image_url(book_link)
        if image_url:  
            image_urls.append([image_url])
        time.sleep(1)  


image_csv_file = 'all_image_urls.csv'
with open(image_csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['image_url'])
    writer.writerows(image_urls)

print("Image URL extraction is complete, and all image URLs have been written to all_image_urls.csv.")
