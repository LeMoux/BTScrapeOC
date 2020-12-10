import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'

response = requests.get(url)

if response.ok:
	soup = BeautifulSoup(response.text, 'lxml')
	title = soup.find('title')

	print("product_page_url: " + url)

	for i in soup.find_all("th"):
		if i.text.strip() == "UPC":
			print("universal_product_code (upc): " + i.find_next("td").text.strip())

	print("title: " + title.text.replace(' | Books to Scrape - Sandbox', ''))

	for i in soup.find_all("th"):
		if i.text.strip() == "Price (incl. tax)":
			print("price_including_tax: " + i.find_next("td").text.strip())
            
	for i in soup.find_all("th"):
		if i.text.strip() == "Price (excl. tax)":
			print("price_excluding_tax: " + i.find_next("td").text.strip())
            
	for i in soup.find_all("th"):
		if i.text.strip() == "Availability":
			print("number_available: " + i.find_next("td").text.strip())
            
	for i in soup.find_all("h2"):
		if i.text.strip() == "Product Description":
			print("product_description: " + i.find_next("p").text.strip())
            
	for i in soup.find_all("li"):
		if i.text.strip() == "Books":
			print("category: " + i.find_next("li").text.strip())
            
	for i in soup.find_all("th"):
		if i.text.strip() == "Number of reviews":
			print("review_rating: " + i.find_next("td").text.strip())
            
	for i in soup.find_all("th"):
		if i.text.strip() == "Number of reviews":
			print("review_rating: " + i.find_next("td").text.strip())
            
	image = soup.find('img')
	print("image_url: " + image["src"].replace('../../', "http://books.toscrape.com/"))
