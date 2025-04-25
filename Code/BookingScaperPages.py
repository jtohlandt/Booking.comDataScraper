from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
pageUrl = 'https://www.booking.com/searchresults.html?ss=New+York%2C+New+York+State%2C+United+States&label=gen173nr-1FCAEoggI46AdIM1gEaJQCiAEBmAExuAEXyAEM2AEB6AEB-AECiAIBqAIDuALzz8KrBsACAdICJDQxNjA1NzlkLWMzNjAtNDYwYS04ZjhmLTFkOTkxOGI1MzViMNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=20088325&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=2bbf7739e14d00ff&ac_meta=GhAyYmJmNzczOWUxNGQwMGZmIAAoATICZW46BG5ldyBAAEoAUAA%3D&checkin=2024-01-31&checkout=2024-02-01&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
driver.get(pageUrl)

hotels_list = []

# Gets total number of pages.
total = int(driver.find_element(By.CSS_SELECTOR, 'div[data-testid="pagination"]  li:last-child').text)


def get_hotel_total():
    url = pageUrl
    for i in range(0, total):
        get_hotel_data(url)
        # moves simulation to next page
        next_page_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Next page")]')
        next_page_button.click()
        # updates url for get_hotel_data
        url = driver.current_url
    # Converted the list to the dataframe
    hotels = pd.DataFrame(hotels_list)
    # Added a header column
    hotels.head()
    print(hotels)
    # Adds to csv file
    hotels.to_csv('hotels.csv', header=True, index=False)


# Adds a page of hotels to the list
def get_hotel_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # property card is each hotel listing
    hotels = soup.findAll('div', {'data-testid': 'property-card'})

    for hotel in hotels:

        # Retrieved elem that each piece of data is in
        name_element = hotel.find('div', {'data-testid': 'title'})
        location_element = hotel.find('span', {'data-testid': 'address'})
        price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        rating_element = hotel.find('div', {'class': 'a3b8729ab1 d86cee9b25'})

        # Stripped each piece of information
        name = name_element.text.strip()
        location = location_element.text.strip()
        price = price_element.text.strip()

        # If else statement to check if rating exists. If not, it is set to N/A
        if rating_element:
            rating = rating_element.text.strip()
        else:
            rating = "N/A"

        # Added various information to the list
        hotels_list.append({
            'name': name,
            'location': location,
            'price': price,
            'rating': rating
        })
    return hotels


get_hotel_total()
