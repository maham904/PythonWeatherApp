import requests
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# OpenWeatherMap API Key
API_KEY = "cbe3891b8233c37b2fb6ba869fb5f944"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        if city:
            weather_data = get_weather(city)
            if weather_data is None:
                weather_data = {'error': 'City not found!'}
    return render_template('index.html', weather_data=weather_data)

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("cod") != 200:
        return None

    # Extract weather details
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    weather_desc = data["weather"][0]["description"].capitalize()

    # Create weather data dictionary
    weather_info = {
        "temp": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "description": weather_desc
    }
    return weather_info

@app.route('/weather_plot.png')
def weather_plot():
    weather_data = get_weather("Lahore")  # Default city
    if not weather_data:
        return "Error: City not found"
    # Plotting
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(['Temperature', 'Feels Like', 'Humidity'], [weather_data['temp'], weather_data['feels_like'], weather_data['humidity']], color=["blue", "orange", "green"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Value")
    ax.set_title("Weather Dashboard")

    # Save plot to a BytesIO object
    canvas = FigureCanvas(fig)
    output = 'static/weather_plot.png'
    canvas.print_figure(output)
    return output

if __name__ == "__main__":
    app.run(debug=True)
