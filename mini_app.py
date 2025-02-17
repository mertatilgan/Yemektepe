import re
import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from printy import printy, inputy
from datetime import datetime

async def scrape_menu():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://sksdb.hacettepe.edu.tr/YemekListesi.xml') as response:
            xml_data = await response.text()
            meals_data = parse_menu(xml_data)
            return meals_data

def clean_meal_name(meal_name):
    return re.sub(r'\([^)]*\)', '', meal_name).strip()

def parse_menu(xml_string):
    root = ET.fromstring(xml_string)
    meals_by_date = {}

    for gun in root.findall('.//gun'):
        tarih = gun.find('tarih').text[0:10].strip()
        yemekler = gun.find('yemekler')
        meals = [clean_meal_name(yemek.text.strip()) for yemek in yemekler.findall('yemek')]
        calories = gun.find('kalori').text.strip()
        meals_by_date[tarih] = {"meals": meals, "calories": calories}

    return meals_by_date

async def main():
    try:
        from printy import printy
    except ImportError:
        printy = None

    meals_data = await scrape_menu()
    today_str = datetime.now().strftime("%#d.%m.%Y")

    if today_str in meals_data:
        details = meals_data[today_str]
        if printy:
            printy(f"\n[r>]Bugünün Menüsü@ [g]({today_str}):@")
            for meal in details["meals"]:
                printy(f"  [r>]-@ [w]{meal}@")
            printy(f"[g]Toplam Kalori:@ [r>]{details['calories']}@")
        else:
            print(f"Bugünün Menüsü ({today_str}):")
            for meal in details["meals"]:
                print(f"  - {meal}")
            print(f"Toplam Kalori: {details['calories']}")
    else:
        message = "Bugünün menüsüne ulaşılamadı."
        if printy:
            printy(f"[r]{message}@")
        else:
            print(message)

if __name__ == "__main__":
    asyncio.run(main())
