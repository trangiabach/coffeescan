from django.core.management.base import BaseCommand
from locations.models import Location
import requests
import environ

env = environ.Env()

API_KEY = env('GOOGLE_API_KEY')
URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'

class Command(BaseCommand):
    help = "Geo-locate locations"

    def handle(self, *args, **options):
        locations = Location.objects.all()
        for location in locations:
            try: 
                r = requests.get(URL + 'query=' + location.location +
                            '&key=' + API_KEY)
                result = r.json()['results'][0]['geometry']['location']
                location.latitude = result['lat']
                location.longitude = result['lng']
                location.save()
                print('Geo-located location: %s' % (location.name,))
            except:
                print('Cannot geo-locate for %s' % (location.name,))
