from django.core.management.base import BaseCommand
from locations.models import Location, Tag, SideImage
import pandas as pd

DATA_DIR = 'D:/Mentorship_Platform/coffeescan/coffeescan_backend/coffeescan_backend/locations/management/commands/data/data.csv'

class Command(BaseCommand):
    help = "collect locations"

    def preprocess(self, caption):
        data = caption.split('\n')
        title = data[0].split(' - ')
        name = title[0].replace('[ ', '')
        slug = name.replace(' ', '-')
        location = title[1].replace(' ]', '')
        tags = []
        space_desc = ''
        coffee_desc = ''
        for tag in data[1:]:
            if '📍' in tag:
                space_desc = tag
            elif '☕️' in tag:
                coffee_desc = tag
            else:
                tags.append(tag)
        return name, slug, location, space_desc, coffee_desc, tags

    def handle(self, *args, **options):
        df = pd.read_csv(DATA_DIR)
        df = df.reset_index() 
        prev = ''
        parent = None
        for index, row in df.iterrows():
            if row['error'] == 'Not a post URL':
                continue
            if prev == row['query']:
                print('create side images for location: %s' % (parent.name,))
                try:
                    SideImage.objects.get_or_create(
                        location=parent,
                        url=row['imgUrl'],
                    )
                    print('%s added' % (row['imgUrl'],))
                except:
                    print('%s already exists or cannot be added' % (row['imgUrl'],))

            else:
                print('Adding new location at index %s' % (index,))
                try:
                    name, slug, location, space_desc, coffee_desc, tags = self.preprocess(row['description'])
                    try:
                        parent, created = Location.objects.get_or_create(
                        name=name,
                        slug=slug,
                        url = row['imgUrl'],
                        location = location,
                        space_desc=space_desc,
                        coffee_desc = coffee_desc
                        )
                        print('%s added' % (name,))
                    except:
                        print('%s already exists or cannot be added' % (name,)) 
                    for name in tags:
                        try:
                            Tag.objects.get_or_create(
                                location=parent,
                                name=name,
                            )
                            print('%s added' % (name,))
                        except:
                            print('%s already exists or cannot be added' % (name,))
                except:
                    print('Failed to add new location at index %s' % (index,))
                    continue
            prev = row['query']