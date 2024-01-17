from django import forms 
from .models import GeolocatorStats

class GeolocatorStatsForm(forms.ModelForm): #indicira da se radi o formi kreiranoj na osnovu modela
    class Meta:
        model=GeolocatorStats
        fields=["query"]
    def __init__(self, *args, **kwargs):
        super(GeolocatorStatsForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({"class": "form-control", "placeholder": "Enter geocoding query"})
    