import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import numpy as np

#Training Data
listings = pd.read_csv("C:/Users/micha/Documents/Python/Real Estate/Condos, Townhomes, Homes/realestaterating/listingsTrained.csv")
listings = listings.set_index("URL")
columns = ["City", "Price", "Beds", "Baths", "Ratings"]
listings = listings[columns]
listings["Price"] = listings["Price"] / 100000
CityS = pd.get_dummies(listings["City"])
listings = listings.drop(["City"], axis = 1)
listings = listings.join(CityS, how = "outer")
listingsTrainY = listings["Ratings"]
listingsTrainX = listings.drop("Ratings",axis = 1)

#Testing Data
listingsTest = pd.read_csv("C:/Users/micha/Documents/Python/Real Estate/Condos, Townhomes, Homes/realestaterating/listings.csv")
listingsTest = listingsTest.set_index("URL")
addressSeries = listingsTest["Address"]
listingsTest = listingsTest[["City", "Price", "Beds", "Baths"]]
listingsTest["Price"] = listingsTest["Price"] / 100000
citySeries = listingsTest["City"]
CityS = pd.get_dummies(listingsTest["City"])
listingsTest = listingsTest.drop(["City"], axis = 1)
listingsTest = listingsTest.join(CityS, how = "outer")

#Model Fit & Predictions
model = LinearRegression().fit(listingsTrainX,listingsTrainY)
predictions = model.predict(listingsTest).round()
listingsTest["Ratings"] = predictions
listingsTest["Price"] = listingsTest["Price"] * 100000
print(model.intercept_)
print(model.coef_)
listingsTest = listingsTest.join(citySeries, how = "outer")
listingsTest = listingsTest.join(addressSeries, how = "outer")
listingsTest = listingsTest[["Address", "City","Price", "Beds", "Baths", "Ratings"]]
listingsTest.to_csv("C:/Users/micha/Documents/Python/Real Estate/Condos, Townhomes, Homes/realestaterating/listingsRated.csv")