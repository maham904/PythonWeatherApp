import io

import requests
from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

# OpenWeatherMap API Key
API_KEY = "cbe3891b8233c37b2fb6ba869fb5f944"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    # API Request to OpenWeatherMap
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("cod") != 200:
        return None

    # Extract necessary weather data
    weather_info = {
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize()
    }

    return weather_info

def weather_dashboard(request):
    weather_data = None
    city = ''

    if request.method == 'POST':
        city = request.POST.get('city')  # Get city name from form input
        if city:
            weather_data = get_weather(city)
            if not weather_data:
                weather_data = {'error': 'City not found!'}

    return render(request, 'forecast/index.html', {'weather_data': weather_data, 'city': city})

def weather_plot(request):
    """ Generate a simple weather-related plot and return as an image response """
    plt.figure(figsize=(5, 3))
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])  # Example plot
    plt.xlabel("Days")
    plt.ylabel("Temperature")
    plt.title("Temperature Trend")

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

