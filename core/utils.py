import os
import requests

def get_weather(lat=None, lon=None):
    API_KEY = os.environ.get('WEATHER_API_KEY') 
    
    if not lat or not lon:
        lat, lon = "41.0082", "28.9784"
        
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url).json()
        return {
            'temp': int(response['main']['temp']),
            'feels_like': int(response['main']['feels_like']),
            'is_precipitating': any(k in response for k in ['rain', 'snow']),
            'city': response.get('name', 'Istanbul')
        }
    except Exception:
        return {'temp': 20, 'feels_like': 20, 'is_precipitating': False, 'city': 'Istanbul'}

def get_weather_by_city(city_name):
    API_KEY = os.environ.get('WEATHER_API_KEY')
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url).json()
        if response.get('cod') != 200:
            raise ValueError("Şehir bulunamadı")
            
        return {
            'temp': int(response['main']['temp']),
            'is_precipitating': any(k in response for k in ['rain', 'snow']),
            'city': response.get('name', city_name)
        }
    except Exception:
        return {'temp': 22, 'is_precipitating': False, 'city': city_name}