from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime


time_now = datetime.now()
format = "%Y-%m-%d-%T"

time_now = time.strftime(format)
print(time_now)

ss_filename = f"output/ss{time_now}"
def scrape_ss():
    def parse_page(page=1):
        for row in rows:
            d = {}
            elements = row.find_all("td", {"class": "msga2-o pp6"})
            element_list = []
            for i in elements:
                element_list.append(i.text)
            try:
                d["address"] = element_list[0]
                d["istabas"] = element_list[1]
                d["platiba"] = element_list[2]
                d["stavs"] = element_list[3]
                d["tips"] = element_list[4]
                d["cena_m2"] = element_list[5].replace(" €", "")
                d["cena(eiro)"] = element_list[-1].replace("  €", "")
            except:
                d["address"] = None
                d["istabas"] = None
                d["platiba"] = None
                d["stavs"] = None
                d["tips"] = None
                d["cena_m2"] = None
                d["cena(eiro)"] = None
            d_list.append(d)



    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    d_list = []

    for page in range(1, 2):
        url = f"https://www.ss.com/lv/real-estate/flats/riga/agenskalns/sell/page{page}.html"
        response = requests.get(url, headers=headers)
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        table = soup.select("table:nth-child(3)")
        rows = table[0].find_all("tr")
        # time.sleep(2)
        print(page)
        parse_page(page)




    df = pd.DataFrame(d_list)

    df.dropna().to_csv(f"{ss_filename}.csv")
    df.dropna().to_excel(f"{ss_filename}.xlsx")
    print("Done!")
