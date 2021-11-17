from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime, timezone, timedelta
import pytz

tz=pytz.timezone("Europe/Riga")
time_now = datetime.now(tz)
format = "%Y-%m-%d-%T"
time_now = time_now.strftime(format)
time_now = time_now

def refresh_time_24():
    tz=pytz.timezone("Europe/Riga")
    time_now = datetime.now(tz)
    format = "%Y-%m-%d-%T"
    time_now = time_now.strftime(format)
    return time_now


def parse_city24_scraper():
    def parse_page_city24(page=0):
        for row in rows:
            d = {}
            try:
                d["address"] = row.find("a", {"class": "addressLink"}).find("span").text.split(",")[0]
            except:
                d["address"] = None

            try:
                d["istabas"] = int(row.find("div", {"class": "column"}).find("ol").find_all("li")[1].find("strong").text)
            except:
                d["istabas"] = None

            try:
                d["platiba"] = float(row.find("div", {"class": "column"}).find("ol").find_all("li")[0].find("strong").text.split(" ")[0])
            except:
                d["platiba"] = None

            try:
                d["stavs"] = row.find("div", {"class": "column"}).find("ol").find_all("li")[2].find("strong").text
            except:
                d["stavs"] = None


            try:
                d["price_m2"] = float(row.find("div", {"class": "price_sqrm"}).text.replace(" ", "").replace("EUR/m²", "").replace(",", "."))
            except:
                d["price_m2"] = None

            try:
                d["price"] = int(row.find("div", {"class": "price"}).find("div").text.replace(" EUR", "").replace(" ", "").strip())
            except:
                d["price"] = None

            try:
                d["links"] = row.find("a", href=True)["href"]
            except:
                d["links"] = None

            try:
                d["vieta"] = row.find("a", {"class": "addressLink"}).find("span").text.split(",")[1]
            except:
                d["vieta"] = None
            

            # try:
            #     d["promo"] = row.find_all("div", {"class": "column"})[1].find("div", {"class": "promo"}).find("span").text
            # except:
            #     d["promo"] = None
            d_list.append(d)
        refresh_time_24()

    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    d_list = []

# TODO set range to (0, 9)
    for page in range(0, 1):
        url = f"https://www.city24.lv/real-estate-search/apartments-for-sale/R%C4%ABga-%C4%80genskalns/id=25875-city/pg={page}"
        print(f"Processing page nr: {page} ...")
        print(url)

        response = requests.get(url, headers=headers)
        content = response.text

        soup = BeautifulSoup(content, "html.parser")
        print(content)
        # write content to file
        with open(f"city24_scraper_{page}.html", "w") as f:
            f.write(content)
            
        # table = soup.find("div", {"id": "list-container"})
        # rows = table.find_all("li", {"class": "new result regular"})

        time.sleep(0.5)

# TODO uncoment next line
        # parse_page_city24(page)


    # create file
    df = pd.DataFrame(d_list)
    # print(df)
    # real filtered file
    # import pandas as pd
    # Create a Pandas Excel writer using XlsxWriter as the engine.

    writer = pd.ExcelWriter(f"output/{refresh_time_24()}_city24.xlsx", engine='xlsxwriter')


    # Convert the dataframe to an XlsxWriter Excel object. We also turn off the
    # index column at the left of the output dataframe.
    df.to_excel(writer, sheet_name='Sludinajumi')
# .dropna()
    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sludinajumi']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Make the columns wider for clarity.
    worksheet.set_column(0,  max_col - 1, 12)

    # Set the autofilter.
    worksheet.autofilter(0, 0, max_row, max_col)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

# print("Done!")
