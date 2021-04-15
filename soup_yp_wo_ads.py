import pprint
import json
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime

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
    current_time = now.strftime("%H:%M_%m-%y")
    global file_name
    if "/" in file_name:
        file_name = args[1].replace('/', '_')
    if " " in file_name:
        file_name = file_name.replace(' ', '_')
    # print('DONE')

    with open(f'output/{file_name}-{current_time}.json', 'w') as json_file:
        global json_name
        json_name = f'{file_name}-{current_time}.json'
        # json_name = f'pp.json'
        
        print(json_name)
        json.dump(top_30, json_file)