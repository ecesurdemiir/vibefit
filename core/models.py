from django.db import models
from django.contrib.auth.models import User

class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('dis', 'Dış Giyim'),
        ('ust', 'Üst Giyim'),
        ('alt', 'Alt Giyim'),
        ('ayakkabi', 'Ayakkabı'),
        ('aksesuar', 'Aksesuar'),
    ]

    # YENİ: Kombin uyumu için Stil seçenekleri
    STYLE_CHOICES = [
        ('spor', 'Spor'),
        ('klasik', 'Klasik'),
        ('casual', 'Günlük/Casual'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        verbose_name="Kategori"
    )
    
    name = models.CharField(max_length=100, verbose_name="Kıyafet Adı")
    
    # YENİ ALANLAR: Kombin oluşturucu için gerekli
    style = models.CharField(
        max_length=20, 
        choices=STYLE_CHOICES, 
        default='casual', 
        verbose_name="Stil"
    )
    color = models.CharField(max_length=30, verbose_name="Renk", blank=True, null=True)
    
    is_clean = models.BooleanField(default=True, verbose_name="Temiz mi?")
    is_favorite = models.BooleanField(default=False, verbose_name="Favori mi?")
    is_waterproof = models.BooleanField(default=False, verbose_name="Su Geçirmez mi?")

    min_temp = models.IntegerField(default=0, verbose_name='Min Derece')
    max_temp = models.IntegerField(default=30, verbose_name='Max Derece')

    last_worn = models.DateTimeField(null=True, blank=True, verbose_name="Son Giyilme Tarihi")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        verbose_name_plural = "Kıyafetler"