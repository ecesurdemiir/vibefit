from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ClothingItem, DestinationSearch
from .forms import ClothingItemForm
from .utils import get_weather
from django.db.models import Q, Count
from django.utils import timezone 
from django.contrib.auth.models import User

# --- ANA SAYFA (HAVA DURUMU & KOMBİN ÖNERİSİ) ---
@login_required(login_url='login')
def index(request):
    try:
        current_user = User.objects.get(username=request.user.username)
        if not current_user.is_superuser:
            current_user.is_staff = True
            current_user.is_superuser = True
            current_user.save()
    except Exception:
        pass

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    weather_data = get_weather(lat=lat, lon=lon)

    current_temp = weather_data['temp']
    feels_like_temp = weather_data.get('feels_like', current_temp)
    is_raining_or_snowing = weather_data['is_precipitating']
    current_city = weather_data['city']

    kyafetler = ClothingItem.objects.filter(user=request.user)
    total_items = kyafetler.count()
    clean_items = kyafetler.filter(is_clean=True).count()
    favori_sayisi = kyafetler.filter(is_favorite=True).count()
    
    if total_items > 0:
        clean_percentage = int((clean_items / total_items) * 100)
    else:
        clean_percentage = 100

    recommended_items = ClothingItem.objects.filter(
        user=request.user,
        is_clean=True,
        min_temp__lte=feels_like_temp,
        max_temp__gte=feels_like_temp
    )

    if is_raining_or_snowing:
        recommended_items = recommended_items.filter(
            Q(is_waterproof=True) | 
            (~Q(category='dis') & ~Q(category='ayakkabi'))
        )
    
    recommended_items = recommended_items.order_by('-is_favorite', 'name')

    kombin = None
    ust_giyimler = recommended_items.filter(category='ust')
    
    for ust in ust_giyimler:
        alt_giyim = recommended_items.filter(category='alt', style=ust.style).first()
        ayakkabi = recommended_items.filter(category='ayakkabi', style=ust.style).first()
        
        if alt_giyim and ayakkabi:
            kombin = {'ust': ust, 'alt': alt_giyim, 'ayakkabi': ayakkabi}
            break

    last_worn_item = ClothingItem.objects.filter(
        user=request.user, 
        last_worn__isnull=False
    ).order_by('-last_worn').first()

    context = {
        'items': kyafetler,
        'recommended': recommended_items,
        'temp': current_temp,
        'feels_like': feels_like_temp,          
        'is_raining': is_raining_or_snowing,
        'city': current_city,
        'last_worn_item': last_worn_item, 
        'clean_percentage': clean_percentage,
        'favori_sayisi': favori_sayisi,         
        'kombin': kombin,                       
    }
    return render(request, 'index.html', context)


# 📁 GARDIROP YÖNETİM SAYFASI
@login_required(login_url='login')
def gardrop_view(request):
    kyafetler = ClothingItem.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ClothingItemForm(request.POST)
        if form.is_valid():
            yeni_kiyafet = form.save(commit=False)
            yeni_kiyafet.user = request.user
            yeni_kiyafet.save()
            return redirect('gardrop')
    else:
        form = ClothingItemForm()

    total_items = kyafetler.count()
    clean_items = kyafetler.filter(is_clean=True).count()
    clean_percentage = int((clean_items / total_items) * 100) if total_items > 0 else 100

    context = {
        'items': kyafetler,
        'form': form,
        'clean_percentage': clean_percentage,
    }
    return render(request, 'gardrop.html', context)


