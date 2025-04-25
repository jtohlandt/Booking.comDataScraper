from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaJQCiAEBmAExuAEXyAEM2AEB6AEB-AECiAIBqAIDuALY7birBsACAdICJDU5ZmY1YTFkLTNkZmItNDA1OS1hZmE5LTU0NWFmYWQ0OTk3YdgCBeACAQ&aid=304142&ss=Carlsbad%2C+California%2C+United+States&lang=en-us&sb=1&src_elem=sb&dest_id=20012027&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=df40902c82b502ea&ac_meta=GhBkZjQwOTAyYzgyYjUwMmVhIAAoATICZW46BGNhcmxAAEoAUAA%3D&checkin=2024-01-22&checkout=2024-01-25&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=popularity'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

# property card is each hotel listing
hotels = soup.findAll('div', {'data-testid': 'property-card'})

hotels_list = []


for hotel in hotels:

    # Retrieved elem that each piece of data is in
    name_elem = hotel.find('div', {'data-testid': 'title'})
    location_elem = hotel.find('span', {'data-testid': 'address'})
    price_elem = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
    rating_elem = hotel.find('div', {'class': 'a3b8729ab1 d86cee9b25'})

    # Stripped each piece of information
    name = name_elem.text.strip()
    location = location_elem.text.strip()
    price = price_elem.text.strip()
    rating = rating_elem.text.strip()

    # Added various information to the list
    hotels_list.append({
        'name': name,
        'location': location,
        'price': price,
        'rating': rating
    })
    # Converted the list to the dataframe
    hotels = pd.DataFrame(hotels_list)
# Added a header column
hotels.head()

print(hotels)
#Adds to csv file
hotels.to_csv('hotels.csv', header=True, index=False)