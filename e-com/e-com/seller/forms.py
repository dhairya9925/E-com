from django import forms
from .models import Seller

class UpdateSeller(forms.ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'  # Include all fields in the model
