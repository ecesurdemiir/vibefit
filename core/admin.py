from django.contrib import admin
from .models import ClothingItem



@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    # Admin panelinde hangi sütunları göreceğimizi seçtik
    # Not: Kategori artık bir seçim (choice) olduğu için direkt 'category' olarak kalabilir.
    list_display = ('name', 'category', 'is_clean', 'min_temp', 'max_temp', 'is_waterproof')
    
    # Filtreleme özelliği eklendi
    list_filter = ('category', 'is_clean', 'is_waterproof')
    
    # Arama çubuğu eklendi
    search_fields = ('name',)