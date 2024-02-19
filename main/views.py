from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GeolocatorStatsForm
from .forms import GeolocatorStatsFormHistory
from .models import GeolocatorStats
import requests
import re

# HOW TO DEAL WITH ERROR MESSAGES 
history = []
#navbar, history, about, home
def index(request):
    resp = ""
    if request.method == "POST":
        form = GeolocatorStatsForm(request.POST)
        print(form)
        if form.is_valid():
            resp = form.cleaned_data['query']
            result = validate_input(resp)
            print(result)
            #provjeriti unos da li je koordinate ili naziv, mozda koristiti regex
            if(result==None):
                context = {"form": form}  
                return render(request,'locator.html', context=context)
            if(len(result) == 1):
                print(resp)
                fwg = forward_geocode(resp)
                if(not fwg):
                    context = {"form": form}  
                    return render(request,'locator.html', context=context)
                else:
                    form.instance.query = fwg[0].get('name')
                    form.instance.latitude = fwg[0].get('latitude')
                    form.instance.longitude = fwg[0].get('longitude')
                    print(form)
                    #history.append(fwg[0])

                    form.save()
                    return render(request, 'locator.html', {"form": form, "queries": fwg[0]})
            elif(len(result) == 2):
                [lat, lon] = result
                rvg = reverse_geocode(lat, lon)
                print(rvg)
                form.save()
                return render(request, 'locator.html', {"form": form, "queries": rvg})
                
    else:
         form = GeolocatorStatsForm()   
    
    context = {"form": form}        
    #stats = GeolocatorStats.objects.all() #object related mapper (ORM)
    #history = stats
    #context['stats'] = stats
    #print(stats)
    return render(request, 'locator.html', context=context)

def validate_input(input_str):
    # Split the input into two numbers
    parts = re.split(r',', input_str)

    try:
        if(len(parts) > 1):
            # Convert the parts to floats
            latitude, longitude = map(float, parts)
            return [latitude,longitude]
            # Check if latitude and longitude are within the valid range
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                return [latitude, longitude]
            else:
                return [200,200]
        else:
            return [input_str]
    except ValueError:
        return None
def forward_geocode(address, format='json'):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': format,
    }

    response = requests.get(base_url, params=params)
    
    data = response.json()
    print(data)
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
            return render(request, 'coordinates.html', {"form": form, "place_name": reverse_geocode(latitude, longitude)[0]}) 
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
    print(data)
    return data

##############################
def about(request):
    return render(request, "about.html")

##############################
def history(request):
    history = GeolocatorStats.objects.all()
    return render(request, "history.html", {'history': history})
