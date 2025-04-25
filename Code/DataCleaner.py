import pandas as pd
import csv

hotels = pd.read_csv('hotels.csv')

### Cleans Ratings ###

# converts ratings result to string
hotels['rating'] = hotels['rating'].astype(str)

# removes all rows with rating of N/A
if hotels['rating'].str.contains('nan').any():
    hotels = hotels[hotels.rating != 'nan']
    hotels = hotels.reset_index(drop=True)

# converts ratings result to int
hotels['rating'] = hotels['rating'].astype(float)

### Cleans Prices ###

# Removes $ and , that way they can be converted to floats
hotels['price'] = hotels['price'].str.replace('$', '')
hotels['price'] = hotels['price'].str.replace(',', '')

# converts prices to float
hotels['price'] = hotels['price'].astype(float)

### Removes Outliers ###

# Calculate IQR
Q1 = hotels['price'].quantile(0.25)
Q3 = hotels['price'].quantile(0.75)
IQR = Q3 - Q1

# Define the upper and lower bounds for outliers
lower_bound = Q1 - 1 * IQR
upper_bound = Q3 + 1 * IQR

# Detect outliers
outliers = hotels[(hotels['price'] < lower_bound) | (hotels['price'] > upper_bound)]

# Remove outliers
hotels = hotels[(hotels['price'] >= lower_bound) & (hotels['price'] <= upper_bound)]


# Adds to csv file
hotels.to_csv('HotelsCleaned.csv', header=True, index=False)


'''
RatingMean = hotels['rating'].mean()
RatingMedian = hotels['rating'].median()
PriceMean = hotels['price'].mean()
PriceMedian = hotels['price'].median()

print("The mean rating is: " + str(RatingMean))
print("The median rating is: " + str(RatingMedian))
print("The mean price is: " + str(PriceMean))
print("The median price is: " + str(PriceMedian))
'''