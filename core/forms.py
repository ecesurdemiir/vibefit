from django import forms
from .models import ClothingItem

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        # DİKKAT: 'style' başta olmak üzere eksik alanlar eklendi
        fields = [
            'category', 
            'name', 
            'style', 
            'color', 
            'min_temp', 
            'max_temp', 
            'is_waterproof', 
            'is_clean', 
            'is_favorite'
        ]
        
        # Tasarımı ana sayfana uyumlu (Bootstrap) hale getirdik
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select mb-2'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Örn: Siyah Spor Tişört'}),
            'style': forms.Select(attrs={'class': 'form-select mb-2'}),
            'color': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Örn: Siyah'}),
            'min_temp': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
            'max_temp': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
            'is_waterproof': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'is_clean': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }