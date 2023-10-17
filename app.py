import re
import aiohttp
import asyncio
import locale
import calendar
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from flask import Flask, render_template

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)

async def scrape_menu():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://sksdb.hacettepe.edu.tr/YemekListesi.xml') as response:
            print("Status:", response.status)
            xml_data = await response.text()
            new_meals_data = parse_menu(xml_data)
            return new_meals_data

def clean_meal_name(meal_name):
    cleaned_name = re.sub(r'\([^)]*\)', '', meal_name)
    return cleaned_name.strip()

def parse_menu(xml_string):
    root = ET.fromstring(xml_string)

    meals_by_date = {}
    for gun in root.findall('.//gun'):
        tarih = gun.find('tarih').text[0:10].strip()
        yemekler = gun.find('yemekler')
        meals = [clean_meal_name(yemek.text.strip()) for yemek in yemekler.findall('yemek')]
        meals_by_date[tarih] = meals

    return meals_by_date

async def get_meals_data():
    new_meals_data = await scrape_menu()
    return new_meals_data

@app.route('/')
def index():
    meals_data = asyncio.run(get_meals_data())
    today = datetime.now()
    meals_list = []

    for day_offset in range(7):
        date_to_check = today + timedelta(days=day_offset)
        formatted_date = date_to_check.strftime("%#d.%m.%Y")
        day_name = calendar.day_name[date_to_check.weekday()]

        if formatted_date in meals_data:
            meals_dict = {}
            if day_offset == 0:
                meals_dict["date"] = f"Bugünün Menüsü ({formatted_date})"
            else:
                meals_dict["date"] = f"{day_name} Gününün Menüsü ({formatted_date})"

            meals_dict["meals"] = meals_data[formatted_date]
            meals_list.append(meals_dict)
        else:
            meals_list.append({"date": f"{day_name}, {formatted_date}", "meals": ["Yemek bulunamadı."]})

    return render_template('meals.html', meals=meals_list)

if __name__ == "__main__":
    app.run()