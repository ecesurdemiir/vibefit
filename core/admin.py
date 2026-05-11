from django.contrib import admin

from .models import Category, ClothingItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    # Admin panelinde hangi sütunları göreceğimizi seçiyoruz
    list_display = ('name', 'category', 'is_clean', 'min_temp', 'max_temp', 'is_waterproof')
    # Filtreleme özelliği ekliyoruz
    list_filter = ('category', 'is_clean', 'is_waterproof')
    # Arama çubuğu ekliyoruz
    search_fields = ('name',)
