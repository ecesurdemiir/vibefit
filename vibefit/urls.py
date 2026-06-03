from django.contrib import admin
from django.urls import path, include 
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('toggle-status/<int:item_id>/', views.toggle_status, name='toggle_status'),
    path('toggle-favorite/<int:item_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history_view, name='history'),
    path('wear/<int:item_id>/', views.wear_item, name='wear_item'),
    path('bavul/', views.bavul_hazirla, name='bavul_hazirla'),
    path('yonetim-paneli/', views.admin_dashboard, name='admin_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)