import requests
import pandas as pd
import pytz
from datetime import datetime
import time

tz = pytz.timezone("Europe/Riga")
time_now = datetime.now(tz)
format = "%Y-%m-%d-%T"
time_now = time_now.strftime(format)
time_now = time_now


def refresh_time_inch():
    tz = pytz.timezone("Europe/Riga")
    time_now = datetime.now(tz)
    format = "%Y-%m-%d-%T"
    time_now = time_now.strftime(format)
    return time_now


headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

url_centrs = "https://api.inch.lv/api/search/apartments?city=R%C4%ABga&district=Centrs,P%C4%81rdaugava," \
             "%C4%80genskalns,Beberbe%C4%B7i+(mukupurvs),Bieri%C5%86i-Atg%C4%81zene,Bi%C5%A1umui%C5%BEa,Ber%C4%A3i," \
             "Bolder%C4%81ja,Bukulti,Bu%C4%BC%C4%BCi,%C4%8Ciekurkalns,D%C4%81rzciems,Daugavgr%C4%ABva,Dreili%C5%86i," \
             "Dzirciems,I%C4%BC%C4%A3uciems,Imanta,Jaunciems,Jugla,Katlakalns,%C4%B6engarags,%C4%B6%C4%ABpsala," \
             "Kleisti,Kl%C4%ABversala,Krasta+rajons,Manga%C4%BCi+(m%C4%ABlgr%C4%81vis),Manga%C4%BCsala," \
             "Maskavas+priek%C5%A1pils.,Me%C5%BEaparks,Me%C5%BEciems,P%C4%BCavnieki,Purvciems,Rumbula," \
             "%C5%A0amp%C4%93teris-Pleskod%C4%81le,Sarkandaugava,%C5%A0%C4%B7irotava,Spilve,Su%C5%BEi,Teika+(VEF)," \
             "Tor%C5%86akalns,Tr%C4%ABsciems,Vec%C4%81%C4%B7i,Vecdaugava,Vecmilgr%C4%81vis,Vecr%C4%ABga,Voleri," \
             "Za%C4%B7usala-Lucavsala,Zasulauks,Ziepniekkalns," \
             "Zolit%C5%ABde&dealType=sale&page=1&optimize=1&fields=id,images,city,district,address,longitude," \
             "latitude,userUpdatedAt,price,dealType,rentPriceUnit,area,roomCount,floorNumber," \
             "floorTotal&offset=0&limit=1210 "

resp = requests.get(url_centrs, headers=headers)
resp_json = resp.json()
resp_headers = resp_json['apartments']['header']
resp_data = resp_json['apartments']['data']


# import json
#
# # Parse JSON
# with open('data.json', 'w') as outfile:
#     json.dump(resp_json, outfile)
def parse_inch_scraper():
    d_list = []
    for i in resp_data:
        d = {}
        try:
            d["adrese"] = i[3].split(',')[0]
        except:
            d["adrese"] = "Nav"
        try:
            d["istabas"] = i[10]
        except:
            d["istabas"] = "Nav"
        try:
            d["platība"] = i[9]
        except:
            d["platība"] = "Nav"
        try:
            d["stāvs"] = f"{i[11]}/{i[12]}"
        except:
            d["stāvs"] = "Nav"

        d["tips"] = "Nav"

        try:
            d["cena_m2"] = round(i[-3] / i[9], 2)
        except:
            d["cena_m2"] = "Nav"
        try:
            d["cena"] = i[-3]
        except:
            d["cena"] = "Nav"

        try:
            d["links"] = f"https://inch.lv/details/apartment/{i[0]}"
        except:
            d["links"] = "Nav"

        try:
            d["vieta"] = i[3].split(',')[1]
        except:
            d["vieta"] = "Nav"

        d_list.append(d)
        # print(len(d_list))
        # create file
        df = pd.DataFrame(d_list)
        # print(df)
        # real filtered file
        # import pandas as pd
        # Create a Pandas Excel writer using XlsxWriter as the engine.

    writer = pd.ExcelWriter(f"output/{refresh_time_inch()}_inch.xlsx", engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object. We also turn off the
    # index column at the left of the output dataframe.
    df.dropna().to_excel(writer, sheet_name='Sludinajumi')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sludinajumi']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Set the autofilter.
    worksheet.autofilter(0, 0, max_row, max_col)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print("Done!")


# parse_inch_scraper()
