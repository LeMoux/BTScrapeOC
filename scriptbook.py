main_url = "http://books.toscrape.com/index.html"

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def getanalyseURL(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    return(soup)

def getlivreURL(url):
    soup = getanalyseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])

pages_urls = [main_url]
soup = getanalyseURL(pages_urls[0])
while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")
    pages_urls.append(new_url)
    soup = getanalyseURL(new_url)

livreURL = []
for page in pages_urls:
    livreURL.extend(getlivreURL(page))

titres = []
categories = []
notes = []

for url in livreURL:
    soup = getanalyseURL(url)
    titres.append(soup.find("div", class_ = re.compile("product_main")).h1.text)
    categories.append(soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3])
    notes.append(soup.find("p", class_ = re.compile("star-rating")).get("class")[1])


scraped_data = pd.DataFrame({'Titre': titres, "Categorie": categories, "Note": notes})
print(scraped_data)
scraped_data.to_csv(r'data.csv')

