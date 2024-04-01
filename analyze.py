import pandas as pd 
from geo import dist_route

df = pd.read_csv('Jan2024.csv')
df['CITY1'] = df['CITY1'].str.upper()
df['CITY1'] = df['CITY1'].str.strip()

df['CITY2'] = df['CITY2'].str.upper()
df['CITY2'] = df['CITY2'].str.strip()

df['TOTAL'] = df['TOTAL'].str.replace(',', '')
df['TOTAL'] = df['TOTAL'].astype(int)


def get_ridership(route, direction="both"):
    # city_pairs = {(city1, city2) for city1 in route for city2 in route if city1 != city2}
    city_pairs1 = set()
    city_pairs2 = set()
    for i in range(len(route)):
        for j in range(i+1, len(route)):
            city_pairs1.add((route[i], route[j]))

    for i in range(len(route)):
        for j in range(i+1, len(route)):
            city_pairs2.add((route[j], route[i]))
    
    if direction=="both":
        city_pairs = city_pairs1 | city_pairs2
    elif direction=="->":
        city_pairs = city_pairs1
    elif direction=="<-":
        city_pairs = city_pairs2
    
    filtered_df = df[df[['CITY1', 'CITY2']].apply(tuple, axis=1).isin(city_pairs)]
    total_sum = filtered_df['TOTAL'].sum()

    return total_sum

#hsr_route = ['DELHI', 'AGRA', 'KANPUR', 'LUCKNOW', 'ALLAHABAD', 'VARANASI', 'PATNA', 'KOLKATA']
hsr_routes = [
    ['AHMEDABAD', 'VADODARA', 'SURAT', 'MUMBAI'],
    ['DELHI', 'JAIPUR', 'KISHANGARH', 'UDAIPUR', 'AHMEDABAD', 'VADODARA', 'SURAT', 'MUMBAI'],
    ['DELHI', 'JAIPUR', 'KISHANGARH', 'UDAIPUR', 'AHMEDABAD', 'VADODARA', 'SURAT', 'MUMBAI', 'PUNE'],
    ['DELHI', 'AGRA', 'GWALIOR', 'BHOPAL', 'NAGPUR', 'HYDERABAD', 'BENGALURU'],
    ['MUMBAI', 'PUNE', 'KALABURAGI', 'HYDERABAD'],
    ['HYDERABAD', 'VIJAYWADA', 'RAJAHMUNDRY', 'VISAKHAPATNAM'],
    ['MUMBAI', 'PUNE', 'BENGALURU', 'CHENNAI'],
    ['MUMBAI', 'PUNE', 'KOLHAPUR', 'BELGAUM', 'HUBLI', 'BENGALURU', 'CHENNAI'],
    ['DELHI', 'CHANDIGARH', 'AMRITSAR'],
    ['MUMBAI', 'DABOLIM', 'MANGALORE', 'KANNUR', 'KOZHIKODE', 'KOCHI','TRIVANDRUM'],
    ['BENGALURU', 'HYDERABAD'],
    ['BENGALURU', 'CHENNAI'],
    ['HYDERABAD', 'VIJAYWADA', 'TIRUPATI', 'CHENNAI'],
    ['DELHI', 'AGRA', 'KANPUR', 'LUCKNOW', 'ALLAHABAD', 'VARANASI', 'PATNA', 'KOLKATA'],
    ['BENGALURU', 'COIMBATORE', 'KOCHI', 'TRIVANDRUM']
]


for route in hsr_routes:
    d = int(dist_route(route))
    ridership = int(get_ridership(route))
    daily_r = int(ridership/30)
    r_per_km = int(ridership/d)
    string_route = "-".join([i.capitalize() for i in route])
    print(f"|{string_route}|{d}|{daily_r}|{r_per_km}|")


