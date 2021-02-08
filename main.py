import requests
from bs4 import BeautifulSoup
import re
import csv
import os

# Function to get all the book's categories and to create the csv folder

def get_categories():
    try:
        os.mkdir('./csv_files')
    except:
        pass
    main_url = 'http://books.toscrape.com/index.html'
    response_main_url = requests.get(main_url)
    if response_main_url.ok:
        soup = BeautifulSoup(response_main_url.text, 'lxml')
        books_category = soup.find("ul", {"class": "nav nav-list"}).find_all("li")[1:]
        for category in books_category:
            print("Next category")
            category_url = 'http://books.toscrape.com/' + category.a['href']
            get_products_urls(category_url)

# Function to get all the book's urls

def get_products_urls(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup('article')
        for book in books:
            book_href = book.find('a')
            links = book_href['href']
            link_product = "https://books.toscrape.com/catalogue/" + links.replace("../../../", "")
            get_product_infos(link_product)
        try:
            next_page_selector = soup.find('section').find('li', {'class': 'next'}).select('a')
            next_page_href = next_page_selector[0]['href']
            url_split = url.rsplit("/", 1)
            next_page_url = url_split[0] + str("/" + next_page_href)
            print("Next page : " + next_page_url)
            get_products_urls(next_page_url)
        except:
            pass

# Function to get all the product's informations

def get_product_infos(url):
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            book_url = str(url)
            book_selector = soup.find("table", {"class": "table table-striped"}).find_all("td")
            book_upc = book_selector[0]
            book_title = str(soup.find('div', {'class': 'col-sm-6 product_main'}).select('h1')[0].text)
            book_price_including_tax = book_selector[3].text[1:]
            book_price_excluding_tax = book_selector[2].text[1:]
            book_number_available = book_selector[5]
            book_description = soup.find("article", {"class": "product_page"}).find_all("p")[3]
            book_category = str(soup.find('ul', {'class': 'breadcrumb'}).select('li')[2].text).replace("\n", '')
            book_review = soup.find('p', class_='star-rating').get('class')[1]           
            book_picture_selector = soup.find('div', {'class': 'item active'}).select('img')[0]['src']
            book_picture_split = book_picture_selector.split('../')[2]
            book_picture_src_link = str('http://books.toscrape.com/' + book_picture_split)
            get_product_picture(book_picture_src_link, book_title, book_category)
            book_datas = {'product_page_url': book_url, 'upc': book_upc.text, 'title': book_title, 'price_including_tax': book_price_including_tax, 'price_excluding_tax': book_price_excluding_tax, 'number_available': book_number_available.text, 'product_description': book_description.text, 'category': book_category, 'review_rating': book_review, 'image_url': book_picture_src_link}
            create_csv_file(book_category, book_datas)
            return book_datas

# Function to get all the books cover and sorting them by their categories

def get_product_picture(file_url, file_name, file_category):
    image = requests.get(file_url)
    picture_name = re.sub('[^A-Za-z0-9]+', '', file_name)
    try:
        os.mkdir('./product_pictures')
    except:
       pass
    if os.path.isdir('./product_pictures/' + file_category):
        file_path = 'product_pictures/'+ file_category + '/' + picture_name + '.' + file_url.split('.')[-1]
        with open(file_path, 'wb') as file:
            file.write(image.content)
    else:
        os.makedirs('./product_pictures/' + file_category)
        file_path = 'product_pictures/' + file_category + '/' + picture_name + '.' + file_url.split('.')[-1]
        with open(file_path, 'wb') as file:
            file.write(image.content)

# Function to create the CSV files

def create_csv_file(category, data):
    try:
        with open('csv_files/' + category + '.csv', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            if reader:
                with open('csv_files/' + category + '.csv', 'a', encoding='UTF8', newline='') as csv_file:
                    header = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
                    writer = csv.DictWriter(csv_file, fieldnames=header)
                    writer.writerow(data)
    except FileNotFoundError:
        with open('csv_files/' + category + '.csv', 'w', encoding='UTF8', newline='') as csv_file:
            header = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            writer.writerow(data)
    finally:
        print("Transfer to CSV file: " + category)



# Launch the Scrapper

get_categories()