import requests
import pandas as pd

cities = ["New Lenox", "Frankfort", "Manhattan", "Mokena", "Orland Park", "Tinley Park", "Lockport", "Homer Glen", "Plainfield", "Lemont", "Palos Park", "Palos Hills", "Bolingbrook"]
columns = ["URL", "Address", "City", "Price", "Beds", "Baths", "Type"]
listings = pd.DataFrame(columns = columns)
url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
headers = {
    'x-rapidapi-host': "realtor.p.rapidapi.com",
    'x-rapidapi-key': "SECRET"
    }

for city in cities:
    print("Populating: " + city)
    querystring = {"beds_min":"2","sort":"relevance","baths_min":"2","price_max":"200000","city":city,"limit":"200","offset":"0","state_code":"IL"}
    response = requests.request("GET", url, headers=headers, params=querystring).json()

    for properties in response["properties"]:
        prop = pd.Series([properties["rdc_web_url"], properties["address"]["line"], properties["address"]["city"], properties["price"], properties["beds"], properties["baths"], properties["prop_type"]],columns)
        listings = listings.append([prop], ignore_index=True)
    
listings = listings[listings["Type"] != "mobile"]
listings = listings[listings["Type"] != "single_family"]
listings = listings.drop(["Type"], axis = 1)
listings = listings.set_index("URL")
listings.to_csv("SAVE LOCATION OF listings.csv")
