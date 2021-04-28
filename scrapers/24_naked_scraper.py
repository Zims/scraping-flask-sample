from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

def parse_page_city24(list_item):
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
            
            # Ir ok jo 24 neljauj izveeleeties vietu
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


d_list = []
# pagination
def pagination_city24():
    for page in range(0, 15):
        url = f"https://www.city24.lv/lv/saraksts?fr={page}"
        print(f"Processing page nr: {page} ...")

        response = requests.get(url, headers=headers)
        content = response.text
        # soup = BeautifulSoup(content, "html.parser")
        # table = soup.find("a", {"class": "next"})
        # rows = table[0].find_all("tr")
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("div", {"id": "list-container"})
        list_item = table.find_all("li", {"class": "new result regular"})
        time.sleep(3)
        parse_page_city24(list_item)


# url = f"https://www.city24.lv/lv/saraksts?fr=0"
# response = requests.get(url, headers=headers)
# content = response.text
# soup = BeautifulSoup(content, "html.parser")
# table = soup.find("div", {"id": "list-container"})
# list_item = table.find_all("li", {"class": "new result regular"})

pagination_city24()

# create file
df = pd.DataFrame(d_list)
# quick test write
# df.dropna().to_excel(f"test_01.xlsx")

# real filtered file
# import pandas as pd
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("{ss_filename}_ss_{chosen_region[0]}.xlsx", engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object. We also turn off the
# index column at the left of the output dataframe.
df.dropna().to_excel(writer, sheet_name='Sludinajumi')

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
print("Done!")
