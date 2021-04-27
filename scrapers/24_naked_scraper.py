from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


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
# print(table)
# rows = table[0].find_all("tr")

# for row in rows:
#     d = {}
#     elements = row.find_all("td", {"class": "msga2-o pp6"})
#     element_list = []
#     for i in elements:
#         element_list.append(i.text)
#     try:
#         d["address"] = element_list[0]
#         try:
#             d["istabas"] = int(element_list[1])
#         except:
#             d["istabas"] = "Nav norādīts"

#         d["platiba"] = int(element_list[2])
#         d["stavs"] = element_list[3]
#         d["tips"] = element_list[4]
#         d["cena_m2"] = int(element_list[5].replace(" €", "").replace(",", ""))
#         d["cena(eiro)"] = int(element_list[-1].replace("  €", "").replace(",", ""))
#         d["Vieta"] = chosen_region[0]
#     except:
#         d["address"] = None
#         d["istabas"] = None
#         d["platiba"] = None
#         d["stavs"] = None
#         d["tips"] = None
#         d["cena_m2"] = None
#         d["cena(eiro)"] = None
#     d_list.append(d)