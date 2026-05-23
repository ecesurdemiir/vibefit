import requests
import os

def get_weather(lat=None, lon=None):
   API_KEY = os.environ.get('WEATHER_API_KEY', '958a754ee97499705b4510c385b74408')
    
    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=tr"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Istanbul&appid={api_key}&units=metric&lang=tr"

    try:
        response = requests.get(url).json()
        return {
            'temp': int(response['main']['temp']),
            'feels_like': int(response['main']['feels_like']),
            'is_precipitating': response['weather'][0]['main'] in ['Rain', 'Snow', 'Drizzle'],
            'city': response.get('name', 'Istanbul')
        }
    except:
        return {'temp': 20, 'city': "Istanbul", 'is_precipitating': False}

# --- YENİ EKLENEN: ŞEHİR İSMİYLE SORGULAMA ---
def get_weather_by_city(city_name):
    api_key = "SENIN_API_KEYIN" # Buraya da aynı keyi yaz
    # q={city_name} parametresi ile şehre göre arama yapıyoruz
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=tr"
    
    try:
        response = requests.get(url).json()
        if response.get('cod') != 200: # Şehir bulunamazsa hata dön
            raise ValueError("Şehir bulunamadı")
            
        return {
            'temp': int(response['main']['temp']),
            'is_precipitating': response['weather'][0]['main'] in ['Rain', 'Snow', 'Drizzle'],
            'city': response.get('name', city_name)
        }
    except:
        # Hata durumunda (internet yoksa veya şehir yanlışsa) varsayılan değerler
        return {
            'temp': 22, 
            'is_precipitating': False, 
            'city': city_name
        }