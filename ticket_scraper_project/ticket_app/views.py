from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import traceback
import time
from .models import Event
import requests_cache


# Enable caching
requests_cache.install_cache('ticket_cache', expire_after=3600)
ticket_urls = [
    "https://m.damai.cn/shows/item.html?itemId=732414067381&spm=a2o71.category.itemlist.ditem_0",

    "https://m.damai.cn/shows/item.html?itemId=729734893447&spm=a2o71.category.itemlist.ditem_1",

    "https://m.damai.cn/shows/item.html?itemId=729527724624&spm=a2o71.category.itemlist.ditem_2",

    "https://m.damai.cn/shows/item.html?itemId=729733566453&spm=a2o71.category.itemlist.ditem_3",

    "https://m.damai.cn/shows/item.html?itemId=729781644377&spm=a2o71.category.itemlist.ditem_4",

    "https://m.damai.cn/shows/item.html?itemId=729527724225&spm=a2o71.category.itemlist.ditem_5",

    "https://m.damai.cn/shows/item.html?itemId=729739541099&spm=a2o71.category.itemlist.ditem_6",

    "https://m.damai.cn/shows/item.html?itemId=727847135684&spm=a2o71.category.itemlist.ditem_7",

    "https://m.damai.cn/shows/item.html?itemId=732053303688&spm=a2o71.category.itemlist.ditem_8",

    "https://m.damai.cn/shows/item.html?itemId=730872127746&spm=a2o71.category.itemlist.ditem_9",

    "https://m.damai.cn/shows/item.html?itemId=730905114833&spm=a2o71.category.itemlist.ditem_10",

    "https://m.damai.cn/shows/item.html?itemId=732724069419&spm=a2o71.category.itemlist.ditem_11",

    "https://m.damai.cn/shows/item.html?itemId=731634129852&spm=a2o71.category.itemlist.ditem_12",

    "https://m.damai.cn/shows/item.html?itemId=733015839472&spm=a2o71.category.itemlist.ditem_13",

    "https://m.damai.cn/shows/item.html?itemId=731443584089&spm=a2o71.category.itemlist.ditem_14",

    "https://m.damai.cn/shows/item.html?itemId=731848556905&spm=a2o71.category.itemlist.ditem_15",

    "https://m.damai.cn/shows/item.html?itemId=732354775176&spm=a2o71.category.itemlist.ditem_16",

    "https://m.damai.cn/shows/item.html?itemId=729996265914&spm=a2o71.category.itemlist.ditem_17",

    "https://m.damai.cn/shows/item.html?itemId=730268992754&spm=a2o71.category.itemlist.ditem_18",

    "https://m.damai.cn/shows/item.html?itemId=732585805221&spm=a2o71.category.itemlist.ditem_19",

    "https://m.damai.cn/shows/item.html?itemId=731504455233&spm=a2o71.category.itemlist.ditem_20"



    # ... list of ticket URLs ...
]

def scrape_ticket_info(url):
    try:
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)  # Adjust the sleep time as needed

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        title_tag = soup.find('div', class_='title-container-title false false')
        title = title_tag.text.strip() if title_tag else "Title not found"

        date_tag = soup.find('div', class_='notice-overflow')
        date = date_tag.text.strip() if date_tag else "Date not found"

        price_range_tag = soup.find('div', class_='price-range price-range_damai')
        if price_range_tag:
            price_range = price_range_tag.find_all('div', class_='price-range-num')
            min_price = price_range[0].text.strip()
            max_price = price_range[1].text.strip()
            price = f"¥{min_price} - ¥{max_price}"
        else:
            price = "Price not found"

        location_tag = soup.find('div', class_='location-container')
        location = location_tag.find('div', class_='notice-overflow').text.strip() if location_tag else "Location not found"

        ratings_tag = soup.find('span', class_='dm-detail-rating-score-num')
        ratings = ratings_tag.text.strip() if ratings_tag else "Ratings not found"

    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        traceback.print_exc()
        # Initialize variables with default values in case of exception
        title = "Title not found"
        date = "Date not found"
        price = "Price not found"
        location = "Location not found"
        ratings = "Ratings not found"

    finally:
        driver.quit()

    return {
        'title': title,
        'date': date,
        'price': price,
        'location': location,
        'ratings': ratings,
        'url': url
    }

def scrape_all_urls(urls):
    scraped_data = []
    for url in urls:
        scraped_data.append(scrape_ticket_info(url))
    return scraped_data

def home(request):
    return render(request, 'ticket_app/home.html')

def ticket_list(request):
    scraped_info = scrape_all_urls(ticket_urls)

    for ticket_info in scraped_info:
        Event.objects.create(
            title=ticket_info['title'],
            date=ticket_info['date'],
            price=ticket_info['price'],
            location=ticket_info['location'],
            ratings=ticket_info['ratings'],
            url=ticket_info['url']
        )

    events = Event.objects.all()
    return render(request, 'ticket_app/ticket_list.html', {'events': events})