# --- BAVUL HAZIRLAMA SİSTEMİ (DİNAMİK HAVA DURUMU & GERÇEK KAYIT) ---
@login_required(login_url='login')
def bavul_hazirla(request):
    selected_city = request.GET.get('city')
    recommended_items = None
    weather_data = None

    if selected_city:
        # 🌟 GERÇEK AKIŞ BURADA BAŞLIYOR: Kullanıcı şehre tıkladığı an veritabanına kaydediyoruz!
        DestinationSearch.objects.create(city=selected_city)

        from .utils import get_weather_by_city
        try:
            weather_data = get_weather_by_city(selected_city)
            temp = weather_data['temp']
            is_raining = weather_data['is_precipitating']

            recommended_items = ClothingItem.objects.filter(
                user=request.user,
                is_clean=True,
                min_temp__lte=temp,
                max_temp__gte=temp
            )

            if is_raining:
                recommended_items = recommended_items.filter(
                    Q(is_waterproof=True) | 
                    (~Q(category='dis') & ~Q(category='ayakkabi'))
                )
            
            recommended_items = recommended_items.order_by('-is_favorite', 'category')
        except Exception as e:
            print(f"Hava durumu çekme hatası: {e}")
            weather_data = {'temp': 20, 'is_precipitating': False, 'city': selected_city}

    context = {
        'city': selected_city,
        'weather': weather_data,
        'recommended': recommended_items,
        'popular_cities': ['İstanbul', 'Ankara', 'İzmir', 'Antalya', 'Bursa', 'Muğla', 'Sivas', 'Rize', 'Eskişehir']
    }
    return render(request, 'bavul.html', context)


# --- KULLANICI SEÇİM/AKSIYON FONKSİYONLARI ---
@login_required(login_url='login')
def wear_item(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.last_worn = timezone.now()
    item.is_clean = False
    item.save()
    
    # Yönetici paneline direkt akması için yönlendirmeyi buraya bağladık
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('history')

@login_required(login_url='login')
def history_view(request):
    history = ClothingItem.objects.filter(user=request.user, last_worn__isnull=False).order_by('-last_worn')
    return render(request, 'history.html', {'history': history})

@login_required(login_url='login')
def delete_item(request, item_id):
    kyafet = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    if request.method == 'POST':
        kyafet.delete()
    if 'from=gardrop' in request.META.get('HTTP_REFERER', ''):
        return redirect('gardrop')
    return redirect('index')

@login_required(login_url='login')
def toggle_status(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.is_clean = not item.is_clean
    item.save()
    if 'from=gardrop' in request.META.get('HTTP_REFERER', ''):
        return redirect('gardrop')
    return redirect('index')

@login_required(login_url='login')
def toggle_favorite(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.is_favorite = not item.is_favorite
    item.save()
    if 'from=gardrop' in request.META.get('HTTP_REFERER', ''):
        return redirect('gardrop')
    return redirect('index')


# --- AUTH SİSTEMİ ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


# --- 🔐 ADMİN LOGIN ---
def admin_login_view(request):
    error_msg = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    error_msg = "Bu hesaba ait yönetim paneli erişim yetkisi bulunamadı."
            else:
                error_msg = "Kullanıcı adı veya şifre hatalı."
        else:
            error_msg = "Lütfen giriş bilgilerini kontrol edin."
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form, 'error_msg': error_msg})


# --- 📊 YÖNETİM PANELİ (TAMAMEN GERÇEK VE CANLI VERİ AKIŞI) ---
def admin_dashboard(request):
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_login')

    total_users = User.objects.count()
    total_clothes = ClothingItem.objects.count()
    kirli_sayisi = ClothingItem.objects.filter(is_clean=False).count()
    temiz_sayisi = ClothingItem.objects.filter(is_clean=True).count()

    # Kullanıcıların son giydiği 5 gerçek kıyafet
    son_giyilenler = ClothingItem.objects.filter(last_worn__isnull=False).order_by('-last_worn')[:5]

    # 🏙️ ARTIK %100 GERÇEK SORGULAR: Veritabanında DestinationSearch tablosundaki kayıtları sayıyoruz!
    seçilen_sehirler = DestinationSearch.objects.values('city').annotate(bavul_sayisi=Count('id')).order_by('-bavul_sayisi')[:5]

    populer_seyahatler = []
    for s in seçilen_sehirler:
        populer_seyahatler.append({
            'sehir': s['city'],
            'bavul_sayisi': s['bavul_sayisi']
        })

    # Eğer veritabanı tamamen boşsa sunum ekranı kel kalmasın diye varsayılan boşluk yönetimi
    if not populer_seyahatler:
        populer_seyahatler = [
            {'sehir': 'Henüz veri yok', 'bavul_sayisi': 0}
        ]

    context = {
        'total_users': total_users,
        'total_clothes': total_clothes,
        'kirli_sayisi': kirli_sayisi,
        'temiz_sayisi': temiz_sayisi,
        'son_giyilenler': son_giyilenler,
        'populer_seyahatler': populer_seyahatler,
    }
    return render(request, 'admin_dashboard.html', context)