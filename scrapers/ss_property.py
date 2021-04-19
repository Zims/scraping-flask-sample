from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime


time_now = datetime.now()
format = "%Y-%m-%d-%T"
time_now = time.strftime(format)
ss_filename = f"output/ss{time_now}"

def refresh_time():
    time_now = datetime.now()
    format = "%Y-%m-%d-%T"
    time_now = time.strftime(format)
    global ss_filename
    ss_filename = f"output/ss{time_now}"
    return ss_filename

def scrape_ss(chosen_region):
    def parse_page(page=1):
        for row in rows:
            d = {}
            elements = row.find_all("td", {"class": "msga2-o pp6"})
            element_list = []
            for i in elements:
                element_list.append(i.text)
            try:
                d["address"] = element_list[0]
                try:
                    d["istabas"] = int(element_list[1])
                except:
                    d["istabas"] = "Nav norādīts"

                d["platiba"] = int(element_list[2])
                d["stavs"] = element_list[3]
                d["tips"] = element_list[4]
                d["cena_m2"] = int(element_list[5].replace(" €", "").replace(",", ""))
                d["cena(eiro)"] = int(element_list[-1].replace("  €", "").replace(",", ""))
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

    for page in range(1, 5):
        url = f"https://www.ss.com/lv/real-estate/flats/riga/{chosen_region[0]}/sell/page{page}.html"
        print(url)
        response = requests.get(url, headers=headers)
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        table = soup.select("table:nth-child(3)")
        rows = table[0].find_all("tr")
        # time.sleep(2)
        print(page)
        parse_page(page)

    print(refresh_time())


    df = pd.DataFrame(d_list)

    # df.dropna().to_csv(f"{ss_filename}.csv")
    df.dropna().to_excel(f"{ss_filename}.xlsx")
    print("Done!")
