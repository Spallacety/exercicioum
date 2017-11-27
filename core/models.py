from django.db import models

class WeatherForecast(models.Model):
  max = models.CharField(max_length=255, null=False)
  min = models.CharField(max_length=255, null=False)
  rain_probability = models.CharField(max_length=255, null=False)
  created_at = models.DateTimeField(auto_now_add=True)