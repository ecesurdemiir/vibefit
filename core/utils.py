import requests

# Fonksiyonun parantez içini (lat=None, lon=None) olarak güncelledik
def get_weather(lat=None, lon=None):
    # Kendi API anahtarını tırnak içine yapıştır
    api_key = "B6853174f9381e654089f168c2a4c1641" 
    
    # 1. MANTIK: Eğer tarayıcıdan koordinat gelmişse (lat ve lon doluysa)
    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=tr"
    
    # 2. MANTIK: Eğer koordinat yoksa (ilk açılış veya izin reddi) varsayılan şehir
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Istanbul&appid={api_key}&units=metric&lang=tr"

    try:
        response = requests.get(url).json()
        # Django'nun beklediği sözlük yapısını döndürüyoruz
        return {
            'temp': int(response['main']['temp']),
            'feels_like': int(response['main']['feels_like']),
            'is_precipitating': response['weather'][0]['main'] in ['Rain', 'Snow', 'Drizzle'],
            'city': response['name']
        }
    except Exception as e:
        # Bir hata olursa (internet kesilmesi vb.) uygulama çökmesin diye yedek veriler
        print(f"Hava durumu hatası: {e}")
        return {
            'temp': 20, 
            'feels_like': 20, 
            'is_precipitating': False, 
            'city': "Konum Alınamadı"
        }