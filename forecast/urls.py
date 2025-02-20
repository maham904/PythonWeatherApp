# forecast/urls.py
from django.urls import path
from . import views
from .weather_dashboard import weather_plot

urlpatterns = [
    path('', views.weather_dashboard, name='weather_dashboard'),
    path('weather-plot/', weather_plot, name='weather_plot'),
    # Add other URL patterns here if needed
]
