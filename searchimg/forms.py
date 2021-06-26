from django import forms
from .models import sekil

class Imageform(forms.ModelForm):
    class Meta:
        model = sekil
        fields = ('image',)