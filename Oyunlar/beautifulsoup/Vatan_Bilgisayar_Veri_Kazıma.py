import requests
from bs4 import BeautifulSoup

url = "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/"

parser = BeautifulSoup(requests.get(url).content,"html.parser")

veri=parser.find("div",{"class":"wrapper-product wrapper-product--list-page clearfix"})\
    .find_all("div",{"class":"product-list product-list--list-page"})

for i in veri:
    ad = i.find("div", {"class": "product-list__content"}).find("a", {"class": "product-list-link"})\
        .find("div",{"class":"product-list__product-name"})
    print(ad)
