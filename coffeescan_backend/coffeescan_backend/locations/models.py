from django.db import models
from django.utils.timezone import now
from decimal import Decimal


# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField()
    url = models.TextField(default="")
    location = models.CharField(max_length=500)
    space_desc = models.TextField(default="")
    coffee_desc = models.TextField(default="")
    latitude = models.DecimalField(max_digits=50, decimal_places=6, default=Decimal(1))
    longitude = models.DecimalField(max_digits=50, decimal_places=6, default=Decimal(1))
    formatted_address = models.TextField(default="")
    date_added = models.DateTimeField(default=now)

    class Meta:
        ordering = ('date_added',)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    location = models.ForeignKey(Location, related_name='tags', on_delete=models.CASCADE)
    name = models.TextField()
    date_added = models.DateTimeField(default=now)

    class Meta:
        ordering = ('date_added',)
    
    def __str__(self):
        return self.name

class SideImage(models.Model):
    location = models.ForeignKey(Location, related_name='side_images', on_delete=models.CASCADE)
    url = models.TextField(default="")
    date_added = models.DateTimeField(default=now)

    class Meta:
        ordering = ('date_added',)
    
    def __str__(self):
        return self.url

    
