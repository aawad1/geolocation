from django import forms 
from .models import GeolocatorStats

class GeolocatorStatsForm(forms.ModelForm): #indicira da se radi o formi kreiranoj na osnovu modela
    class Meta:
        model=GeolocatorStats
        fields=["query"]
    def __init__(self, *args, **kwargs):
        super(GeolocatorStatsForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({"class": "form-control", "placeholder": "Enter geocoding query"})
    
class  GeolocatorStatsFormLL(forms.ModelForm):
    class Meta:
        model=GeolocatorStats
        fields=["latitude", "longitude"]
        
    def __init__(self, *args, **kwargs):
        super(GeolocatorStatsFormLL, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs.update({"class": "form-control", "placeholder": "Enter latitude"})
        self.fields['longitude'].widget.attrs.update({"class": "form-control", "placeholder": "Enter longitude"})    
    
    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        if latitude < -90 or latitude > 90:
            raise forms.ValidationError("Latitude must be between -90 and 90 degrees.")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        if longitude < -180 or longitude > 180:
            raise forms.ValidationError("Longitude must be between -180 and 180 degrees.")
        return longitude