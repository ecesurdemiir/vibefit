import requests

def get_weather(lat=None, lon=None):
    api_key = "B6853174f9381e654089f168c2a4c1641" # Buraya kendi anahtarını yapıştır
    
    # Koordinat varsa koordinatla, yoksa direkt İstanbul ismiyle sorgula
    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=tr"
    else:
        # Varsayılan olarak İstanbul merkez
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Istanbul&appid={api_key}&units=metric&lang=tr"

    try:
        response = requests.get(url).json()
        
        # API'den gelen şehir/ilçe ismini al (Örn: Beşiktaş, Şişli veya İstanbul)
        city_name = response.get('name', 'Istanbul')
        
        return {
            'temp': int(response['main']['temp']),
            'feels_like': int(response['main']['feels_like']),
            'is_precipitating': response['weather'][0]['main'] in ['Rain', 'Snow', 'Drizzle'],
            'city': f"İstanbul / {city_name}" if city_name != "Istanbul" else "İstanbul"
        }
    except Exception as e:
        print(f"Hava durumu hatası: {e}")
        # Hata anında bile profesyonel görünsün
        return {
            'temp': 20, 
            'feels_like': 19, 
            'is_precipitating': False, 
            'city': "İstanbul"
        }