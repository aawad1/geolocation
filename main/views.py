from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GeolocatorStatsForm
from .forms import GeolocatorStatsFormHistory
from .models import GeolocatorStats
import requests
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# HOW TO DEAL WITH ERROR MESSAGES 
history = []
error_message = ""
#navbar, history, about, home
def index(request):
    resp = ""
    error_message = ""  # Initialize error_message here

    if request.method == "POST":
        form = GeolocatorStatsForm(request.POST)

        if form.is_valid():
            resp = form.cleaned_data['query']
            result = validate_input(resp)

            if result is None:
                error_message = "Invalid input. Please enter valid coordinates or location name."
                context = {"form": form, "error": error_message}
                return render(request, 'locator.html', context=context)

            if len(result) == 1:
                fwg = forward_geocode(resp)

                if not fwg:
                    context = {"form": form, "error": "Could not find the location"}
                    return render(request, 'locator.html', context=context)
                else:
                    # Create an instance of GeolocatorStats using form data
                    gls = form.save(commit=False)
                    gls.query = fwg[0]['name']
                    gls.latitude = fwg[0]['lat']
                    gls.longitude = fwg[0]['lon']
                    gls.save()  
                    
                    return render(request, 'locator.html', {"form": form, "queries": fwg[0]})
            elif len(result) == 2:
                [lat, lon] = result
                rvg = reverse_geocode(lat, lon)
                gls = form.save(commit=False)
                gls.query = rvg['name']
                gls.latitude = rvg['lat']
                gls.longitude = rvg['lon']
                gls.save()  
                return render(request, 'locator.html', {"form": form, "queries": rvg})

    else:
        form = GeolocatorStatsForm()

    context = {
        "form": form,
        "error": error_message
    }

    return render(request, 'locator.html', context=context)

def validate_input(input_str):
    # Split the input into two numbers
    parts = re.split(r',', input_str)

    try:
        if len(parts) == 2:
            # Convert the parts to floats
            latitude, longitude = map(float, parts)
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                return [latitude, longitude]
            else:
                raise ValueError("Invalid latitude or longitude range.")
                
        elif len(parts) > 2:
            raise ValueError("Input must be a comma-separated pair of coordinates.")
        else:
            return [input_str]
    except ValueError as e:
        global error_message
        error_message = str(e)
        print(error_message)
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
    all_history = GeolocatorStats.objects.all()
    items_per_page = 10
    paginator = Paginator(all_history, items_per_page)
    page = request.GET.get('page')
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)
        
    context = {'history': history}
    return render(request, "history.html", context)