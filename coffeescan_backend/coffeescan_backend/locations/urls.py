from django.urls import path, include
from locations import views

urlpatterns = [
    path('user-location/', views.locate_user),
    path('place-location/', views.locate_places),
]
