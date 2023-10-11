# Yemektepe
This is a simple Flask web application that scrapes a menu from the Hacettepe University's Office of Health, Culture and Sports (SKSDB) website and displays it for the current week.

## Requirements
Before you can run this application, make sure you have the following requirements installed:
- aiohttp
- Flask

You can install these dependencies using pip:
```bash
pip install -r requirements.txt
```

## Getting Started
1. Clone or download this repository to your local machine.
2. Navigate to the directory where the `app.py` file is located.
3. Run the Flask application by clicking on it or executing the following command:

```bash
python app.py
```

The app should now be running, and you can access it by opening a web browser and going to `http://localhost:5000/`.

## Usage
The application provides a menu for the current week, showing meals for each day. The menu is scraped from the following URL: [https://sksdb.hacettepe.edu.tr/YemekListesi.xml](https://sksdb.hacettepe.edu.tr/YemekListesi.xml).

The app displays the menu in a simple HTML format. You can navigate to the root URL (http://localhost:5000/) to see the menu.

The menu is organized by date, and it shows the meal names for each day of the week. If no menu data is available for a specific day, it will display "Yemek bulunamadı" (No meal found).

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.