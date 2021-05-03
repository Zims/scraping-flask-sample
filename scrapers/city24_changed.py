from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime, timezone, timedelta
import pytz

# city 24 ir paargaajis uz js
# vajag selenium

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
url = "https://m.city24.lv/real-estate-search/apartments-for-sale/R%C4%ABga-%C4%80genskalns/date=all_time/id=25875-city/tc=1,1"


resp = requests.get(url, headers=headers)
content = resp.content
# print(content)

soup = BeautifulSoup(content, "html.parser")
table = soup.find("div", attrs={"class": "results__objects"})
print(soup)
# rows = table.find_all("li", {"class": "new result regular"})
