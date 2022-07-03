from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Location, Tag, SideImage
import environ
import requests
from concurrent.futures import ThreadPoolExecutor
from django.forms.models import model_to_dict

env = environ.Env()
API_KEY = env('GOOGLE_API_KEY')
SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
DISTANCE_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
HANOI_LOCATION = '21.028511%2C-105.804817'

def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]

def make_request(origin, locations):
    destinations = ''
    destinations_list = []
    for location in locations:
        if location.formatted_address == '':
            continue
        else:
            destinations = destinations + location.formatted_address + '|'
            destinations_list.append(location.formatted_address)
    destinations = destinations[:-1] 
    request = DISTANCE_MATRIX_URL + 'origins=' + origin + '&destinations=' + destinations + '&key=' + API_KEY
    return request, destinations_list

def execute_request(url):
        distance_results = requests.get(url[0])
        distance_results = distance_results.json()
        addresses = url[1]
        distances = distance_results['rows'][0]['elements']
        results = []
        for i in range(len(addresses)):
            try:
                obj = {}
                obj['address'] = addresses[i]
                obj['distance'] = distances[i]['distance']
                obj['duration'] = distances[i]['duration']
                results.append(obj)
            except:
                continue
        return results

@api_view(['POST'])
def locate_user(request):
    print(request.data)
    query = request.data['query']
    search_results = requests.get(SEARCH_URL + 'input=' + query +
                            '&location=' + 
                            '&key=' + API_KEY)
    origin = search_results.json()['results']
    return Response(origin)

@api_view(['POST'])
def locate_places(request):
    origin = request.data['query']
    location_chunks = list(split(Location.objects.all(),25))
    matrix_urls = []
    matrix = []
    for locations in location_chunks:
        distance_request, destination_list = make_request(origin, locations)
        matrix_urls.append((distance_request, destination_list))
    pool = ThreadPoolExecutor()
    for result in pool.map(execute_request, matrix_urls):
        matrix = matrix + result
    matrix.sort(key = lambda x : x['distance']['value'])
    matrix = matrix[:10]
    final_res = []
    for mat in matrix:
        location = Location.objects.filter(formatted_address=mat['address']).first()
        tags = Tag.objects.filter(location=location)
        location = model_to_dict(location)
        location['tags'] = []
        for tag in tags:
            if len(tag.name) > 20:
                continue
            location['tags'].append(model_to_dict(tag))
        location['distance'] = mat['distance']['text']
        location['duration'] = mat['duration']['text']
        if location not in final_res:
            final_res.append(location)
    return Response(final_res)




