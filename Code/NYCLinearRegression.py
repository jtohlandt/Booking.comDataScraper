from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

hotels = pd.read_csv('HotelsCleaned.csv')


# Prepare the data for linear regression
X = hotels[['rating']]
y = hotels['price']

# Create and fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Make linear regression line
predictions = model.predict(X)

# Width and height of graph
plt.figure(figsize=(8, 6))

# Plots the data
plt.scatter(X, y, label='Data')

# Plots the linear regression line
plt.plot(X, predictions, color='red', label='Linear Regression')

# Adds labels and legend
plt.title('Hotel Prices vs. Ratings with Linear Regression')
plt.xlabel('Rating')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

# R Squared Value

R2 = model.score(X, y)

#print(R2)

R2 = str(R2.item())

print("The R Squared Value is "+R2)

# Root Mean Squared Error

MSE = mean_squared_error(y, predictions)
RMSE = MSE ** 0.5

#print(RMSE)

RMSE = str(RMSE.item())
print("The Root Mean Squared Error is "+RMSE)

