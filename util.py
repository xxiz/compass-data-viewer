import requests, os, json, datetime

TRANSLINK_API_KEY = os.environ.get('TRANSLINK_API_KEY')
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

if not os.path.exists('cache'):
    os.makedirs('cache')

if not os.path.exists('cache/routes.json'):
    with open('cache/routes.json', 'w') as f:
        f.write('[]')
        f.close()

def check_cache(route):
    with open('cache/routes.json', 'r') as f:
        cache = json.load(f)
        f.close()
    
    if route in cache:
        return cache[route]
    else:
        return False

def update_cache(route, data):
    with open('cache/routes.json', 'r') as f:
        cache = json.load(f)
        f.close()
    
    cache.update({route: data})
    
    with open('cache/routes.json', 'w') as f:
        json.dump(cache, f)
        f.close()

def get_coordinates(address, city='Vancouver', province='BC', country='Canada'):
    location = f'{address}, {city}, {province}, {country}'
    route = f'/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}&'
    
    url = 'https://maps.google.com' + route
    response = requests.get(url)
    data = response.json()
    
    if data.get('status') == 'OK':
        return data.get('results')[0].get('geometry').get('location')
    else:
        return None

def seek_stop_id(transaction):
    
    try:
        location = transaction.split(' at ')[1]
        return location.replace('Bus Stop ', '')
    except:
        if 'AutoLoaded' in transaction:
            return None
        return transaction

def format_datetime(date):
    read_format = datetime.datetime.strptime(date, "%b-%d-%Y %I:%M %p")
    out_format = read_format.strftime("%a, %B %d, %Y at %I:%M %p")
    return out_format

def lookup(route):
    cache = check_cache(route)
    
    if cache:
        return cache

    try:
        url = f"https://api.translink.ca/RTTIAPI/V1/stops/{route}?apiKey=" + TRANSLINK_API_KEY
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        data = {
            'id': r.json().get('StopNo'),
            'name': r.json().get('Name'),
            'location': r.json().get('Name') + ', ' + r.json().get('City'),
            'coordinates': {
                'lat': r.json().get('Latitude'),
                'lng': r.json().get('Longitude'),
            },
            'raw': r.json(),
        }
        update_cache(route, data)
        return data
    except:
        print('Error Got Result: ' + r.text)
        return None
    
    
