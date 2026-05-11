from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    
    # İŞTE BURASI EKSİKTİ: Durum Değiştirme Yolu
    path('toggle-status/<int:item_id>/', views.toggle_status, name='toggle_status'),
    
    # KAYIT VE GİRİŞ İŞLEMLERİ:
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]