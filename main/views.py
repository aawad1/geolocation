from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GeolocatorStatsForm
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
    if resp!="":     
        context = {"form": form, "queries": forward_geocode(resp)} 
    else:
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