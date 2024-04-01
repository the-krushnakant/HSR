from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd

csv_file = 'coordinates.csv'
df = None

def get_coordinates(city_name):
    """
    Get the latitude and longitude coordinates of a city using its name.
    Returns a tuple (latitude, longitude).
    """
    global df 

    if df is None:
        df = pd.read_csv(csv_file)
    
    try:
        i = df['city'] == city_name
        if i.any():
            res = df.loc[i, ['latitude', 'longitude']]
            return tuple(res.iloc[0])
    
    except:
        pass


    geolocator = Nominatim(user_agent="city_distance_calculator")

    temp_city_name = city_name + ", India"
    
    location = geolocator.geocode(temp_city_name, timeout=1000)

    if location:
        tuple_to_append = (city_name, location.latitude, location.longitude)
        df = pd.DataFrame([tuple_to_append])
        df.to_csv(csv_file, mode='a', index=False, header=False)
        return location.latitude, location.longitude
    else:
        return None

def dist(city1, city2):
    """
    Calculate the aerial distance between two cities given their names.
    Returns the distance in kilometers.
    """
    coordinates1 = get_coordinates(city1)
    coordinates2 = get_coordinates(city2)

    if coordinates1 and coordinates2:
        distance = great_circle(coordinates1, coordinates2).kilometers
        return distance
    else:
        return None

def dist_route(route):
    sum = 0
    for i in range(len(route)-1):
        m = dist(route[i], route[i+1])
        #print(f'distance from {route[i]} to {route[i+1]} is {m:.1f}')
        sum += m
    return sum



