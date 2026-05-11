from django.db import models
from django.contrib.auth.models import User

# 1. Kategori Tablosu (ForeignKey puanı için gerekli)
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategori Adı")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kategoriler"

# 2. Kıyafet (Envanter) Tablosu
class ClothingItem(models.Model):
    # Kullanıcı ilişkisi: Herkes sadece kendi dolabını görecek
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Kategori ilişkisi: Bir kıyafetin bir kategorisi olur (ForeignKey)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategori")
    
    name = models.CharField(max_length=100, verbose_name="Kıyafet Adı")
    color = models.CharField(max_length=30, verbose_name="Renk")
    
    # Envanter Durumu: Temiz mi? (Stok mantığı)
    is_clean = models.BooleanField(default=True, verbose_name="Temiz mi?")
    
    # Akıllı Karar Motoru Verileri (Derece aralıkları)
    # Bu değerleri ileride API'den gelen sıcaklıkla kıyaslayacağız
    min_temp = models.IntegerField(default=0, verbose_name="Minimum Sıcaklık")
    max_temp = models.IntegerField(default=30, verbose_name="Maximum Sıcaklık")
    
    # Hava Durumu Özelliği
    is_waterproof = models.BooleanField(default=False, verbose_name="Su Geçirmez mi?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kıyafetler"