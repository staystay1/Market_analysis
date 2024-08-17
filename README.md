# Web Scraping Project

This project scrapes data from the "Books to Scrape" website. The following code extracts book information, handle pagination, categorize data, and download images.

## Prerequisites

Ensure you have Python 3.8 or higher installed on your device.

## Features 

- Extracting one book data into a csv file.
- Extracting a category of books data into a csv file.
- Extracting all categoires of books data and separating each category into its own csv file.
- Extracting all image URL's and allowing you to download them if desired.

## Setup Instructions

How to get set up 

### 1. Clone the Repository

Run the followng:

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Installing libaries  

Run the following:

```bash
pip install bs4
```
```bash
pip install requests  
```
```bash
pip install beautifulsoup4 
```

### 3. Running the Enviroment 

Running the following code will extract and store the data from the given URL of any book you desire.

```bash
python scrape_book.py
```

Running the following code will extract and store the data of all books from the given URL's of any category you desire.

```bash
python scrape_category.py
```

Running the following code will extract and store the data of all books into their respective category.

```bash
python scrape_all_categories.py
```

Running the following code will extract and store the data of all image URL's.

```bash
python scrape_all_images.py
```

### 4. Stopping the Enviroment

To stop the process of the eniroment before it stops on it's own. Press the follwoing keys:
'ctrl' 'c'
