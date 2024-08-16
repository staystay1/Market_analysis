import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

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

def extract_book_data(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        product_page_url = book_url
        upc = soup.find('th', string='UPC').find_next('td').text if soup.find('th', string='UPC') else 'N/A'
        book_title = soup.h1.text if soup.h1 else 'N/A'
        price_including_tax = soup.find('th', string='Price (incl. tax)').find_next('td').text if soup.find('th', string='Price (incl. tax)') else 'N/A'
        price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text if soup.find('th', string='Price (excl. tax)') else 'N/A'
        quantity_available = soup.find('th', string='Availability').find_next('td').text.strip() if soup.find('th', string='Availability') else 'N/A'
        product_description = soup.find('div', id='product_description').find_next('p').text if soup.find('div', id='product_description') else 'N/A'
        category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip() if soup.find('ul', class_='breadcrumb') and len(soup.find('ul', class_='breadcrumb').find_all('li')) > 2 else 'N/A'
        review_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else 'N/A'
        image_url = urljoin(book_url, soup.find('img')['src']) if soup.find('img') else 'N/A'
    
        print(f"Successfully extracted data from: {book_title}")
    
    except Exception as e:
        print(f"Error extracting data from {book_url}: {e}")
        return None
    
    return [product_page_url, upc, book_title, price_including_tax, price_excluding_tax,
            quantity_available, product_description, category, review_rating, image_url]


category_url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
book_links = get_book_links(category_url)

csv_file = 'travel_books_data.csv'


with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['product_page_url', 'universal_product_code (upc)', 'book_title', 'price_including_tax',
                     'price_excluding_tax', 'quantity_available', 'product_description', 'category',
                     'review_rating', 'image_url'])
    
  
    for book_link in book_links:
        print(f"Processing book: {book_link}")
        book_data = extract_book_data(book_link)
        if book_data:  
            writer.writerow(book_data)
        time.sleep(1)  

print(f"Data for all books in the category has been written to {csv_file}")
