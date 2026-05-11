from django import forms
from .models import ClothingItem

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['category', 'name', 'color', 'min_temp', 'max_temp', 'is_waterproof']
        # Tasarımı biraz güzelleştirmek için basit CSS sınıfları ekliyoruz
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Örn: Kırmızı Kazak'}),
            'color': forms.TextInput(attrs={'placeholder': 'Örn: Kırmızı'}),
        }