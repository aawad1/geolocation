from django.db import models

class GeolocatorStats(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    geocoding_type = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    latitude = models.DecimalField( max_digits=30, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField( max_digits=30, decimal_places=20, null=True, blank=True)
    
    def __str__(self):
        return f"Geocoding request - ID: {self.id}, query: {self.query}, latitude: {self.latitude}, longitude: {self.longitude}"