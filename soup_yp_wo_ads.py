import pprint
import json
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import csv
import pandas as pd
import numpy as np
  

file_name = ''
json_name = ''
business_title_list = []
def output_file(*args):
    def get_result():
        search_url = args[0]
        global file_name
        file_name = args[1]
        res = requests.get(search_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        organic_pane = soup.find_all(lambda tag: tag.name == 'div' and
                               tag.get('class') == ['result'])

        for business in organic_pane:
            global title
            title = ""
            global address_location
            address_location = ""
            global street_address
            street_address = ""
            global phone_num
            phone_num = ""

            for business_title in business.select('.business-name'):
                title = business_title.text
            for address in business.select('.locality'):
                address_location = address.text
            for str_address in business.select('.street-address'):
                street_address = str_address.text
            for phone in business.select('.phones.phone.primary'):
                phone_num = phone.text

            yield {
                "title": title,
                "address": address_location,
                "street_address": street_address,
                "number": phone_num,
                }


    get_result()
    top_30 = list(get_result())
    now = datetime.now()
    current_time = now.strftime("%y-%m-%d-%H-%M")
# %H:%M_%m-%y
    global file_name
    if "/" in file_name:
        file_name = args[1].replace('/', '_')
    if " " in file_name:
        file_name = file_name.replace(' ', '_')
    # print('DONE')

# writting json
    with open(f'output/{current_time}_{file_name}.json', 'w') as json_file:
        global json_name
        json_name = f'{current_time}_{file_name}.json'
        json.dump(top_30, json_file)

# writting csv
    with open(f"output/{current_time}_{file_name}.csv","w",newline="") as f:  # python 2: open("output.csv","wb")
        title = "title,address,street_address,number".split(",") # quick hack
        cw = csv.DictWriter(f,title,delimiter=',', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(top_30)

# writting excel
# Reading the csv file
    df_new = pd.read_csv(f'output/{current_time}_{file_name}.csv')
    
    # saving xlsx file
    GFG = pd.ExcelWriter(f'output/{current_time}_{file_name}.xlsx')
    df_new.to_excel(GFG, index = False)
    
    GFG.save()