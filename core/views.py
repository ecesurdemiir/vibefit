from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ClothingItem
from .forms import ClothingItemForm
from .utils import get_weather
from django.db.models import Q
from django.utils import timezone 

@login_required(login_url='login')
def index(request):
    weather_data = get_weather()
    current_temp = weather_data['temp']
    
    # 4. FİKİR: GELİŞMİŞ HAVA DURUMU (Hissedilen Sıcaklık)
    feels_like_temp = weather_data.get('feels_like', current_temp)
    
    is_raining_or_snowing = weather_data['is_precipitating']
    current_city = weather_data['city']

    if request.method == 'POST':
        form = ClothingItemForm(request.POST)
        if form.is_valid():
            yeni_kiyafet = form.save(commit=False)
            yeni_kiyafet.user = request.user
            yeni_kiyafet.save()
            return redirect('index')
    else:
        form = ClothingItemForm()

    kyafetler = ClothingItem.objects.filter(user=request.user)

    # 2. FİKİR: ÇAMAŞIR GÜNÜ GÖSTERGESİ
    total_items = kyafetler.count()
    clean_items = kyafetler.filter(is_clean=True).count()
    
    if total_items > 0:
        clean_percentage = int((clean_items / total_items) * 100)
    else:
        clean_percentage = 100

    # KARAR MOTORU FİLTRESİ
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

    # --- 1. FİKİR: AKILLI KOMBİN OLUŞTURUCU (DÜZELTİLEN KISIM) ---
    kombin = None
    
    # Hava durumuna uyan tüm üst giyimleri alıyoruz
    ust_giyimler = recommended_items.filter(category='ust')
    
    # Tam bir eşleşme (Üst + Alt + Ayakkabı) bulana kadar sırayla dene
    for ust in ust_giyimler:
        alt_giyim = recommended_items.filter(category='alt', style=ust.style).first()
        ayakkabi = recommended_items.filter(category='ayakkabi', style=ust.style).first()
        
        # Eğer bu üst giyimin 'stiline' uygun alt ve ayakkabı varsa kombini tamamla!
        if alt_giyim and ayakkabi:
            kombin = {
                'ust': ust,
                'alt': alt_giyim,
                'ayakkabi': ayakkabi
            }
            break # Kombini bulduk, döngüyü (aramayı) durdur.

    # En son giyilen ürün
    last_worn_item = ClothingItem.objects.filter(
        user=request.user, 
        last_worn__isnull=False
    ).order_by('-last_worn').first()

    context = {
        'items': kyafetler,
        'form': form,
        'recommended': recommended_items,
        'temp': current_temp,
        'feels_like': feels_like_temp,          
        'is_raining': is_raining_or_snowing,
        'city': current_city,
        'last_worn_item': last_worn_item, 
        'clean_percentage': clean_percentage,   
        'kombin': kombin,                       
    }
    return render(request, 'index.html', context)

# --- SON GİYDİKLERİM SİSTEMİ ---

@login_required(login_url='login')
def wear_item(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.last_worn = timezone.now()
    item.is_clean = False
    item.save()
    return redirect('history')

@login_required(login_url='login')
def history_view(request):
    history = ClothingItem.objects.filter(
        user=request.user, 
        last_worn__isnull=False
    ).order_by('-last_worn')
    return render(request, 'history.html', {'history': history})

# --- DİĞER YARDIMCI FONKSİYONLAR ---

@login_required(login_url='login')
def delete_item(request, item_id):
    kyafet = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    if request.method == 'POST':
        kyafet.delete()
    return redirect('index')

@login_required(login_url='login')
def toggle_status(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.is_clean = not item.is_clean
    item.save()
    return redirect('index')

@login_required(login_url='login')
def toggle_favorite(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.is_favorite = not item.is_favorite
    item.save()
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