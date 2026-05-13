from django.contrib import admin
from .models import ClothingItem

# CategoryAdmin kısmını tamamen sildik çünkü Category modeli artık yok.

@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    # Admin panelinde hangi sütunları göreceğimizi seçiyoruz
    # Not: Kategori artık bir seçim (choice) olduğu için direkt 'category' olarak kalabilir.
    list_display = ('name', 'category', 'is_clean', 'min_temp', 'max_temp', 'is_waterproof')
    
    # Filtreleme özelliği ekliyoruz
    list_filter = ('category', 'is_clean', 'is_waterproof')
    
    # Arama çubuğu ekliyoruz
    search_fields = ('name',)