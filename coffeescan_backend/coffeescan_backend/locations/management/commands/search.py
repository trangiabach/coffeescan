from django.core.management.base import BaseCommand
from locations.models import Location
import requests
from concurrent.futures import ThreadPoolExecutor
import environ

env = environ.Env()
API_KEY = env('GOOGLE_API_KEY')
SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
DISTANCE_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

class Command(BaseCommand):
    help = "Search locations"

    def split(self, list_a, chunk_size):
        for i in range(0, len(list_a), chunk_size):
            yield list_a[i:i + chunk_size]
    
    def make_request(self, origin, locations):
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
    
    def execute_request(self, url):
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

    def handle(self, *args, **options):
        query = input('Search: ')
        search_results = requests.get(SEARCH_URL + 'query=' + query +
                                '&key=' + API_KEY)
        print(search_results.json())
        origin = search_results.json()['results'][0]['formatted_address']
        location_chunks = list(self.split(Location.objects.all(),25))
        matrix_urls = []
        matrix = []
        for locations in location_chunks:
            distance_request, destination_list = self.make_request(origin, locations)
            matrix_urls.append((distance_request, destination_list))
        pool = ThreadPoolExecutor()
        for result in pool.map(self.execute_request, matrix_urls):
            matrix = matrix + result
        matrix.sort(key = lambda x : x['distance']['value'])
        matrix = matrix[:10]
        for mat in matrix:
            for location in Location.objects.all():
                if mat['address'] == location.formatted_address:
                    print(location.name)




        
        
        