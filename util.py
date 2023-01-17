import requests, os, json, datetime

TRANS_LINK_API_KEY = 'YOUR_API_KEY'

if not os.path.exists('cache'):
    os.makedirs('cache')

if not os.path.exists('cache/routes.json'):
    with open('cache/routes.json', 'w') as f:
        f.write('[]')
        f.close()

# !! fix this: slow
def check_cache(route):
    with open('cache/routes.json', 'r') as f:
        cache = json.load(f)
        f.close()
    
    if route in cache:
        return cache[route]
    else:
        return False

# !! kaboom warning: slow, wasteful
def update_cache(route, data):
    with open('cache/routes.json', 'r') as f:
        cache = json.load(f)
        f.close()
    
    cache[route] = data
    
    with open('cache/routes.json', 'w') as f:
        json.dump(cache, f)
        f.close()

def get_coordinates(address):
    route = '/maps/api/geocode/json?key=YOUR_API_KEY&address=' + address
    cache = check_cache(route)
    
    if cache:
        return cache
    
    url = 'https://maps.googleapis.com' + route
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        return data
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
    o = datetime.datetime.strptime(date, "%b-%d-%Y %I:%M %p")
    desired_format = o.strftime("%a, %B %d, %Y at %I:%M %p")
    return desired_format

def lookup(route):
    cache = check_cache(route)
    
    if cache:
        return cache
    
    url = f"https://api.translink.ca/RTTIAPI/V1/stops/{route}?apiKey=" + TRANS_LINK_API_KEY
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
    
    if data['status'] == 'OK':
        update_cache(route, data)
        return data
    else:
        return None