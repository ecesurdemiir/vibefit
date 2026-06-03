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
    STYLE_CHOICES = [
        ('spor', 'Spor'),
        ('klasik', 'Klasik'),
        ('casual', 'Günlük/Casual'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategori")
    name = models.CharField(max_length=100, verbose_name="Kıyafet Adı")
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='casual', verbose_name="Stil")
    color = models.CharField(max_length=30, verbose_name="Renk", blank=True, null=True)
    is_clean = models.BooleanField(default=True, verbose_name="Temiz mi?")
    is_favorite = models.BooleanField(default=False, verbose_name="Favori mi?")
    is_waterproof = models.BooleanField(default=False, verbose_name="Su Geçirmez mi?")
    min_temp = models.IntegerField(default=0, verbose_name='Min Derece')
    max_temp = models.IntegerField(default=30, verbose_name='Max Derece')
    last_worn = models.DateTimeField(null=True, blank=True, verbose_name="Son Giyilme Tarihi")

    # YENİ ALAN ↓
    photo = models.ImageField(
        upload_to='clothing/',
        null=True,
        blank=True,
        verbose_name="Fotoğraf"
    )

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return None  # template'de varsayılan görselle hallederiz

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        verbose_name_plural = "Kıyafetler"