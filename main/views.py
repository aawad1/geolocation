from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GeolocatorStatsForm
from .forms import GeolocatorStatsFormLL
from .models import GeolocatorStats
import requests

def index(request):
    resp = ""
    if request.method == "POST":
        form = GeolocatorStatsForm(request.POST)
        if form.is_valid():
            resp = form.cleaned_data['query']
            form.save()
            return render(request, 'locator.html', {"form": form, "queries": forward_geocode(resp)}) 
    else:
         form = GeolocatorStatsForm()   
    
    context = {"form": form}        
    return render(request, 'locator.html', context=context)

def forward_geocode(address, format='json'):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': format,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    return data
######################################
def coordinates(request):
    # Your view logic goes here
    
    if request.method == "POST":
        form = GeolocatorStatsFormLL(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            form.save()
            return render(request, 'coordinates.html', {"form": form, "place_name": reverse_geocode(latitude, longitude)}) 
    else:
         form = GeolocatorStatsFormLL()   
    
    context = {"form": form}        
    return render(request, "coordinates.html", context=context)

def reverse_geocode(latitude, longitude, format='json'):
    base_url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'lat': latitude,
        'lon': longitude,
        'format': format,
    }

    response = requests.get(base_url, params=params)
    print(response.content)
    data = response.json()

    return data