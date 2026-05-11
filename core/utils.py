import requests

def get_weather():
    try:
        # 1. YENİ EKLENTİ: Otomatik Konum Bulucu (İnternet üzerinden şehri bulur)
        loc_url = "http://ip-api.com/json/"
        loc_data = requests.get(loc_url).json()
        
        # Eğer konumu otomatik bulamazsa varsayılan olarak İSTANBUL koordinatlarını kullan
        lat = loc_data.get('lat', 41.01)
        lon = loc_data.get('lon', 28.97)
        city = loc_data.get('city', 'İstanbul')

        # 2. Bulunan o koordinatlara (Enlem ve Boylam) göre hava durumunu çek
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()
        
        temp = weather_data['current_weather']['temperature']
        weather_code = weather_data['current_weather']['weathercode']
        
        # Yağmur veya Kar kontrolü
        is_raining_or_snowing = False
        if weather_code >= 60:
            is_raining_or_snowing = True
            
        return {
            'temp': temp,
            'is_precipitating': is_raining_or_snowing,
            'city': city  # Şehir adını da ekrana yazdırmak için pakete ekledik!
        }
        
    except Exception as e:
        # Hata olursa sistemi çökertme, İstanbul varsayılanıyla devam et
        return {
            'temp': 20,
            'is_precipitating': False,
            'city': 'İstanbul'
        }