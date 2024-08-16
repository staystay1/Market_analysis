import requests
from bs4 import BeautifulSoup
import csv


url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


product_page_url = url
upc = soup.find('th', string='UPC').find_next('td').text
book_title = soup.h1.text
price_including_tax = soup.find('th', string='Price (incl. tax)').find_next('td').text
price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text
quantity_available = soup.find('th', string='Availability').find_next('td').text.strip()
product_description = soup.find('div', id='product_description').find_next('p').text
category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
review_rating = soup.find('p', class_='star-rating')['class'][1]
image_url = "http://books.toscrape.com/" + soup.find('img')['src'].replace('../', '')


print("UPC:", upc)
print("Title:", book_title)
print("Price (incl. tax):", price_including_tax)
print("Price (excl. tax):", price_excluding_tax)
print("Quantity available:", quantity_available)
print("Description:", product_description)
print("Category:", category)
print("Review rating:", review_rating)
print("Image URL:", image_url)


csv_file = 'book_data.csv'


with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(['product_page_url', 'universal_product_code (upc)', 'book_title', 'price_including_tax',
                     'price_excluding_tax', 'quantity_available', 'product_description', 'category',
                     'review_rating', 'image_url'])
    
    writer.writerow([product_page_url, upc, book_title, price_including_tax, price_excluding_tax,
                     quantity_available, product_description, category, review_rating, image_url])

print(f"Data has been written to {csv_file}")
