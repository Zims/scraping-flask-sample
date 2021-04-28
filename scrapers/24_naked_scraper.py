from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

d_list = []
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}


url = f"https://www.city24.lv/lv/saraksts?usp=true&fr=0"
# print(url)
response = requests.get(url, headers=headers)
content = response.text
# print(content)
soup = BeautifulSoup(content, "html.parser")

# table = soup.select("div:")
table = soup.find("div", {"id": "list-container"})
list_item = table.find_all("li", {"class": "new result regular"})
print(len(list_item))

def parse_page_city24():
    for i in list_item:
        d = {}
        try:
            d["address"] = i.find("a", {"class": "addressLink"}).find("span").text.split(",")[0]
            d["istabas"] = int(i.find("div", {"class": "column"}).find("ol").find_all("li")[1].find("strong").text)
            d["platiba"] = float(i.find("div", {"class": "column"}).find("ol").find_all("li")[0].find("strong").text.split(" ")[0])
            d["stavs"] = i.find("div", {"class": "column"}).find("ol").find_all("li")[2].find("strong").text
            d["promo"] = i.find_all("div", {"class": "column"})[1].find("div", {"class": "promo"}).find("span").text
            
            d["price_m2"] = float(i.find("div", {"class": "price_sqrm"}).text.replace(" ", "").replace("EUR/m²", "").replace(",", "."))
            d["price"] = int(i.find("div", {"class": "price"}).find("div").text.replace(" EUR", "").replace(" ", "").strip())
            
            # No good TODO. Use scraper input
            d["vieta"] = i.find("a", {"class": "addressLink"}).find("span").text.split(",")[1]
        except:
            d["address"] = None
            d["istabas"] = None
            d["platiba"] = None
            d["stavs"] = None
            d["promo"] = None
            d["price_m2"] = None
            d["price"] = None
            d["vieta"] = None
        d_list.append(d)
    print(d_list[5])
