import requests
from bs4 import BeautifulSoup
import pandas as pd


district = 'https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={}&region=2'

links = []

i = 1
response = requests.get(district.format(i))
html_soup = BeautifulSoup(response.text, 'html.parser')
total_flats_number = str(html_soup.find('h5', class_="_93444fe79c--color_black_100--A_xYw "
                                                 "_93444fe79c--lineHeight_20px--2dV2a "
                                                 "_93444fe79c--fontWeight_bold--t3Ars "
                                                 "_93444fe79c--fontSize_14px--10R7l "
                                                 "_93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER"))

start = total_flats_number.find('Найдено') + len('Найдено') + 1
end = total_flats_number.find('объявлени') - 1

total_flats_number = int(total_flats_number[start:end].replace(" ", ""))

current_number_flats = 0

flat_titles = []
flat_cost = []
out = []
geo_labels = []
while current_number_flats < total_flats_number:
    search_page = requests.get(district.format(i))
    soup = BeautifulSoup(search_page.text, 'lxml')
    flats = soup.find_all('div', class_='_93444fe79c--content--2IC7j')
    for flat in flats:
        if 'этаж' in flat.find('div', class_='_93444fe79c--container--JdWD4').find('span').text.split():
            flat_titles.append(flat.find('div', class_='_93444fe79c--container--JdWD4').find('span').text)
        else:
            flat_titles.append(flat.find('div', class_='_93444fe79c--subtitle--iGb0_').text)

        flat_cost.append(flat.find('span', class_='_93444fe79c--color_black_100--A_xYw '
                                                  '_93444fe79c--lineHeight_28px--3QLml '
                                                  '_93444fe79c--fontWeight_bold--t3Ars '
                                                  '_93444fe79c--fontSize_22px--3UVPd '
                                                  '_93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER').text)

        geo_labels.append(flat.find('div', class_='_93444fe79c--labels--1J6M3').text)

    current_number_flats = len(flat_titles)
    i += 1


data = {'title': flat_titles, 'cost': flat_cost, 'geo_data': geo_labels}
data = pd.DataFrame(data)
data.to_csv('data.csv', index=False)