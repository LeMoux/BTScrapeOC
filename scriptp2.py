import requests
from bs4 import BeautifulSoup
import csv
import re



def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return (soup)

class Category:

    def __init__(self, name):
        self.name = name
        self.books = []

    def addBook(self, book):
        self.books.append(book)

class Book:

    def __init__(self, url, productCode, title, priceTTC, priceHT, availableCount, description, reviewRating, imageUrl):
        self.url = url
        self.productCode = productCode
        self.title = title
        self.priceTTC = priceTTC
        self.priceHT = priceHT
        self.availableCount = availableCount
        self.description = description
        self.reviewRating = reviewRating
        self.imageUrl = imageUrl

class Scrapper:

    def __init__(self):
        self.categories = []

    def get_categories(self):
        soup = getSoup("http://books.toscrape.com/")
        books_category = soup.find("ul", {"class": "nav nav-list"}).find_all("li")[1:]
        for li in books_category:
            category = Category(li.find("a")["href"].split('/')[3])
            self.categories.append(category)

    def get_products_urls(self):
        for category in self.categories:
            soup = getSoup("https://books.toscrape.com/catalogue/category/books/" + category.name + "/index.html")
            pager = (soup.find("li", {"class": "current"}))
            if pager is None:
                books = soup.findAll("h3")
                for h3 in books:
                    a = h3.find("a")
                    links = a["href"]
                    link_product = "https://books.toscrape.com/catalogue/" + links.replace("../../../", "")
                    category.addBook(self.get_product_infos(link_product))
            else:
                pager = str(pager)
                pager = pager.split()[5]
                nbPages = int(pager)
                for i in range(nbPages + 1):
                    url = "https://books.toscrape.com/catalogue/category/books/" + category.name + "/page-" + str(i) + ".html"
                    response = requests.get(url)
                    if response.ok:
                        soup = BeautifulSoup(response.text, 'lxml')
                        books = soup.findAll("h3")
                        for h3 in books:
                            a = h3.find("a")
                            links = a["href"]
                            links_product = "https://books.toscrape.com/catalogue/" + links.replace("../../../", "")
                            category.addBook(self.get_product_infos(links_product))

    def get_product_infos(self, link_product):
            book_url = link_product.strip()
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.text, 'lxml')
            book_colonne = book_soup.find("table", {"class": "table table-striped"}).find_all("td")
            book_universal_product_code = book_colonne[0]
            book_title = book_soup.find("h1")
            book_price_including_tax = book_colonne[3]
            book_price_excluding_tax = book_colonne[2]
            book_number_available = book_colonne[5]
            book_product_description = book_soup.find("article", {"class": "product_page"}).find_all("p")[3]
            book_review_rating = book_soup.find('p', class_='star-rating').get('class')[1]
            book_images = book_soup.find("div", class_='item active').find_all("img")
            book_image_url = ""
            for book_image_url in book_images:
                book_image_url = "http://books.toscrape.com/" + (book_image_url.get('src')[5:])            
            return Book(book_url, book_universal_product_code.text, book_title.text, book_price_including_tax.text[2:],
                        book_price_excluding_tax.text[2:],
                        book_number_available.text, book_product_description.text, book_review_rating, book_image_url)

    def createCsv(self):
        for category in self.categories:
            with open(category.name + ".csv", "a", encoding='utf-8') as file:
                writer = csv.writer(file)
                file.write(
                    "product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,review_rating,images\n")
                for book in category.books:
                    writer.writerow([book.url, book.productCode, book.title, book.priceTTC, book.priceHT, book.availableCount, book.description, book.reviewRating, book.imageUrl])
                    


MyScrapper = Scrapper()
MyScrapper.get_categories()
MyScrapper.get_products_urls()
MyScrapper.createCsv()