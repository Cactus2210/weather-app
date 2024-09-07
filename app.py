from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Load the OpenWeatherMap API key from environment variables
API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if weather_data:
            return render_template('weather.html', weather=weather_data)
        else:
            return render_template('weather.html', error="City not found")
    return render_template('weather.html')

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
    return None

if __name__ == '__main__':
    app.run(debug=True)
