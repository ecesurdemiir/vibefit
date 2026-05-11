from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ClothingItem
from .forms import ClothingItemForm
from .utils import get_weather
from django.db.models import Q

@login_required(login_url='login')
def index(request):
    # 1. Kuryeden güncel verileri alıyoruz
    weather_data = get_weather()
    current_temp = weather_data['temp']
    is_raining_or_snowing = weather_data['is_precipitating']
    current_city = weather_data['city'] # YENİ: Şehir bilgisini de aldık

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

    # KARAR MOTORU FİLTRESİ
    recommended_items = ClothingItem.objects.filter(
        user=request.user,
        is_clean=True,
        min_temp__lte=current_temp,
        max_temp__gte=current_temp
    )

    if is_raining_or_snowing:
       recommended_items = recommended_items.filter(
            Q(is_waterproof=True) | 
            (~Q(category__name__icontains='dış') & ~Q(category__name__icontains='ayakkabı'))
        )

    context = {
        'items': kyafetler,
        'form': form,
        'recommended': recommended_items,
        'temp': current_temp,
        'is_raining': is_raining_or_snowing,
        'city': current_city # YENİ: Şehri HTML'e gönderiyoruz
    }
    return render(request, 'index.html', context)

# --- Aşağıdaki kodlar aynı ---
@login_required(login_url='login')
def delete_item(request, item_id):
    kyafet = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    if request.method == 'POST':
        kyafet.delete()
    return redirect('index')

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

@login_required(login_url='login')
def toggle_status(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, user=request.user)
    item.is_clean = not item.is_clean
    item.save()
    return redirect('index')